import time
import win32gui, win32ui, win32con, win32api
from PIL import Image
import pytesseract
def window_capture(filename):
    hwnd = win32gui.FindWindow(None,"LINE") # 視窗的編號，0號表示當前活躍視窗 #用vs studio裡的spy++來獲得個別視窗控制代碼 # 我還沒研究出 win32gui.FindWindow怎麼用
    hwndDC = win32gui.GetWindowDC(hwnd) # 根據視窗控制代碼獲取視窗的裝置上下文DC（Divice Context）
    mfcDC = win32ui.CreateDCFromHandle(hwndDC) # 根據視窗的DC獲取mfcDC
    saveDC = mfcDC.CreateCompatibleDC() # mfcDC建立可相容的DC
    saveBitMap = win32ui.CreateBitmap()# 建立bigmap準備儲存圖片
    MoniterDev = win32api.EnumDisplayMonitors(None, None)# 獲取監控器資訊
    w = MoniterDev[0][2][2]
    h = MoniterDev[0][2][3]
    # print w,h　　　#圖片大小
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)# 為bitmap開闢空間
    saveDC.SelectObject(saveBitMap)# 高度saveDC，將截圖儲存到saveBitmap中
    saveDC.BitBlt((0,0), (1100,550), mfcDC, (400,141), win32con.SRCCOPY)# 擷取從左上角（0，0）長寬為（w，h）的圖片
    saveBitMap.SaveBitmapFile(saveDC, "c:\\temp\\bli.bmp")
    print(hwnd)
window_capture("bli.bmp")
image = Image.open('c:\\temp\\bli.bmp')
print(pytesseract.image_to_string(image,lang='chi_tra'))


