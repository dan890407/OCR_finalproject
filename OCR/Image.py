from PIL import Image
import pytesseract
  
img = Image.open('screencapture/1.jpg')
text = pytesseract.image_to_string(img, lang='eng')
print(text)