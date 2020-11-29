from PIL import Image
import pytesseract
  
img = Image.open('screencapture/2.jpg')
text = pytesseract.image_to_string(img, lang='chi_sim')
print(text)