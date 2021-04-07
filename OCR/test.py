from gui_lib import *
from fbclub_lib import *

test=project(0X1903d8,"test",302,232,1043,850,"./text_file/") 
run=True

if run == True:
    while(run):
        test.web_screenshot()
        pos = imagesearch("threedot.jpg")
        if pos != [800,500]:
            pyautogui.scroll(int(test.up)-pos[1])
            time.sleep(1)
            pyautogui.scroll(-20)
        else:
            pyautogui.scroll(int(test.up)-int(test.down))
            print(2)
        time.sleep(3)
else:
    test.web_screenshot()
    pos = imagesearch("threedot.jpg")
    if pos != [800,500]:
        pyautogui.scroll(int(test.up)-pos[1])
