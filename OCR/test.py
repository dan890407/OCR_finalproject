from ocr_lib import *

test=project(0X03B0B98,"desktop",500,251,1000,889,10) 
run=True

while(run):
    test.autofetch()    
    time.sleep(test.interval) 