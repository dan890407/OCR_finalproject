from ocr_lib import *


run=True
while(run):
    hwnd = catch("Qt5QWindowIcon","LINE")
    app_screenshot(hwnd,"./screenshot/line")
    divid("./screenshot/line.jpg",1384,251,1860,889,"./screenshot/newline")
    text = ocr("./screenshot/newline.jpg")
    write(text,'./text_file/line')
    merge('./text_file/line','./text_file/all_line')
    time.sleep(10)