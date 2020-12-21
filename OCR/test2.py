from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import *
import win32gui
import sys
import time
from PIL import Image,ImageEnhance
import pytesseract
def merge():
<<<<<<< HEAD
    unprocess_link = './OCR/old//text.txt' 
    processed_link = './OCR/new//text.txt' 
=======
    unprocess_link = './old//text.txt' 
    processed_link = './new//text.txt' 
>>>>>>> fa614abbc630b47cafaf508047cba9fb9b231520
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
<<<<<<< HEAD
<<<<<<< HEAD
=======
print(type(hwnd))
>>>>>>> fa614abbc630b47cafaf508047cba9fb9b231520
=======
>>>>>>> da89157aae23bdc73a9b154ba0fd1af99c08d0e9
while(run):

    screen = QApplication.primaryScreen()
    img = screen.grabWindow(hwnd).toImage()

<<<<<<< HEAD
    img.save("./OCR/screencapture/screenshot.jpg")
    time.sleep(0.5)


    mg = Image.open('./OCR/screencapture/screenshot.jpg').convert('L')
=======
    img.save("./screencapture/screenshot.jpg")
    time.sleep(0.5)


    mg = Image.open('./screencapture/screenshot.jpg').convert('L')
>>>>>>> fa614abbc630b47cafaf508047cba9fb9b231520
    new_mg = mg.crop((520, 80, 1920, 870))
    enh_con = ImageEnhance.Contrast(new_mg)
    contrast=2
    image_contrasted = enh_con.enhance(contrast)
<<<<<<< HEAD
    image_contrasted.save('./OCR/screencapture/screenshot2.jpg') 
    mcg = Image.open('./OCR/screencapture/screenshot2.jpg')
=======
    image_contrasted.save('./screencapture/screenshot2.jpg') 
    mcg = Image.open('./screencapture/screenshot2.jpg')
>>>>>>> fa614abbc630b47cafaf508047cba9fb9b231520
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

