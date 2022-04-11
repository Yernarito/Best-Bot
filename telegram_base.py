import os
import sys
from telegram import *
from telegram.ext import *
from requests import *
from abc import *

class   telegram_base(metaclass=ABCMeta):

    def __init__(self, token_paths:list, id_paths:list):
        #############################
        # Проблема с отсутствием папок с относительным путем, таких как ./ или ../, заключается в следующем.
         # Это связано с тем, что Python создает временную папку и выполняет ее.
         # Поэтому используйте sys._MEIPASS для обозначения временно созданной папки.
        try:
            print("Try 1 : " + sys._MEIPASS)
            os.chdir(sys._MEIPASS)
        except:
            print("Try 2 : " + os.getcwd())
            os.chdir(os.getcwd())
        
        #############################
        def read_file(path_list):
            found = False
            ret_val = ""
            for path in path_list:
                if os.path.exists(path) == True: 
                    file = open(path, "r", encoding="utf8")                
                    ret_val = file.read()
                    file.close()
                    found = True
                    print("file открыл и прочитал.(path={0})".format(path))
                    break
            if found == False:
                print("file не могу читать. бот не работает.")

            return ret_val
        
        
        #############################
        # telegram параметр
        self.my_token = read_file(token_paths)  
        self.my_id    = int(read_file(id_paths))
        
        # Настройка данных для перевода.
        self.user_data = {int:[]}
        self.reply_string = ""
        self.bot = Bot(self.my_token)
        # updater
        self.updater = Updater(token=self.my_token, use_context=True)
        self.dispatcher = self.updater.dispatcher


    ##################################
    # send message
    def send_msg(self, msg, is_sending=True):
        try:
            print(msg)
            if is_sending == True:
                self.bot.send_message(chat_id=self.my_id, text=msg)        
        except:
            try:
                print("처음 응답이 없어 두 번째 시도합니다.")
                self.bot.send_message(chat_id=self.my_id, text=msg)
            except:
                print("send_message를 다시 시도하였으나 실패함.")
 
    ##################################
    def start_bot(self):            
        ##################################
        handler_text    = MessageHandler(Filters.text     & (~Filters.command), self.proc_text    )
        handler_photo   = MessageHandler(Filters.photo    & (~Filters.command), self.proc_photo   )
        handler_document= MessageHandler(Filters.document & (~Filters.command), self.proc_document)       
        
        self.dispatcher.add_handler(handler_text    )
        self.dispatcher.add_handler(handler_photo   )
        self.dispatcher.add_handler(handler_document)
        # polling
        self.updater.start_polling()
        self.send_msg('Запустите Telegram-бота.')


    ##################################
    # text handler
    @abstractmethod
    def proc_text(self, update:Update, context:CallbackContext):
        pass
        
        
    ##################################
    # photo handler
    @abstractmethod
    def proc_photo(self, update:Update, context:CallbackContext):
        pass
        
        
    ##################################
    # document handler
    @abstractmethod
    def proc_document(self, update:Update, context:CallbackContext):
        pass
