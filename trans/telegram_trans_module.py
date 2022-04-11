import os
import re
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from telegram_base import * 
from translator import TranslationData
from translator_google_cloud import *
from vision_google_cloud import *
from vision_tesseract import *

class telegram_trans_module(telegram_base):
    
    def __init__(self):
        telegram_base.__init__(self, 
                               ["./token_translator.txt", 
                                "./tokens/token_translator.txt",
                                "../tokens/token_translator.txt",
                                "../../tokens/token_translator.txt",
                                "../../../tokens/token_translator.txt"],
                               ["./id.txt", 
                                "./tokens/id.txt",
                                "../tokens/id.txt",
                                "../../tokens/id.txt",
                                "../../../tokens/id.txt"])
        ##################################
        # 
        self.user_data = {int: TranslationData}
        self.languages = {"kk":"kk", # 
                          "ko":"", # 
                          "ru":"", # 
                          "en":""} # 

        self.send_string = ""
        self.order = False  # True = order, False = words
        self.option_verify = True  # True=ON, False=OFF
        
        self.translator = Translator_google_cloud()
        # self.extractor   = Vision_tesseract()
        self.extractor  = Vision_google_cloud()
        return

    
    def start_bot(self):
        if self.user_data.get(self.my_id) == None:
            self.user_data[self.my_id] = TranslationData("auto", ["kk"])
        
        self.dispatcher.add_handler(CommandHandler("lang", self.langCommand))
        
        print("\n") # 
        message = "If you want to change to some languages.\nClick /lang option!"
        self.send_msg(message)
        
        return super().start_bot()
    

    def check_order(self, user_id, text):
        # global userData
        result   = ""
        lang     = ""
        strings  = []
        
        if text.find("\\") <= -1:
            return result
        strings = re.findall(r'\w+', text)
        if len(strings) == 0: 
            return result
        
        ###################################
        for lang in strings:
            if self.languages.get(lang) != None:
                if self.languages[lang] == "":
                    if lang not in self.user_data[user_id].trglang:
                        self.user_data[user_id].trglang.append(lang)
                        self.languages[lang] = lang
                else:
                    # Количество списков должно быть не менее 1
                    if lang in self.user_data[user_id].trglang:
                        if len(self.user_data[user_id].trglang) > 1:
                            index = self.user_data[user_id].trglang.index(lang)
                            self.user_data[user_id].trglang.remove(self.user_data[user_id].trglang[index])
                            self.languages[lang] = ""
                        else:
                            result = "Должен быть хотя бы один язык для перевода.\n"

        ###############################################
        if len(self.user_data[user_id].trglang) > 0:
            result = result  + "Язык ввода будет переведен как {0}.".format(self.user_data[user_id].trglang)

        return result
    
    
    ##################################
    # translate
    def translate_text(self, user_id, text):
        result_string = ""
        translated_txt = ""
        verifing_text = ""
        
        for targetlang in self.user_data[user_id].trglang:
            translated_txt = self.translator.translate(text, targetlang)
            result_string = result_string + translated_txt + "\n\n"
            if verifing_text == "": # 
                verifing_text = translated_txt

        if self.option_verify is True and len(self.user_data[user_id].trglang) > 0:
            # 
            if "ko" not in self.user_data[user_id].trglang: 
                translated_txt = self.translator.translate(verifing_text, "ko")
                result_string = result_string + "-------Первая проверка перевода-------\n" + translated_txt + "\n"
            
        return result_string


    ##################################
    # text handler  
    def proc_text(self, update, context): 
        user_id = update.effective_chat.id
        user_text = update.message.text

        send_string = self.check_order(user_id, user_text)          
        if send_string  == "":
            send_string = self.translate_text(user_id, user_text)   
                        
        self.send_msg(send_string)
        return
        

    ##################################
    # photo handler
    def proc_photo(self, update, context):     
        user_id = update.effective_chat.id
        
        list_index = len(update.message.photo)
        list_index -= 1
        if list_index < 0:
            return
        
        file = update.message.photo[list_index].file_id
        obj = context.bot.get_file(file)
        obj.download()

        index = obj.file_path.rfind("/")
        file_name = obj.file_path[index+1:]
        file_path = "./" + file_name

        #######################################
        extracted_text = self.extractor.extract_text(file_path) # 
        self.send_msg(extracted_text)  # 
        #######################################
        send_string = self.translate_text(user_id, extracted_text) # 
        self.send_msg(send_string) # 
        #######################################
        os.remove(file_path) # 
        return
    
    
    ####################################
    # doc handler
    def proc_document(update, context):
        return
    
    
    ####################################
    # doc handler
    def langCommand(self, update:Update, context:CallbackContext):
        buttons = [[KeyboardButton("\\kk 🇰🇿"), KeyboardButton("\\ko 🇰🇷")],
                   [KeyboardButton("\\ru 🇷🇺"), KeyboardButton("\\en 🇬🇧")]]

        context.bot.send_message(chat_id=update.effective_chat.id, 
                                 text="choose language!",
                                 reply_markup=ReplyKeyboardMarkup(buttons))
        return


##################################
if "__main__" == __name__:
    tele = telegram_trans_module()
    tele.start_bot()
