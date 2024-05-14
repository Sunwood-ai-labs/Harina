import anthropic
import base64

client = anthropic.Anthropic()

# 画像ファイルをbase64エンコード
with open("data/img/20240218124248_IMG_5323_v2.jpg", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode("utf-8")

message = client.messages.create(
    model="claude-3-haiku-20240307",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": encoded_string,
                    },
                },
                {
                    "type": "text",
                    "text": "画像のレシートを日本語で解説して"
                }
            ],
        }
    ],
)
print(message)