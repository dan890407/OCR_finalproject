from cv2 import cv2
import numpy as np
import pyautogui
import time
import win32gui
import win32com.client
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import *
from PIL import ImageGrab,Image,ImageEnhance
import win32con
import time
import sys,os
import pytesseract
import jieba

def click_image(image,pos,  action, timestamp,offset=5):
    img = cv2.imread(image)
    height, width, channels = img.shape
    pyautogui.moveTo(pos[0] + offset, pos[1] + offset, timestamp)
    pyautogui.click(button=action)


def imagesearch(image, precision=0.8):
    im = pyautogui.screenshot()
    img_rgb = np.array(im)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(image, 0)
    template.shape[::-1]

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val < precision:
        return [800,500]
    return max_loc #返回圖片座標

class project :
    def __init__(self,hwnd,filename,left,up,right,down,path):
        self.hwnd=hwnd
        self.filename=filename
        self.left=left
        self.up=up
        self.right=right
        self.down=down
        newpath=str(path)+"/"
        self.path=newpath
        self.count = 0

    def web_screenshot(self):            #web截圖 圖名稱screenshot
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')
        win32gui.SetForegroundWindow(self.hwnd)
        img = ImageGrab.grab()
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
        newtext = pytesseract.image_to_string(test_img, lang='chi_tra+fbclub')
        fixed_text = newtext.strip()
        self.text=fixed_text
        print(self.text)

    def txt(self):   #生成txt
        temporary = './text_file/temporary.txt'
        view = './text_file/view.txt'
        with open(temporary,'w',encoding='utf-8') as t:
            t.writelines(self.text.replace(" ",""))
        with open(view,'a',encoding='utf-8') as v:
            v.writelines(self.text.replace(" ",""))
            v.writelines('\n-----\n')

    def cut_word(self):  #斷詞+關鍵字
        jieba.load_userdict('./jieba/fb_club_dict.txt')
        temporary = './text_file/temporary.txt'
        keywords = []
        index = []
        with open('./jieba/key_word.txt','r',encoding='utf-8') as f:
            for word in  f.readlines():
                keywords.append(word.strip())
        article = open(temporary,'r',encoding='utf-8')
        for sentence in article.readlines():
            cut_sentence = jieba.cut(sentence.strip(),cut_all = False)
            for word in cut_sentence:
                if word in keywords:
                    index.append(sentence)
        article.close()
        with open(temporary,'w',encoding='utf-8') as t:
            if len(index) != 0:
                for word in index:
                    t.writelines(word)
                t.writelines("\n-----\n")
            else:
                t.write("")

    def judge(self):     #判斷是否符合資格 -> weight > 6
        temporary='./text_file/temporary.txt'
        important = []
        keywords = []
        index = []
        with open('./jieba/key_word.txt','r',encoding='utf-8') as f:
            for word in  f.readlines():
                keywords.append(word.strip())
        with open('./jieba/important.txt','r',encoding='utf-8') as f:
            for word in f.readlines():
                important.append(word.strip())
        weight = 0
        with open(temporary,'r',encoding='utf-8') as t:
            for sentence in t.readlines():
                if ':' in sentence:
                    session = sentence.strip().split(":")[0]
                    cut_session = jieba.cut(session)
                    for s in cut_session:
                        if s in important:
                            weight = weight + 2
                            index.append(s+':'+sentence.strip().split(":")[1])
                            important.remove(s)
                            continue
                        if s in keywords:
                            weight = weight + 1
                            index.append(s+':'+sentence.strip().split(":")[1])
                            keywords.remove(s)
        print(index)
        print(weight)
        if weight < 5:
            with open(temporary,'w',encoding='utf-8') as t:
                t.write("")
        else:
            with open(temporary,'w',encoding='utf-8') as t:
                for sentence in index:
                    t.writelines(sentence)
                    t.write('\n')
    def jsons():
        form={
                "price":["價格","開價","售價","總價"],
                "location":["地址","地點","區域"],
                "size":["建坪","坪數","總建"],
                "inner":["室內","主附"],
                "floor":["樓層"],
                "car":["車位"],
                "age":["屋齡"],
                "format":["格局"],
                "managementfee":["管理費"],
                "facing":["坐向","朝向","座向"]		
        }
        regularform={
                "price":"(\d+)萬",
                "location":"(\w+)",
                "size":"(\d+)坪",
                "inner":"(\d+)坪",
                "floor":"(\d+)樓",
                "car":"(\w)個",
                "age":"(\d)年",
                "format":"(\d+)房(\d+)廳(\d+)衛",
                "managementfee":"(\d+)元",
                "facing":["東","南","西","北"]		
        }
        with open("test.txt","r",encoding="UTF-8") as f:
            with open("testjson.txt","a") as t:
                t.write("\t"+"{\n")
                texts=f.readlines()
                for line in texts:
                    if line.find(":") != -1:
                        for name,data in form.items():  
                            for i in data:
                                if i==line[:line.find(":")]:   #標準化key
                                    t.write('\t\t"'+name+'":"') #標準化key
                                    if name=="facing":  #找朝向的第一個方位  通常是面對方向
                                        flag=0
                                        for k in line[(line.find(":")+1):len(line)-1]:
                                            if k in regularform['facing']:
                                                flag=1
                                                t.write(k)
                                                break
                                    else: #用正規式處理字串(value)
                                        if name!='format':
                                            t.write(str(*re.compile(regularform[name]).findall(line[(line.find(":")+1):len(line)-1])))
                                        else:#格局標準化
                                            localformat=re.compile(regularform[name]).findall(line[(line.find(":")+1):len(line)-1])[0]
                                            for jj in localformat:
                                                t.write(jj+"/")
                        if line != texts[-1]:
                            t.write('",\n')
                        else:
                            t.write('"\n')
                t.write("\t"+"},\n")
    def merge(self):             #合併
        temporary='./text_file/temporarytojson.txt'
        goal = self.path+self.filename+".txt"     
        f = open(goal,'a',encoding="utf-8")   
        t = open(temporary,'r',encoding='utf-8')
        if os.path.getsize(temporary):
            for line in t.readlines():
                    f.writelines(line)
            f.writelines("-----\n")
        t.close()
        f.close()
        os.remove(temporary)