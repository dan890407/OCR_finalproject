from fbclub_lib import *

test=project(0Xa005e,"test",415,233,1027,1000,"./text_file/") 
run=False

first = True
num1 = 0
num2 = 0
test1 = []
test2 = []
testall = []

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
    test.jsons_nlp()
    '''test.judge(testall,test1,test2,num1,num2)
    test.makefile(testall,test1,test2)'''