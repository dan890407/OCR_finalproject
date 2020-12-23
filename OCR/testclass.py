from ocr_lib2 import *

test=project("Chrome_WidgetWin_1","【#狗屎寫手】謝忻會來亂談什麼話題呢？ - YouTube - Google Chrome","youtube",1384,251,1789,889) 
run=True

test.autofetch()    
test.merge('./text_file/text','./text_file/all_text')
time.sleep(2)

    