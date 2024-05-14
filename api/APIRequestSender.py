import requests
import os  # osモジュールをインポート

class APIRequestSender:
    def __init__(self, api_key):
        self.api_key = api_key
        # 環境変数からURLを取得
        self.url = os.getenv('API_URL', "http://localhost:8080/v1/chat/completions")  # デフォルト値も設定
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def send_request(self, data):
        response = requests.post(self.url, json=data, headers=self.headers)
        return response.json()
