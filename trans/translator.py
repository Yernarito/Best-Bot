from abc import *

class TranslationData:
    def __init__(self, srclang, trglang: list):
        self.srclang:str  = srclang
        self.trglang:list = trglang

class Translator(metaclass=ABCMeta):
    def __init__(self):
        self.translated_text = ""
        pass

    @abstractmethod
    def translate(self, text, target='kk'):
        pass