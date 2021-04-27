from final import *

test=project(0X402ec,"test",402,348,1027,969,"./text_file/") 
run=True

test1 = []
test2 = []
testall = []
if run == True:
    for i in range(3):
        test.web_screenshot()
        test.divid()
        test.ocr()
        test.cut_word()
        test.judge(testall,test1,test2)
        time.sleep(3)
    test.makefile(testall,test1,test2)
else:
    test.web_screenshot()
    test.divid()
    test.ocr()
    test.cut_word()
    test.judge(testall,test1,test2)
    test.makefile(testall,test1,test2)