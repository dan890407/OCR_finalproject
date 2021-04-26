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

    def judge(self):     #判斷是否符合資格 -> weight >= 6
        temporary='./text_file/temporary.txt'
        location = ["地址","地點","區域"]
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
                        if s in location:
                            flag = True
                        if s in important:
                            weight = weight + 2
                            index.append(s+':'+sentence.strip().split(":")[1])
                            important.remove(s)
                            continue
                        if s in keywords:
                            weight = weight + 1
                            index.append(s+':'+sentence.strip().split(":")[1])
                            keywords.remove(s)
        print(index,weight)
        if weight < 6:
            with open(temporary,'w',encoding='utf-8') as t:
                t.write("")
        else:
            with open(temporary,'w',encoding='utf-8') as t:
                for sentence in index:
                    t.writelines(sentence)
                    t.write('\n')
                    
    def jsons_nlp(self):
        temporary='./text_file/temporary.txt'
        def write_json(data, filename='./text_file/text.json'):
            data=json.load(open(filename))
            if type(data) is dict:
                data = [data]
            data.append(a)
            with open(filename, 'w') as outfile:
                json.dump(data, outfile,indent=4)
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
        answerdict=dict()
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
                    answerdict[question]=re.compile(regularform[question]).findall(answer.replace(" ",""))[0]
                    flag=1
            if flag == 0:
                answerdict[question]="null"
                print(f"Question: {question}")
                print(f"Answer not found")
        print("--- %s seconds ---" % (time.time() - start_time))
        print (answerdict)
        write_json(answerdict)
        with open("temporary.txt","w",encoding="UTF-8") as f:
            f.seek(0)
            f.truncate()
            f.write(json.dumps(answerdict,indent=5,ensure_ascii=False))
        
    def jsons(self):
        temporary='./text_file/temporary.txt'
        localdic=dict()
        form={
                "price":["價格","開價","售價","總價"],
                "location":["地址","地點","區域"],
                "size":["建坪","坪數","總建"],
                "inner":["室內","主附"],
                "car":["車位"],
                "age":["屋齡"],
                "format":["格局"],
                "managementfee":["管理費"],
                "facing":["坐向","朝向","座向"]		
        }
        regularform={
                "price":"(\d+)萬",
                "location":"(\w+)",
                "size":"(\d*[\.\d]*)[坪]*",
                "inner":"(\d*[\.\d]*)[坪]*",
                "car":"(\w)個",
                "car2":["無","沒有","0"],
                "age":"(\d+)年",
                "format":"(\d+)[房/]*(\d+)[廳/]*(\d+)[衛]*",
                "managementfee":"(\d+)[元]*",
                "facing":["東","南","西","北"]	
        }
        with open(temporary,"r+",encoding="UTF-8") as f:
            texts=f.readlines()
            for line in texts:
                flag=0
                if line.find(":") != -1:
                    for name,data in form.items():  
                        for i in data:
                            if i==line[:line.find(":")]:   
                                if name=="facing":  #找朝向的第一個方位  通常是面對方向
                                    facing_cut=[]
                                    for fac in jieba.cut(line[(line.find(":")+1):len(line)-1],cut_all = False):	
                                        facing_cut.append(fac)
                                    for facs in facing_cut:
                                        if facs in regularform['facing']:
                                            localdic[name]=facs
                                else: #用正規式處理字串(value)
                                    if name=='format':
                                        try:
                                            if len(re.compile(regularform[name]).findall(line[(line.find(":")+1):len(line)-1])):	
                                                localformat=re.compile(regularform[name]).findall(line[(line.find(":")+1):len(line)-1])[0]
                                                a=''
                                                for jj in localformat:
                                                    a+=jj+'/'
                                                localdic[name]=a
                                            else:
                                                pass
                                        except Exception as e:
                                            print("exception :")
                                            print(e)																			
                                    elif name=='car':
                                        if len(re.compile(regularform[name]).findall(line[(line.find(":")+1):len(line)-1])):
                                            localdic[name]=''.join(re.compile(regularform[name]).findall(line[(line.find(":")+1):len(line)-1]))
                                        else:
                                            if line[(line.find(":")+1):len(line)-1] in regularform['car2']:
                                                localdic[name]="no"
                                            else:
                                                localdic[name]="yes"
                                    else:#格局標準化
                                        if len(re.compile(regularform[name]).findall(line[(line.find(":")+1):len(line)-1])):
                                            localdic[name]=re.compile(regularform[name]).findall(line[(line.find(":")+1):len(line)-1])[0]
                                        else:
                                            localdic[name]=''.join(re.compile(regularform[name]).findall(line[(line.find(":")+1):len(line)-1]))
            f.seek(0)
            f.truncate()
            f.write(json.dumps(localdic,indent=5,ensure_ascii=False))

    def merge(self):
        temporary='./text_file/temporary.txt'
        goal = self.path+self.filename+".txt"     
        f = open(goal,'a',encoding="utf-8")   
        t = open(temporary,'r',encoding='utf-8')
        if os.path.getsize(temporary) != 2:
            for line in t.readlines():
                    f.writelines(line)
            f.write(",\n")
        t.close()
        f.close()
        os.remove(temporary)

    def fix(self):
        price = ["價格","開價","售價","總價"]
        location = ["地址","地點","區域"]
        size = ["建坪","坪數","總建"]
        inner = ["室內","主附"]
        car = ["車位"]
        age = ["屋齡"]
        form = ["格局"]
        managementfee = ["管理費"]
        facing = ["坐向","朝向","座向"]
        direction = ["東","南","西","北","東北","東南","西南","西北"]
        temporary='./text_file/temporary.txt'
        index = []

        with open(temporary,'r',encoding='utf-8') as t:
            for line in t.readlines():
                front = line.strip().split(":")[0]
                back = line.strip().split(":")[1]
                cut_back = jieba.lcut(back)
                print(cut_back)
                if front in price:
                    front = 'price'
                    for i in cut_back:
                        if is_number(i) == True:
                            index.append('"'+front+'":"'+i+'"')
                            break
                    continue
                elif front in location:
                    front = 'location'
                    index.append('"'+front+'":"'+back+'"')
                    continue
                elif front in size:
                    front = 'size'
                    for i in cut_back:
                        if is_number(i) == True:
                            index.append('"'+front+'":"'+i+'"')
                            break
                    continue
                elif front in inner:
                    front = 'inner'
                    for i in cut_back:
                        if is_number(i) == True:
                            index.append('"'+front+'":"'+i+'"')
                            break
                    continue
                elif front in car:
                    front = 'car'
                    if '無' in cut_back or '沒有' in cut_back:
                        index.append('"'+front+'":"no"')
                    else:
                        index.append('"'+front+'":"yes"')
                    continue
                elif front in age:
                    front = 'age'
                    for i in cut_back:
                        if is_number(i) == True:
                            index.append('"'+front+'":"'+i+'"')
                            break
                    continue
                elif front in form:
                    front = 'form'
                    count = 0
                    num = []
                    if '陽台' not in cut_back:
                        for i in cut_back:
                            if is_number(i) == True:
                                num.append(i)
                                count = count + 1
                                if count == 3:
                                    index.append('"'+front+'":"'+num[0]+'/'+num[1]+'/'+num[2]+'"')
                    continue
                elif front in managementfee:
                    front = 'managementfee'
                    for i in cut_back:
                        if is_number(i) == True:
                            index.append('"'+front+'":"'+i+'"')
                            break
                    continue
                elif front in facing:
                    front = 'facing'
                    for i in cut_back:
                        if i in direction:
                            index.append('"'+front+'":"'+i+'"')
                    continue
        with open(temporary,'w',encoding='utf-8') as t:
            t.write('{\n')
            for sentence in index:
                    t.writelines(sentence+',\n')
            t.write('}')
