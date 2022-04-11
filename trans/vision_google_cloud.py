from PyInstaller.utils.hooks import collect_data_files
#############################
try:
    from vision import *
except: 
    from trans.vision import *
#############################
from google.cloud import vision
import os
import io

#############################
class Vision_google_cloud(Vision):
    
    def __init__(self):
        
        info_paths = ["./acquired-script-333402-9f47de5a4da5.json", 
                      "./tokens/acquired-script-333402-9f47de5a4da5.json", 
                      "../tokens/acquired-script-333402-9f47de5a4da5.json",
                      "../../tokens/acquired-script-333402-9f47de5a4da5.json",
                      "../../../tokens/acquired-script-333402-9f47de5a4da5.json"]
        
        found = False
        
        for path in info_paths:
            if os.path.exists(path) == True:
                os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path
                found = True
        if found == False:
            raise "API file loading failed!!"
        
        self.client = vision.ImageAnnotatorClient()


    def extract_text(self, file_path):
        with io.open(file_path, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)

        response = self.client.text_detection(image=image)
        texts = response.text_annotations
        text_list = list(map(lambda x: x.description, texts))

        if response.error.message:
            raise Exception(
                '{}\nFor more info on error messages, check: '
                'https://cloud.google.com/apis/design/errors'.format(
                    response.error.message))

        if len(text_list) > 0:
            text = text_list[0]

        return text


