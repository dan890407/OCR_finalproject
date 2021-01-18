from ocr_lib import *


run=True
while(run):
    hwnd = catch("Chrome_WidgetWin_1","Facebook - Google Chrome")
    web_screenshot(hwnd,"./screenshot/fb")
    divid("./screenshot/fb.jpg",1450,450,1830,980,"./screenshot/newfb")
    text = ocr("./screenshot/newfb.jpg")
    write(text,'./text_file/fb')
    merge('./text_file/fb','./text_file/all_fb')
    time.sleep(2)