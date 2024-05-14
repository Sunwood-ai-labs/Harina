import os
import json
import pprint
import glob
from api.APIRequestSender import APIRequestSender
from api.ImageEncoder import ImageEncoder
import anthropic

class ReceiptAnalyzer:
    def __init__(self, config_loader, category_loader):
        self.config_loader = config_loader
        self.category_loader = category_loader
        self.client = anthropic.Anthropic()

    def create_system_prompt(self, categories):
        """
        システムプロンプトを生成します。
        """
        # ユーザーがアップロードしたファイルを読み込んで内容を確認する
        receipt_temp_path = 'data/RECEIPT_JSON_FORMAT.txt'
        with open(receipt_temp_path, 'r', encoding='utf-8') as file:
            receipt_json_format = file.read()
        
        system_prompt = f"""
        画像のレシートを下記のJSONフォーマットで解析してください。
        カテゴリは下記のリストから適切なカテゴリを選択してください。
        リストにないカテゴリは選択しないでください。
        {categories}

        ## 出力フォーマット (JSON形式):
        {receipt_json_format}
        """
        return system_prompt

    def analyze_receipts(self, image_folder, save_dir):
        """
        指定されたフォルダ内のすべてのレシート画像を解析します。
        """
        # 保存ディレクトリのパスを生成
        save_path = os.path.join("output", save_dir)
        # 保存ディレクトリが存在しない場合は作成
        os.makedirs(save_path, exist_ok=True)
        
        image_paths = glob.glob(f"{image_folder}/*.jpg")
        print(f"image_paths:{image_paths}")
        for image_path in image_paths:
            image_name = os.path.basename(image_path)
            output_file_name = os.path.join(save_path, f"receipt_{image_name.replace('.jpg', '.json')}")

            # 出力フォルダに同名のファイルが存在する場合はスキップ
            if os.path.exists(output_file_name):
                print(f"Skipping {image_name} as output JSON already exists.")
                continue

            base64_image = ImageEncoder.encode_image(image_path)
            system_prompt = self.create_system_prompt(self.category_loader.categories)

            message = self.client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1024,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": system_prompt
                            },
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/jpeg",
                                    "data": base64_image
                                }
                            }
                        ],
                    }
                ],
            )

            # 応答データの処理
            content = message.content[0].text
            _receipt = content.replace("```json", "").replace("```", "")
            receipt = json.loads(_receipt)
            
            with open(output_file_name, 'w', encoding='utf-8') as f:
                json.dump(receipt, f, ensure_ascii=False, indent=2)
            print(f"Output saved to {output_file_name}")

        return receipt