from ocr_lib import *
import tkinter as tk 
from PIL import ImageTk

window = tk.Tk()
window.title('OCR')
window.geometry('800x500') 

def func(event):
    pos =win32gui.GetCursorPos()      
    hwnd=win32gui.WindowFromPoint(pos) #10和11行取得hwnd
    var.set(hex(hwnd))  #標籤顯示hwnd
    print(hex(hwnd))

var = tk.StringVar()
l = tk.Label(window, textvariable=var)
l.pack()

img = Image.open("eye.gif")     #按鈕圖標
img = img.resize((30,30))
photoImg =  ImageTk.PhotoImage(img)
b=tk.Button(window, image=photoImg,cursor="tcross")     #讓鼠標經過圖時變成十字
b.pack()
b.bind("<ButtonRelease-1>",func)   #左鍵放開觸發func
window.mainloop()