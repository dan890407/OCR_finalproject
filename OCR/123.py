from tkinter import *
from tkinter.messagebox import *
import pyautogui
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
		self.createPage()

	
	def createPage(self):
		Button(self,text="+").grid(row=0,stick=W,pady=20)
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
		

	
		Button(self,text="間隔").grid(row=2,column=0,stick=W,pady=3)
		Button(self,text="測試").grid(row=2,column=1,stick=W,pady=3)
		Button(self,text="開始").grid(row=2,column=4,stick=W,pady=3)
		Button(self,text="停止").grid(row=2,column=5,stick=W,pady=3)
	
	def createscreenshot(self):       #建造一個top-level的視窗
		top = Toplevel()
		top.overrideredirect(True)    #忘了
		top.attributes("-alpha", 0.3)    #透明度，讓他有灰灰的感覺
		top.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight())) #跟螢幕一樣大
		top.configure(bg="black")
		root.withdraw()     #暫時隱藏root(主畫面)，不是top-level哦
		cv = Canvas(top) #可以圈出框框的畫布
		
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


root = Tk()
root.title('OCR')
MainPage(root)
root.mainloop()