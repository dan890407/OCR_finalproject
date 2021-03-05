import win32gui
import pyautogui
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import *
from PIL import ImageGrab,Image,ImageEnhance
import win32con
import time
import sys,os
import pytesseract
class project :
    def __init__(self,hwnd,filename,left,up,right,down,interval):
        self.hwnd=hwnd
        self.filename=filename
        self.left=left
        self.up=up
        self.right=right
        self.down=down
        self.interval=interval

    def autofetch(self):
        ipclass = win32gui.GetClassName(self.hwnd)
        if ipclass=="Chrome_WidgetWin_1":
            self.web_screenshot()
        else:
            self.app_screenshot()
        self.divid()
        self.ocr()
        self.merge()

    def web_screenshot(self):            #web截圖 圖名稱screenshot
        win32gui.SetForegroundWindow(self.hwnd)
        img = ImageGrab.grab()
        img.save("./screenshot/temporary.jpg")

    def app_screenshot(self):            #應用程式截圖 圖名稱screenshot
        app = QApplication(sys.argv)
        screen = QApplication.primaryScreen()
        img = screen.grabWindow(self.hwnd).toImage()
        img.save("./screenshot/temporary.jpg")

    def divid(self):      #切割成特定範圍的圖片
        img = Image.open("./screenshot/temporary.jpg")
        new_mg = img.crop((self.left,self.up,self.right,self.down))
        enh_con = ImageEnhance.Contrast(new_mg)
        contrast=2
        image_contrasted = enh_con.enhance(contrast)
        image_contrasted.save("./screenshot/"+self.filename+".jpg")
        os.remove("./screenshot/temporary.jpg")

    def ocr(self):                           #ocr影像辨識
        test_img = Image.open("./screenshot/"+self.filename+".jpg")
        newtext = pytesseract.image_to_string(test_img, lang='chi_tra+equ+eng')
        fixed_text = newtext.strip()
        self.text=fixed_text
    
    def merge(self):             #合併
        temporary='./text_file/temporary'
        goal = './text_file/'+self.filename
        with open(temporary,'w',encoding='utf-8') as t:
            t.writelines(self.text)
        with open(goal,'r',encoding='utf-8') as f:
            lines = f.readlines()
        t = open(temporary,'r',encoding='utf-8')
        f = open(goal,'a+',encoding="utf-8")   
        if os.path.getsize(goal):
            last_line = lines[-1]
            print(last_line)
            check = 0
            for line in t.readlines():
                if check == 1:
                    if line.split():
                        f.writelines(line)
                    else:
                        f.writelines("")
                if line == last_line:
                    check = 1
            if check==0:
                for line in t.readlines():
                    if line.split():
                        f.writelines(line)
                    else:
                        f.writelines("")
        else:
            for line in t.readlines():
                if line.split():
                    f.writelines(line)
                else:
                    f.writelines("")
        t.close()
        f.close()
        os.remove(temporary)
    