import anthropic
import pprint
client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-3-haiku-20240307",
    max_tokens=1000,
    temperature=0.0,
    system="Respond only in Yoda-speak.",
    messages=[
        {"role": "user", "content": "How are you today?"}
    ]
)

print(message.content)
print("----------------")
pprint.pprint(message)
print("----------------")
pprint.pprint(message.content[0].text)
