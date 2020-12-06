from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import *
import win32gui
import sys
import time
from PIL import Image
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
while(run):
    hwnd = win32gui.FindWindow(None,"LINE")
    app = QApplication(sys.argv)
    screen = QApplication.primaryScreen()
    img = screen.grabWindow(hwnd).toImage()

    img.save("./OCR/screencapture/screenshot.jpg")
    time.sleep(0.5)


    mg = Image.open('./OCR/screencapture/screenshot.jpg')
    new_mg = mg.crop((480, 100, 1920, 900))
    new_mg.save('./OCR/screencapture/screenshot2.jpg') 
    mcg = Image.open('./OCR/screencapture/screenshot2.jpg')
    text = pytesseract.image_to_string(mcg, lang='chi_tra')
    k=open('./OCR/old/text.txt','w+',encoding="utf-8")
    k.write(text)
    print(text)
    """merge()
    for i in range(9):
        print("sleep"+i+"s")
        time.sleep(1)"""

