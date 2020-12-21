import win32gui
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import *
from PIL import ImageGrab,Image,ImageEnhance
import win32con
import time
import sys
import pytesseract

def catch_web(ipclass,name):            #取得web視窗代碼 ipclass=類名 name=標題
    hwnd = win32gui.FindWindow(ipclass,name)
    win32gui.SetForegroundWindow(hwnd)
    img = ImageGrab.grab()
    img.save("screenshot.jpg")


def catch_app(ipclass,name):            #取得應用程式視窗代碼 ipclass=類名 name=標題
    hwnd = win32gui.FindWindow(ipclass,name)
    app = QApplication(sys.argv)
    screen = QApplication.primaryScreen()
    img = screen.grabWindow(hwnd).toImage()
    img.save("screenshot.jpg")


def divid(img,left,up,right,down):      #切割成特定範圍的圖片
    new_img = Image.open(img)
    new_mg = new_img.crop((left,up,right,down))
    enh_con = ImageEnhance.Contrast(new_mg)
    contrast=2
    image_contrasted = enh_con.enhance(contrast)
    image_contrasted.save('newscreenshot.jpg')


def merge(new_text,all_text):             #將newtext合併到alltext
    f = open(all_text,'r',encoding="utf-8")   
    lines = f.readlines()
    last_line = lines[-1]
    f.close()
    
    k=open(new_text,'r',encoding="utf-8") 
    c=open(all_text,'a+',encoding="utf-8")          
    check = 0
    for line in k.readlines():
        if check == 1:
            c.write(line)
        if line == last_line:
            check = 1
    k.close()
    if check==0:
        k=open(new_text,'r',encoding="utf-8")
        for line in k.readlines():
            c.write(line)


def ocr(img):
    test_img = Image.open(img)
    text = pytesseract.image_to_string(test_img, lang='chi_tra+equ+eng')
    print(text)
