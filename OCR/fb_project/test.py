from fbclub_lib import *

test=project(0Xb7080e,"test",425,236,1027,899,"./text_file/") 
run=False

test1 = []
test2 = []
testall = []
first = True
if first == True:
    num1 = 0
    num2 = 0
    for f in os.listdir('../house_web/static/screenshot'):
        if f.startswith('test1'):
            num1 = num1 + 1
        elif f.startswith('test2'):
            num2 = num2 + 1
    first = False
if run == True:
    for i in range(3):
        test.web_screenshot()
        test.divid()
        test.ocr()
        test.cut_word()
        test.judge(testall,test1,test2,num1,num2)
        time.sleep(6)
else:
    test.web_screenshot()
    test.divid()
    test.ocr()
    test.cut_word()
    test.judge(testall,test1,test2,num1,num2)