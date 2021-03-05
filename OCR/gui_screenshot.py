import pyautogui
import tkinter as tk 

root = tk.Tk()
root.title('screenshot')     
root.geometry('800x500')

def create():       #建造一個top-level的視窗
    top = tk.Toplevel()
    top.overrideredirect(True)    #忘了
    top.attributes("-alpha", 0.3)    #透明度，讓他有灰灰的感覺
    top.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight())) #跟螢幕一樣大
    top.configure(bg="black")
    root.withdraw()     #暫時隱藏root(主畫面)，不是top-level哦
    cv = tk.Canvas(top) #可以圈出框框的畫布
    
    def button_1(event):    #其他我都照抄懶的理解
        global x, y ,xstart,ystart
        global rec
        x, y = event.x, event.y
        xstart,ystart = event.x, event.y
        up.set(xstart)      #紀錄點下去那個點
        left.set(ystart)    #紀錄點下去那個點
        cv.configure(height=1)
        cv.configure(width=1)
        cv.config(highlightthickness=0) # 無邊框
        cv.place(x=event.x, y=event.y)
        rec = cv.create_rectangle(0,0,0,0,outline='red',width=2,dash=(4,4))

    def b1_Motion(event):
        global x, y,xstart,ystart
        x, y = event.x, event.y
        cv.configure(height = event.y - ystart)
        cv.configure(width = event.x - xstart)
        cv.coords(rec,0,0,event.x-xstart,event.y-ystart)

    def buttonRelease_1(event):
        global xend,yend
        xend, yend = event.x, event.y
        down.set(xend)  #紀錄釋放的那個點
        right.set(yend) #紀錄釋放的那個點
        top.destroy()   #把top-level刪除掉
        root.deiconify()    #恢復root(主視窗)
    
    top.bind("<Button-1>", button_1)  # 滑鼠左鍵點選->顯示子視窗 
    top.bind("<B1-Motion>", b1_Motion)# 滑鼠左鍵移動->改變子視窗大小
    top.bind("<ButtonRelease-1>", buttonRelease_1) # 滑鼠左鍵釋放->記錄最後遊標的位置
    


b = tk.Button(root,text='screenshot',command=create)
b.pack()
up = tk.StringVar()
left = tk.StringVar()
down = tk.StringVar()
right = tk.StringVar()
l1 = tk.Label(root,textvariable=up,bg='red',width='20')
l2 = tk.Label(root,textvariable=left,bg='orange',width='20')
l3 = tk.Label(root,textvariable=down,bg='yellow',width='20')
l4 = tk.Label(root,textvariable=right,bg='green',width='20')
l1.pack()
l2.pack()
l3.pack()
l4.pack()

root.mainloop()