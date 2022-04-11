import requests
import uuid
from translator import *

class Translator_ms(Translator):
    def __init__(self):
        # Add your subscription key and endpoint
        self.subscription_key = "78cc47eac697477e9c3c800758cedb86"
        self.endpoint = "https://api.cognitive.microsofttranslator.com"
        # Add your location, also known as region. The default is global.
        # This is required if using a Cognitive Services resource.
        self.location = "koreacentral"
        self.path = '/translate'
        self.constructed_url = self.endpoint + self.path

    def translate(self, text, target='kk'):
        # detectedlang, detectedval = langid.classify(text)
        params = {
            'api-version': '3.0',
            'to': target
        }
        headers = {
            'Ocp-Apim-Subscription-Key': self.subscription_key,
            'Ocp-Apim-Subscription-Region': self.location,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }
        # You can pass more than one object in body.
        body = [{
            'text': text
        }]
        request = requests.post(self.constructed_url, params=params, headers=headers, json=body)
        response = request.json()
        
        translated_text = ""        
        if request.status_code == 200:
            temp1 = response[0]
            temp2 = temp1['translations']
            temp3 = temp2[0]
            temp4 = temp3['text']
            translated_text = temp4
        else:
            translated_text = "."

        return translated_text
