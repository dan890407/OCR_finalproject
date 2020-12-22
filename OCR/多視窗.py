from ocr_lib import *

run=True
while(run):
    hwnd = catch("Chrome_WidgetWin_1","【#狗屎寫手】謝忻會來亂談什麼話題呢？ - YouTube - Google Chrome")
    web_screenshot(hwnd,"./screenshot/youtube")
    divid("./screenshot/youtube.jpg",1384,251,1789,889,"./screenshot/newyoutube")
    text = ocr("./screenshot/newyoutube.jpg")
    write(text,'./text_file/text')
    merge('./text_file/text','./text_file/all_text')
    time.sleep(2)
    hwnd = catch("Chrome_WidgetWin_1","HowFun / 性知識大亂鬥 ft. 阿滴、白癡公主、Joeman、酷炫 - YouTube - Google Chrome")
    web_screenshot(hwnd,"./screenshot/youtube1")
    divid("./screenshot/youtube1.jpg",1384,251,1789,889,"./screenshot/newyoutube1")
    text = ocr("./screenshot/newyoutube1.jpg")
    write(text,'./text_file/text1')
    merge('./text_file/text1','./text_file/all_text1')
    time.sleep(2)
