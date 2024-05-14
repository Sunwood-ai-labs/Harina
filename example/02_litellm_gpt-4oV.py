import os
import sys
from litellm import completion
from art import text2art
from termcolor import colored

# 現在のファイル名を取得
file_name = os.path.basename(__file__)
print(colored(text2art(file_name), 'yellow'))

# デコレーションされたメッセージ
def decorated_message(message):
    art_message = text2art("OpenAI Response")
    colored_message = colored(art_message, 'cyan')
    return colored_message + "\n" + colored(message, 'green')
# openai call
response = completion(
    model = "gpt-4o", 
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
                                "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
                                }
                            }
                        ]
        }
    ],
)

# 結果を表示
print(decorated_message(response['choices'][0]['message']['content']))