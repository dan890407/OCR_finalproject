from fbclub_lib import *

test=project(0X180ace,"test",418,236,1027,765,"./text_file/") 
run=False

if run == True:
    while(run):
        test.web_screenshot()
        pos = imagesearch("./picture/threedot.jpg")
        if pos != [800,500]:
            pyautogui.scroll(int(test.up)-pos[1])
            time.sleep(1)
            pyautogui.scroll(-20)
        else:
            pyautogui.scroll(int(test.up)-int(test.down))
            print(2)
        time.sleep(3)
else:
    '''test.web_screenshot()
    test.divid()
    test.ocr()
    test.txt()
    test.cut_word()
    test.judge()'''
    with open('./text_file/fbclub.txt','r',encoding='utf-8') as f:
        data = json.load(f)
        pri = 0
        addre = 0
        pa = 0
        al = 0
        b = 0
        c = 0
        for i in range(len(data)):
            if 'price' in data[i] and 'location' not in data[i]:
                pri = pri + 1
            if 'price' not in data[i] and 'location' in data[i]:
                addre = addre + 1
            if ('price' and 'location') in data[i]:
                pa = pa + 1
            if ('price' and 'location') in data[i]:
                if ('format' and 'size') in data[i]:
                    al = al + 1
            if 'price' not in data[i]:
                b = b + 1
            if 'location' not in data[i]:
                c = c + 1
        print('只有價格的筆數為: '+str(pri))
        print('只有地址的筆數為: '+str(addre))
        print('有價格和地址的筆數為: '+str(pa))
        print('有價格地址格局坪數的筆數為: '+str(al))
        print('沒有價格的筆數為: '+str(b))
        print('沒有地址的筆數為: '+str(c))
        print('總共有'+str(len(data))+'筆資料')