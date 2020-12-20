from PyQt5.QtWidgets import QApplication
<<<<<<< HEAD
=======
from selenium.webdriver.chrome.options import Options
>>>>>>> fa614abbc630b47cafaf508047cba9fb9b231520
from PyQt5.QtGui import *
import win32gui
import sys
import time
from PIL import Image
import pytesseract
<<<<<<< HEAD

hwnd = win32gui.FindWindow(None,"LINE")
=======
from selenium import webdriver

options = Options()
options.add_argument("--start-maximized")
driver =webdriver.Chrome(chrome_options=options)
driver.get('https://www.google.com.tw/')
time.sleep(10)
hwnd = win32gui.GetForegroundWindow()
print(hex(hwnd))
>>>>>>> fa614abbc630b47cafaf508047cba9fb9b231520
app = QApplication(sys.argv)
screen = QApplication.primaryScreen()
img = screen.grabWindow(hwnd).toImage()

<<<<<<< HEAD
img.save("./OCR/screencapture/screenshot.jpg")
time.sleep(0.5)


mg = Image.open('./OCR/screencapture/screenshot.jpg')
new_mg = mg.crop((480, 100, 1920, 900))
new_mg.save('./OCR/screencapture/screenshot2.jpg') 
mcg = Image.open('./OCR/screencapture/screenshot2.jpg')
text = pytesseract.image_to_string(mcg, lang='chi_tra')
=======
img.save("./screencapture/screenshot.jpg")
time.sleep(0.5)


mg = Image.open('./screencapture/screenshot.jpg')
new_mg = mg.crop((520, 80, 1920, 870))
new_mg.save('./screencapture/screenshot2.jpg') 
mcg = Image.open('./screencapture/screenshot2.jpg')
text = pytesseract.image_to_string(mcg, lang='chi_tra+eng+equ')
>>>>>>> fa614abbc630b47cafaf508047cba9fb9b231520
print(text)