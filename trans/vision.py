from abc import *

class Vision:
    def __init__(self):
        pass

    @abstractmethod
    def extract_text(self, file_path):
        pass
