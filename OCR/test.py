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