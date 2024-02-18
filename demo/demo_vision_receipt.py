import base64
import requests
import os
from dotenv import load_dotenv
import pprint
import json
import pandas as pd

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

# JSONフォーマットのテンプレートを定義
JSON_FORMAT = """
{
  "store": {
    "name": ""
  },
  "transaction": {
    "date": "",
    "time": ""
  },
  "items": [
    {
      "item_name": "",
      "unit_price": ,
      "quantity": ,
      "unit": "",
      "category": "".
      "total_price": 
    }
  ],
  "total": {
    "amount": ,
    "points_earned": ,
    "points_used": 
  },
  "payment": {
    "payment_method": ""
  }
}
"""

# システムプロンプトを定義
SYSTEM_PROMPT = f"""
画像のレシートを下記のJSONフォーマットで解析してください。
カテゴリは下記のリストから適切なカテゴリを選択してください。
リストにないカテゴリは選択しないでください。
{CATEGORIES_STRING}

## 出力フォーマット (JSON形式):
{JSON_FORMAT}
"""

# 画像をBase64形式にエンコードする関数
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# 画像のパス
image_path = "data/img/IMG_5322_v2.jpg"

# 画像をBase64でエンコード
base64_image = encode_image(image_path)

# APIリクエストの設定
url = "http://localhost:8080/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {YOUR_GOOGLE_AI_STUDIO_API_KEY}"
}
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

print(SYSTEM_PROMPT)

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
with open('output/receipt_IMG_5322_v2.json', 'w', encoding='utf-8') as f:
    json.dump(receipt, f, ensure_ascii=False, indent=2)