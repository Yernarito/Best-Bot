#############################
import pytesseract
import cv2
#############################
try:
    from vision import *
except: 
    from trans.vision import *
#############################
'''
opencv-python 
open cv python 
 config.py
  pip install opencv-python==4.5.3.56 
 .
'''

class Vision_tesseract(Vision):
    def __init__(self):
        pass

    def extract_text(self, file_path):
        '''
        tesseract
        1. brew tesseract.
        2. brew tesseract-lang
        3. which tesseract
         pytesseract.pytesseract.tesseract_cmd .
        '''
        pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'
        image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        (thresh, im_bw) = cv2.threshold(image, 127, 255, cv2.THRESH_TRUNC | cv2.THRESH_OTSU)
        text = pytesseract.pytesseract.image_to_string(image, lang='kor+eng+rus+kaz', config='--psm 4 --oem 3')

        return text

    
