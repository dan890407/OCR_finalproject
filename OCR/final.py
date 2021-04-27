from cv2 import cv2
import numpy as np
import pyautogui
import win32gui
import win32con
import win32com.client
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import *
from PIL import ImageGrab,Image,ImageEnhance
import sys,os,re,json,time
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

def is_number(s):
    try:  
        float(s)
        return True
    except ValueError:
        pass 
    try:
        import unicodedata 
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False

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

    def cut_word(self):  #斷詞取得目標
        temporary = './text_file/temporary.txt'
        keywords = []
        self.localdic = dict()
        form={
                "price":["價格","開價","售價","總價"],
                "location":["地址","地點","區域"],
                "size":["建坪","坪數","總建"],
                "age":["屋齡"],
                "format":["格局"],	
        }
        regularform={
                "price":"(\d+)萬",
                "location":"(\w+)",
                "size":"(\d*[\.\d]*)[坪]*",
                "age":"(\d+)年",
                "format":"(\d+)[房/]*(\d+)[廳/]*(\d+)[衛]*",
        }
        with open(temporary,'w',encoding='utf-8') as t:       #temporary檔寫入ocr檔案
            t.writelines(self.text.replace(" ",""))
        with open('./jieba/key_word.txt','r',encoding='utf-8') as f:    #將關鍵字傳入index
            for word in  f.readlines():
                keywords.append(word.strip())
        with open(temporary,'r',encoding='utf-8') as t:     #從temporary篩選出需要的資料在寫入
            for sentence in t.readlines():
                if ':' in sentence:
                    session = sentence.strip().split(":")[0]
                    contain = sentence.strip().split(":")[1]
                    cut_session = jieba.cut(session)
                    for word in cut_session:
                        if word in keywords:
                            for name,data in form.items():      #正規化
                                for i in data:
                                    if i == word:  
                                        if name=='format':
                                            try:
                                                if len(re.compile(regularform[name]).findall(contain)):
                                                    localformat=re.compile(regularform[name]).findall(contain)[0]
                                                    a=''
                                                    self.format_number = 0      #房間總數
                                                    for rom in localformat:
                                                        a += rom+'/'
                                                        self.format_number += int(rom)
                                                    self.localdic[name] = a
                                                else:
                                                    pass
                                            except Exception as e:
                                                print("exception :")
                                                print(e)																			
                                        else:
                                            if len(re.compile(regularform[name]).findall(contain)):
                                                self.localdic[name]=re.compile(regularform[name]).findall(contain)[0]
                                            else:
                                                self.localdic[name]=''.join(re.compile(regularform[name]).findall(contain))
        print(self.localdic["location"])
        print(type(self.localdic["location"]))

    def jsons_nlp(self):
        temporary='./text_file/temporary.txt'
        def strQ2B(s):
            rstring = ""
            for uchar in s:
                u_code = ord(uchar)
                if u_code == 12288:  # 全形空格直接轉換
                    u_code = 32
                elif 65281 <= u_code <= 65374:  # 全形字元（除空格）根據關係轉化
                    u_code -= 65248
                rstring += chr(u_code)
            return rstring
        wrapper = textwrap.TextWrapper(width=80) 
        start_time = time.time()
        tokenizer = BertTokenizer.from_pretrained("bert-base-chinese")
        config = BertConfig.from_pretrained("./models/config.json") 
        model = BertForQuestionAnswering.from_pretrained("./models/pytorch_model.bin", config=config)
        with open (temporary,"r",encoding="utf-8") as f:
            context=f.read()
            context=strQ2B(context)
            context=context.replace("\n",",")
            print(context)
        form={
                    "price":["價格","開價","售價","總價"],
                    "location":["地址","地點","區域"],
                    "size":["建坪","坪數","總建"],
                    "age":["屋齡"],
                    "format":["格局"],	
        }
        regularform={
                    "price":"(\d+)萬",
                    "location":"(\w+)",
                    "size":"(\d*[\.\d]*)[坪]*",
                    "age":"(\d+)年",
                    "format":"(\d+)[房/]*(\d+)[廳/]*(\d+)[衛]*",
        }
        questions = ['format','age','size','price']
        self.localdic= dict()
        for question in questions:
            flag=0
            for ques in form[question]:

                inputs = tokenizer(ques, context, add_special_tokens=True, return_tensors="pt")
                input_ids = inputs["input_ids"].tolist()[0]

                context_tokens = tokenizer.convert_ids_to_tokens(input_ids)

                logits = model(**inputs,return_dict=True)
                answer_start_scores = logits['start_logits'] 
                answer_end_scores = logits['end_logits']
                answer_start = torch.argmax(answer_start_scores)
                answer_end = torch.argmax(answer_end_scores) + 1
                answer = tokenizer.convert_tokens_to_string(context_tokens[answer_start:answer_end])


                if answer!="[CLS]":
                    print(f"Question: {question}")
                    print(f"Answer: {answer}")
                    self.localdic[question]=re.compile(regularform[question]).findall(answer.replace(" ",""))[0]
                    flag=1
            if flag == 0:
                self.localdic[question]="null"
                print(f"Question: {question}")
                print(f"Answer not found")
        print("--- %s seconds ---" % (time.time() - start_time))
        print (self.localdic)

    def judge(self,index,index1,index2): 
        temporary='./text_file/temporary.txt'

        #取出dictionary的值放入預測模型，判斷是否符合標準，有則保留dict
        #放入index,index1,index2
        #if放入index1，index1.append(self.localdic)
        #else，index2.append(self.localdic)
        #index1,index2宣告在fbclub_project的start函式
        index.append(self.localdic)
        index1.append(self.localdic)
        index2.append(self.localdic)
        os.remove(temporary)
   
    def makefile(self,index,index1,index2):        #將txt轉成另存成json
        goal = self.path+self.filename+".txt" 
        jsonfile1 = './house_web/static/data/'+self.filename+'1.json'
        jsonfile2 = './house_web/static/data/'+self.filename+'2.json'
        with open(goal,"a",encoding='utf-8') as g:
            json.dump(index,g,indent=4,ensure_ascii=False)
        with open(jsonfile1,"a",encoding='utf-8') as j:
            json.dump(index1,j,indent=4,ensure_ascii=False)
        with open(jsonfile2,"a",encoding='utf-8') as j:
            json.dump(index2,j,indent=4,ensure_ascii=False)