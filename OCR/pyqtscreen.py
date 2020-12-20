from PyQt5.QtWidgets import QApplication
from selenium.webdriver.chrome.options import Options
from PyQt5.QtGui import *
import win32gui
import sys
import time
from PIL import Image
import pytesseract
from selenium import webdriver

options = Options()
options.add_argument("--start-maximized")
driver =webdriver.Chrome(chrome_options=options)
driver.get('https://www.google.com.tw/')
time.sleep(10)
hwnd = win32gui.GetForegroundWindow()
print(hex(hwnd))
app = QApplication(sys.argv)
screen = QApplication.primaryScreen()
img = screen.grabWindow(hwnd).toImage()

img.save("./screencapture/screenshot.jpg")
time.sleep(0.5)


mg = Image.open('./screencapture/screenshot.jpg')
new_mg = mg.crop((520, 80, 1920, 870))
new_mg.save('./screencapture/screenshot2.jpg') 
mcg = Image.open('./screencapture/screenshot2.jpg')
text = pytesseract.image_to_string(mcg, lang='chi_tra+eng+equ')
print(text)