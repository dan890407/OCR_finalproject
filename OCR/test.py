from ocr_lib import *


hwnd = catch("HwndWrapper[Bluestacks.exe;;ab47773c-2155-41f2-893b-7f8210ebb9a0]","BlueStacks")
print(hex(hwnd))
app_screenshot(hwnd,"./screenshot/bluestack")
divid("./screenshot/bluestack.jpg",683,259,1189,663,"./screenshot/newbluestack")