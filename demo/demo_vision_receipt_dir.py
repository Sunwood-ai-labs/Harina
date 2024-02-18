import base64
import requests
import os
from dotenv import load_dotenv
import pprint
import json
import pandas as pd
import glob

# .envファイルから環境変数を読み込む
load_dotenv()

# .envファイルからAPIキーを読み込む
YOUR_GOOGLE_AI_STUDIO_API_KEY = os.getenv("GOOGLE_AI_STUDIO_API_KEY")
# または
# YOUR_GOOGLE_AI_STUDIO_API_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# カテゴリデータを読み込む
df_uploaded = pd.read_csv("data/category.csv", header=None, names=['category'])

# カテゴリ文字列を生成
CATEGORIES_STRING = df_uploaded['category'].str.cat(sep=',')

# ユーザーがアップロードしたファイルを読み込んで内容を確認する
receipt_temp_path = 'data/RECEIPT_JSON_FORMAT.txt'

# ファイルの内容を読み込む
with open(receipt_temp_path, 'r', encoding='utf-8') as file:
    RECEIPT_JSON_FORMAT = file.read()


# システムプロンプトを定義
SYSTEM_PROMPT = f"""
画像のレシートを下記のJSONフォーマットで解析してください。
カテゴリは下記のリストから適切なカテゴリを選択してください。
リストにないカテゴリは選択しないでください。
{CATEGORIES_STRING}

## 出力フォーマット (JSON形式):
{RECEIPT_JSON_FORMAT}
"""

# 画像をBase64形式にエンコードする関数
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# 指定ディレクトリ内のすべてのJPEG画像を検索
image_paths = glob.glob("data/img/*.jpg")

# APIリクエストの設定
url = "http://localhost:8080/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {YOUR_GOOGLE_AI_STUDIO_API_KEY}"
}

for image_path in image_paths:
    # 画像名に基づく出力ファイル名を生成
    image_name = os.path.basename(image_path)
    output_file_name = f"output/receipt_{image_name.replace('.jpg', '.json')}"
    
    # 出力フォルダに同名のファイルが存在する場合はスキップ
    if os.path.exists(output_file_name):
        print(f"Skipping {image_name} as output JSON already exists.")
        continue
    
    # 画像をBase64でエンコード
    base64_image = encode_image(image_path)
    
    # リクエストデータの設定
    data = {
        "model": "gpt-4-vision-preview",
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": f"{SYSTEM_PROMPT}"},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
            ]
        }],
        "temperature": 0.7
    }

    # APIリクエストを送信し、応答を表示
    response = requests.post(url, json=data, headers=headers)
    
    # 応答データをPythonの辞書に変換
    data = response.json()
    pprint.pprint(data)
    
    # 'choices'の最初の要素から'message'の'content'を取得して表示
    content = data['choices'][0]['message']['content']
    print("-------------")
    _receipt = content.replace("```json", "").replace("```", "")
    print(_receipt)
    
    # JSON文字列をPythonの辞書に変換
    receipt = json.loads(_receipt)
    
    # 辞書をJSON形式でファイルに書き込み
    with open(output_file_name, 'w', encoding='utf-8') as f:
        json.dump(receipt, f, ensure_ascii=False, indent=2)
    print(f"Output saved to {output_file_name}")