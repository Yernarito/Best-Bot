from PyInstaller.utils.hooks import collect_data_files
from google.cloud import translate_v3beta1 as translate
from google.cloud import translate
#############################
try:
    from translator import *
except: 
    from trans.translator import *
#############################
import sys
import os

'''

grpc 

/usr/local/lib/python3.9/site-packages/PyInstaller/hooks
'''

# filename = "acquired-script-333402-9f47de5a4da5.json"

# # determine if application is a script file or frozen exe
# if getattr(sys, 'frozen', False):
#     application_path = os.path.dirname(sys.executable)
# elif __file__:
#     application_path = os.path.dirname(__file__)

# filepath = os.path.join(application_path, filename)
# print(filepath)

class Translator_google_cloud(Translator):

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
        
        self.client = translate.TranslationServiceClient()


    def translate(self, text, target='kk'):
        parent = f"projects/acquired-script-333402/locations/global"
        response = self.client.translate_text(parent=parent,
                                            contents=[text],
                                            mime_type='text/plain',  # mime types: text/plain, text/html
                                            source_language_code=None,
                                            target_language_code=target)
        if len(response.translations) < 0:
            return 
    
        return response.translations[0].translated_text
