import os
import json
import pprint
import glob
from api.APIRequestSender import APIRequestSender
from api.ImageEncoder import ImageEncoder

class ReceiptAnalyzer:
    def __init__(self, config_loader, category_loader):
        self.config_loader = config_loader
        self.category_loader = category_loader
        self.api_sender = APIRequestSender(self.config_loader.config['API_KEY'])

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
        image_paths = glob.glob(f"{image_folder}/*.jpg")
        for image_path in image_paths:
            image_name = os.path.basename(image_path)
            output_file_name = f"output/{save_dir}/receipt_{image_name.replace('.jpg', '.json')}"
            
            # 出力フォルダに同名のファイルが存在する場合はスキップ
            if os.path.exists(output_file_name):
                print(f"Skipping {image_name} as output JSON already exists.")
                continue

            base64_image = ImageEncoder.encode_image(image_path)
            system_prompt = self.create_system_prompt(self.category_loader.categories)

            data = {
                "model": "gpt-4-vision-preview",
                "messages": [{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": f"{system_prompt}"},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                    ]
                }],
                "temperature": 0.7
            }

            response_data = self.api_sender.send_request(data)

            # 応答データの処理
            content = response_data['choices'][0]['message']['content']
            _receipt = content.replace("```json", "").replace("```", "")
            receipt = json.loads(_receipt)
            
            with open(output_file_name, 'w', encoding='utf-8') as f:
                json.dump(receipt, f, ensure_ascii=False, indent=2)
            print(f"Output saved to {output_file_name}")

        return receipt
