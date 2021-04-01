from gui_lib import *
from fbclub_lib import *

test=project(0X180926,"test",304,364,1044,943) 
run=False

if run == True:
    while(run):
        test.autofetch() 
        time.sleep(5) 
else:
    test.web_screenshot()
    test.divid()