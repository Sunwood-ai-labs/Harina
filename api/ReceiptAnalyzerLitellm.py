import os
import json
import pprint
import glob
from litellm import completion
from art import text2art
from termcolor import colored
from pathlib import Path
import base64
from PIL import Image
import io
import asyncio
import shutil

class ReceiptAnalyzerLitellm:
    def __init__(self, config_loader, category_loader):
        self.config_loader = config_loader
        self.category_loader = category_loader

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

    def optimize_image(self, image_path, max_size=1024):
        """
        画像を最適化します。
        - サイズを縮小
        - 品質を調整
        """
        try:
            with Image.open(image_path) as img:
                # 画像が大きすぎる場合はリサイズ
                if max(img.size) > max_size:
                    ratio = max_size / max(img.size)
                    new_size = tuple(int(dim * ratio) for dim in img.size)
                    img = img.resize(new_size, Image.Resampling.LANCZOS)
                
                # メモリ内にJPEG形式で保存
                buffer = io.BytesIO()
                img.save(buffer, format="JPEG", quality=85, optimize=True)
                return base64.b64encode(buffer.getvalue()).decode('utf-8')
        except Exception as e:
            print(f"画像の最適化中にエラーが発生: {e}")
            # 最適化に失敗した場合は通常のエンコードを使用
            return self.encode_image(image_path)

    def encode_image(self, image_path):
        """
        画像をBase64エンコードします。
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def decorated_message(self, message):
        """
        デコレーションされたメッセージを生成します。
        """
        art_message = text2art("OpenAI Response")
        colored_message = colored(art_message, 'cyan')
        return colored_message + "\n" + colored(message, 'green')

    async def analyze_receipts(self, image_folder, save_dir, message, retry_count=3):
        """
        指定されたフォルダ内のすべてのレシート画像を解析します。
        エラーが発生した場合、指定された回数だけ再試行します。
        """
        # 保存ディレクトリのパスを生成
        save_path = os.path.join("output", save_dir)
        # 保存ディレクトリが存在しない場合は作成
        os.makedirs(save_path, exist_ok=True)
        
        image_paths = glob.glob(f"{image_folder}/*.jpg")
        print(f"image_paths:{image_paths}")
        for image_path in image_paths:
            
            await message.channel.send(f"---\n`{os.path.basename(image_path)}` の解析を開始します...")
            for retry in range(retry_count):
                try:
                    image_name = os.path.basename(image_path)
                    output_file_name = os.path.join(save_path, f"receipt_{image_name.replace('.jpg', '.json')}")

                    # 出力フォルダに同名のファイルが存在する場合はスキップ
                    if os.path.exists(output_file_name):
                        print(f"Skipping {image_name} as output JSON already exists.")
                        break

                    # 画像の最適化
                    base64_image = self.optimize_image(image_path)
                    file_extension = Path(image_path).suffix[1:]
                    url = f"data:image/{file_extension};base64,{base64_image}"

                    system_prompt = self.create_system_prompt(self.category_loader.categories)

                    # タイムアウト設定付きでAPI呼び出し
                    response = await asyncio.wait_for(
                        asyncio.get_event_loop().run_in_executor(
                            None,
                            lambda: completion(
                        # model="claude-3-5-sonnet-20241022",
                        model="gpt-4o",
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": system_prompt
                                    },
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": url,
                                        },
                                    }
                                ]
                            }
                        ],
                        max_tokens=1024
                    )),
                        timeout=30.0  # 30秒のタイムアウト
                    )

                    # 応答データの処理
                    content = response['choices'][0]['message']['content']
                    _receipt = content.replace("```json", "").replace("```", "")
                    receipt = json.loads(_receipt)
                    
                    with open(output_file_name, 'w', encoding='utf-8') as f:
                        json.dump(receipt, f, ensure_ascii=False, indent=2)
                    print(f"Output saved to {output_file_name}")
                    await message.channel.send("解析が完了しました。")
                    break
                except Exception as e:
                    error_message = str(e)
                    if "timeout" in error_message.lower():
                        await message.channel.send("APIリクエストがタイムアウトしました。再試行します。")
                    if retry < retry_count - 1:
                        await message.channel.send(f"エラー発生！リトライします [{retry+1}/{retry_count}] {e}")
                        await asyncio.sleep(1)  # リトライ前に少し待機
                    else:
                        await message.channel.send(f"エラー発生！スキップします {e}")

        # 画像ファイルをアーカイブフォルダに移動
        for image_path in image_paths:
            if os.path.exists(image_path):
                archive_path = os.path.join("archive", save_dir)
                os.makedirs(archive_path, exist_ok=True)
                image_name = os.path.basename(image_path)
                shutil.move(image_path, os.path.join(archive_path, image_name))
                await message.channel.send(f"`{image_name}` をアーカイブに移動しました。")

        return receipt


