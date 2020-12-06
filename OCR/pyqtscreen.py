from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import *
import win32gui
import sys
import time
from PIL import Image
import pytesseract

hwnd = win32gui.FindWindow(None,"LINE")
app = QApplication(sys.argv)
screen = QApplication.primaryScreen()
img = screen.grabWindow(hwnd).toImage()

img.save("./OCR/screencapture/screenshot.jpg")
time.sleep(0.5)


mg = Image.open('./OCR/screencapture/screenshot.jpg')
new_mg = mg.crop((480, 100, 1920, 900))
new_mg.save('./OCR/screencapture/screenshot2.jpg') 
mcg = Image.open('./OCR/screencapture/screenshot2.jpg')
text = pytesseract.image_to_string(mcg, lang='chi_tra')
print(text)