import win32gui
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import *
from PIL import ImageGrab,Image,ImageEnhance
import win32con
import time
import sys
import pytesseract
class project :
<<<<<<< HEAD
    def __init__(self,ipclass,name,lineoryoutube,left,up,right,down):
        self.ipclass=ipclass
        self.name=name
        self.lineoryoutube=lineoryoutube
=======
    def __init__(self,ipclass,name,filename,left,up,right,down):
        self.ipclass=ipclass
        self.name=name
        self.filename=filename
>>>>>>> 8fa9eb1660c69ded0843a875fe26d1ed0fd3d0df
        self.left=left
        self.up=up
        self.right=right
        self.down=down
        self.catch()
        print(hex(self.hwnd))
    def autofetch(self):
<<<<<<< HEAD
        if self.lineoryoutube=="youtube":
            self.web_screenshot()
        elif self.lineoryoutube=="line":
            self.app_screenshot
        self.divid()
        """
        self.OCR()
        """
    def catch(self):            #取得視窗代碼 ipclass=類名 name=標題
        hwnd = win32gui.FindWindow(self.ipclass,self.name)
        self.hwnd=hwnd
    def web_screenshot(self):            #web截圖 圖名稱screenshot
        win32gui.SetForegroundWindow(self.hwnd)
        img = ImageGrab.grab()
        img.save("./screenshot/"+self.lineoryoutube+".jpg")

=======
        if self.ipclass=="Chrome_WidgetWin_1":
            self.web_screenshot()
        else:
            self.app_screenshot
        self.divid()
        self.ocr()

    def catch(self):            #取得視窗代碼 ipclass=類名 name=標題
        hwnd = win32gui.FindWindow(self.ipclass,self.name)
        self.hwnd=hwnd

    def web_screenshot(self):            #web截圖 圖名稱screenshot
        win32gui.SetForegroundWindow(self.hwnd)
        img = ImageGrab.grab()
        img.save("./screenshot/"+self.filename+".jpg")
>>>>>>> 8fa9eb1660c69ded0843a875fe26d1ed0fd3d0df

    def app_screenshot(self):            #應用程式截圖 圖名稱screenshot
        app = QApplication(sys.argv)
        screen = QApplication.primaryScreen()
        img = screen.grabWindow(self.hwnd).toImage()
<<<<<<< HEAD
        img.save("./screenshot/"+self.lineoryoutube+".jpg")


    def divid(self):      #切割成特定範圍的圖片
        new_img = Image.open("./screenshot/"+self.lineoryoutube+".jpg")
=======
        img.save("./screenshot/"+self.filename+".jpg")

    def divid(self):      #切割成特定範圍的圖片
        new_img = Image.open("./screenshot/"+self.filename+".jpg")
>>>>>>> 8fa9eb1660c69ded0843a875fe26d1ed0fd3d0df
        new_mg = new_img.crop((self.left,self.up,self.right,self.down))
        enh_con = ImageEnhance.Contrast(new_mg)
        contrast=2
        image_contrasted = enh_con.enhance(contrast)
<<<<<<< HEAD
        image_contrasted.save("./screenshot/new"+self.lineoryoutube+".jpg")
    
    def ocr(self):                           #ocr影像辨識
        test_img = Image.open("./screenshot/new"+self.lineoryoutube+".jpg")
        text = pytesseract.image_to_string(test_img, lang='chi_tra+equ+eng')
        print(text)
        self.text=text
=======
        image_contrasted.save("./screenshot/new"+self.filename+".jpg")
    
    def ocr(self):                           #ocr影像辨識
        test_img = Image.open("./screenshot/new"+self.filename+".jpg")
        newtext = pytesseract.image_to_string(test_img, lang='chi_tra+equ+eng')
        fixed_text = newtext.strip()
        self.text=fixed_text
>>>>>>> 8fa9eb1660c69ded0843a875fe26d1ed0fd3d0df
    
    def merge(self,new_text,all_text):             #將newtext合併到alltext
        with open(new_text,'w',encoding='utf-8') as f:
            f.writelines(self.text)
        f = open(all_text,'r',encoding="utf-8")   
        lines = f.readlines()
        last_line = lines[-1]
        f.close()
<<<<<<< HEAD
        
=======
                
>>>>>>> 8fa9eb1660c69ded0843a875fe26d1ed0fd3d0df
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
<<<<<<< HEAD
                c.write(line)





    
=======
                c.write(line)
>>>>>>> 8fa9eb1660c69ded0843a875fe26d1ed0fd3d0df
