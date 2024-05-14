import os
import sys
from litellm import completion
from art import text2art
from termcolor import colored
import base64
from pathlib import Path

# 現在のファイル名を取得
file_name = os.path.basename(__file__)
print(colored(text2art(file_name), 'yellow'))

# 画像をBase64エンコード
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# デコレーションされたメッセージ
def decorated_message(message):
    art_message = text2art("OpenAI Response")
    colored_message = colored(art_message, 'cyan')
    return colored_message + "\n" + colored(message, 'green')

# ローカル画像のパス
image_path = "docs/IMG_6243.jpg"

base64_image = encode_image(image_path)
file_extension = Path(image_path).suffix
file_extension_without_dot = file_extension[1:]

# Base64エンコードされた画像URL
url = f"data:image/{file_extension_without_dot};base64,{base64_image}"

# ファイルが存在するか確認
if not os.path.exists(image_path):
    print(colored(f"Error: File {image_path} not found.", 'red'))
    sys.exit(1)

# OpenAI 呼び出し
response = completion(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "この画像は何?"
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
)

# 結果を表示
print(decorated_message(response['choices'][0]['message']['content']))
