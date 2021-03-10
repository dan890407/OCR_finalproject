from tkinter import *
from tkinter import messagebox
import pyautogui
from PIL import ImageTk , Image
import win32gui
import win32con
from ocr_lib import *
from tkinter.filedialog import askdirectory
import pytesseract
import cv2 as cv
class MainPage(object):
	def __init__(self, master=None):
		self.root = master #定義內部變數root
		self.createPage()

	def createPage(self):
		self.inputPage = InputFrame(self.root) # 建立不同Frame
		self.inputPage.pack() #預設顯示資料錄入介面
class InputFrame(Frame): # 繼承Frame類
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.root = master #定義內部變數root
		self.root.geometry('%dx%d' % (800, 280)) #設定視窗大小
		self.hwnd = StringVar()
		self.top = StringVar()
		self.left = StringVar()
		self.bottom = StringVar()
		self.right = StringVar()
		self.path=StringVar()
		self.interval=StringVar()
		self.run=True
		self.createPage()
		messagebox.showinfo("提醒", "請拖曳圖標至視窗取得視窗代碼(準確拖曳至視窗上方邊框正中心)")
	
	def createPage(self):
		img = Image.open("./eye.gif")     #按鈕圖標
		img = img.resize((30,30))
		self.photoImg =  ImageTk.PhotoImage(img)	
		b=Button(self,image=self.photoImg,cursor="tcross")
		b.grid(row=0,stick=W,pady=20)
		b.bind("<ButtonRelease-1>",self.func)
		hwndlabel=Label(self, text = '視窗代碼: ')
		hwndlabel.grid(row=0, column=1,stick=W, pady=10)
		hwnd_var=Entry(self, textvariable=self.hwnd,width=15)
		hwnd_var.grid(row=0, column=2,stick=W, pady=10)
		hwnd_var.insert(0,"hwnd")
		
		b=Button(self,text="P",command=self.createscreenshot)
		b.grid(row=1,stick=W,pady=20)
		poslabel=Label(self, text = '位置(pixel上,左,下,右): ')
		poslabel.grid(row=1, column=1,stick=W, pady=3)
		pos_var1=Entry(self, textvariable=self.top,width=15)
		pos_var1.insert(0,"上")
		pos_var1.grid(row=1, column=2,stick=W, pady=3)
		pos_var2=Entry(self, textvariable=self.left,width=15)
		pos_var2.insert(0,"左")
		pos_var2.grid(row=1, column=3,stick=W, pady=3)
		pos_var3=Entry(self, textvariable=self.bottom,width=15)
		pos_var3.insert(0,"下")
		pos_var3.grid(row=1, column=4,stick=W, pady=3)
		pos_var4=Entry(self, textvariable=self.right,width=15)
		pos_var4.insert(0,"右")
		pos_var4.grid(row=1, column=5,stick=W, pady=3)

		Label(self,text = "儲存路徑:").grid(row = 2, column = 0)
		pathentry=Entry(self, textvariable =self.path)
		pathentry.insert(0,"路徑")
		pathentry.grid(row = 2, column = 1)
		Button(self, text = "路徑選擇", command = self.selectPath).grid(row = 2, column = 2)

	
		Button(self,text="間隔").grid(row=3,column=0,stick=W,pady=3)
		interval=Entry(self, textvariable=self.interval,width=15)
		interval.insert(0,"default is 5 sec")
		interval.grid(row=3,column=1,stick=W,pady=3)
		Button(self,text="測試",command=self.test_showimg).grid(row=3,column=2,stick=W,pady=3)
		Button(self,text="開始",command=self.buttonstart).grid(row=3,column=4,stick=W,pady=3)
		Button(self,text="停止",command=self.loopstop).grid(row=3,column=5,stick=W,pady=3)
	def test_showimg(self):
		"""
		src = cv.imread("./screenshot/desktop.jpg") # 這四行能在一個新視窗開啟照片
		cv.imshow("test image", src)
		cv.waitKey(0)
		cv.destroyAllWindows()
		"""
		pass
	def selectPath(self):
		path_ = askdirectory()
		path_=path_.replace("\\",'//')
		self.path.set(path_)
	
	def createscreenshot(self):       #建造一個top-level的視窗
		if self.hwnd.get() == 'hwnd':
			messagebox.showinfo("missing input", "請拖曳圖標至視窗取得視窗代碼(準確拖曳至視窗上方邊框正中心)")
			return
		win32gui.SetForegroundWindow(self.localhwnd)
		win32gui.ShowWindow (self.localhwnd,win32con.SW_MAXIMIZE )
		top = Toplevel()
		top.overrideredirect(True)    #忘了
		top.attributes("-alpha", 0.3)    #透明度，讓他有灰灰的感覺
		top.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight())) #跟螢幕一樣大
		top.configure(bg="black")
		root.withdraw()     #暫時隱藏root(主畫面)，不是top-level哦
		cv = Canvas(top) #可以圈出框框的畫布
		win32gui.SetForegroundWindow(top.winfo_id())
		def button_1(event):    #其他我都照抄懶的理解
			global x, y ,xstart,ystart
			global rec
			x, y = event.x, event.y
			xstart,ystart = event.x, event.y
			self.top.set(xstart)      #紀錄點下去那個點
			self.left.set(ystart)    #紀錄點下去那個點
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
			self.bottom.set(xend)  #紀錄釋放的那個點
			self.right.set(yend) #紀錄釋放的那個點
			top.destroy()   #把top-level刪除掉
			root.deiconify()    #恢復root(主視窗)
			

		top.bind("<Button-1>", button_1)  # 滑鼠左鍵點選->顯示子視窗 
		top.bind("<B1-Motion>", b1_Motion)# 滑鼠左鍵移動->改變子視窗大小
		top.bind("<ButtonRelease-1>", buttonRelease_1) # 滑鼠左鍵釋放->記錄最後遊標的位置
	def func(self,event):
		pos =win32gui.GetCursorPos()      
		self.localhwnd=win32gui.WindowFromPoint(pos) #10和11行取得hwnd
		self.hwnd.set(hex(self.localhwnd))  #標籤顯示hwnd
		print(hex(int(self.hwnd.get(),16)))
	def buttonstart(self):
		if self.hwnd.get() == 'hwnd' or self.top.get() == '上' or self.path.get()=='路徑':
			if self.hwnd.get() == 'hwnd':
				messagebox.showinfo("missing input", "請拖曳圖標至視窗取得視窗代碼")
			if self.top.get() == '上':
				messagebox.showinfo("missing input", "請選擇範圍")
			if self.path.get() == '路徑':
				messagebox.showinfo("missing input", "請選擇路徑")
		else:			
			if self.interval.get()=="default is 5 sec":
				interval_variable = 5
			else:
				interval_variable=int(self.interval.get())
			while self.run==True:
				test=project(self.localhwnd,"desktop",int(self.top.get()),int(self.left.get()),int(self.bottom.get()),int(self.right.get()),interval_variable) 
				test.autofetch()  
	def loopstop(self):
		self.run==False
root = Tk()
root.title('OCR')
MainPage(root)
root.mainloop()