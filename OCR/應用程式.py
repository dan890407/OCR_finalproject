from ocr_lib import *


run=True
while(run):
    hwnd = catch("HwndWrapper[Bluestacks.exe;;4197d16e-70aa-4dad-ae15-f79286ae866d]","BlueStacks")
    app_screenshot(hwnd,"./screenshot/bluestack")
    divid("./screenshot/bluestack.jpg",683,259,1189,663,"./screenshot/newbluestack")
    text = ocr("./screenshot/newbluestack.jpg")
    write(text,'./text_file/bluestack')
    merge('./text_file/bluestack','./text_file/all_bluestack')
    time.sleep(10)