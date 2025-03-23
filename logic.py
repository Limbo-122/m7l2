import json
import time

import requests

import base64
from PIL import Image
from io import BytesIO

class Text2ImageAPI:

    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, model, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']

            attempts -= 1
            time.sleep(delay)
        
def text2img(text, file_path):
    decoded_data = base64.b64decode(text)
    image = Image.open(BytesIO(decoded_data))
    image.save(file_path)


if __name__ == '__main__':
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', '157527EDD477B87F4DDF069293CCCFC1', '928D18CC45A912B57745A32D55E098AE')
    model_id = api.get_model()
    uuid = api.generate("Сфотографированый кот, сидит на крыльце в солнечную погоду, а рядом стоит небольшая ваза с цветами", model_id)
    images = api.check_generation(uuid)
    with open('text.txt', 'w', encoding='utf-8') as f:
        f.write(images[0])
    print(images)
