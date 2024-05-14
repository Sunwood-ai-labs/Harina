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

# OpenAI 呼び出し
response = completion(
    model="gpt-4o",
    messages=[{"content": "こんにちは お元気ですか？", "role": "user"}]
)

# 結果を表示
print(decorated_message(response['choices'][0]['message']['content']))