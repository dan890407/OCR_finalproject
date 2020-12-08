from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import *
import win32gui
import sys
import time
from PIL import Image,ImageEnhance
import pytesseract
def merge():
    unprocess_link = './OCR/old//text.txt' 
    processed_link = './OCR/new//text.txt' 
    f = open(processed_link,'r',encoding="utf-8")   
    lines = f.readlines()
    last_line = lines[-1]
    f.close()
    
    
    k=open(unprocess_link,'r',encoding="utf-8") 
    c=open(processed_link,'a+',encoding="utf-8")          
    check = 0
    for line in k.readlines():
        if check == 1:
            c.write(line)
        if line == last_line:
            check = 1
    k.close()
    if check==0:
        k=open(unprocess_link,'r',encoding="utf-8")
        for line in k.readlines():
            c.write(line)

run=True
hwnd = win32gui.FindWindow(None,"LINE")
app = QApplication(sys.argv)
while(run):

    screen = QApplication.primaryScreen()
    img = screen.grabWindow(hwnd).toImage()

    img.save("./OCR/screencapture/screenshot.jpg")
    time.sleep(0.5)


    mg = Image.open('./OCR/screencapture/screenshot.jpg').convert('L')
    new_mg = mg.crop((520, 80, 1920, 870))
    enh_con = ImageEnhance.Contrast(new_mg)
    contrast=2
    image_contrasted = enh_con.enhance(contrast)
    image_contrasted.save('./OCR/screencapture/screenshot2.jpg') 
    mcg = Image.open('./OCR/screencapture/screenshot2.jpg')
    text = pytesseract.image_to_string(mcg, lang='chi_tra+equ')
    """last_line=text[-1]
    check=0
    for line in text:
        if check == 1:
            print(line)
        if line == last_line:
            check = 1
    """
    """with open('./OCR/old/text.txt','w+',encoding="utf-8") as k:
        k.write(text)
        for line in k.readline():
           if 
    """
    print(text)
    """time.sleep(3)"""
    
    """merge()
    for i in range(9):
        print("sleep"+i+"s")
        time.sleep(1)"""

