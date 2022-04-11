from translator import *
from googletrans import Translator

class Translator_google(Translator):
    def __init__(self):
        self.translator = Translator(service_urls=['translate.google.com', 'translate.google.co.kr',])

    def translate(self, text, target='kk'):
        # detectedlang, detectedval = langid.classify(text)
        self.translated_ret = self.translator.translate(text, src="auto", dest=target)
        return self.translated_ret.text