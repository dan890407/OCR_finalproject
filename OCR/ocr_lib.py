import win32gui
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import *
from PIL import ImageGrab,Image,ImageEnhance
import win32con
import time
import sys
import pytesseract

def catch(ipclass,name):            #取得視窗代碼 ipclass=類名 name=標題
    hwnd = win32gui.FindWindow(ipclass,name)
    return hwnd


def web_screenshot(hwnd,screenshot):            #web截圖 圖名稱screenshot
    win32gui.SetForegroundWindow(hwnd)
    img = ImageGrab.grab()
    img.save(screenshot+".jpg")


def app_screenshot(hwnd,screenshot):            #應用程式截圖 圖名稱screenshot
    app = QApplication(sys.argv)
    screen = QApplication.primaryScreen()
    img = screen.grabWindow(hwnd).toImage()
    img.save(screenshot+".jpg")


def divid(img,left,up,right,down,newscreenshot):      #切割成特定範圍的圖片
    new_img = Image.open(img)
    new_mg = new_img.crop((left,up,right,down))
    enh_con = ImageEnhance.Contrast(new_mg)
    contrast=2
    image_contrasted = enh_con.enhance(contrast)
    image_contrasted.save(newscreenshot+".jpg")


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


def ocr(img):                           #ocr影像辨識
    test_img = Image.open(img)
    text = pytesseract.image_to_string(test_img, lang='chi_tra+equ+eng')
    print(text)
    return text


def write(text,place):                #寫檔案入place
    with open(place,'w',encoding='utf-8') as f:
        fixed_text = text.strip()
        f.writelines(fixed_text)
