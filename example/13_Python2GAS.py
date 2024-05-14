import os
import requests
import json

def send_data_to_gas(json_data, tag, file_name):
    url = os.environ['GAS_JSON2GSS_URL']
    headers = {'Content-Type': 'application/json'}
    data = {
        'json_data': json_data,
        'tag': tag,
        'file_name': file_name
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    print(response.text)

# outputフォルダ内のJSONファイルを読み込む
output_folder = 'output'

for root, dirs, files in os.walk(output_folder):
    for file_name in files:
        if file_name.endswith('.json'):
            file_path = os.path.join(root, file_name)
            with open(file_path, 'r') as file:
                json_data = json.load(file)
                tag = os.path.basename(os.path.dirname(file_path))
                send_data_to_gas(json_data, tag, file_name)