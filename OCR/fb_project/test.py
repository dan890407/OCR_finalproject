from fbclub_lib import *

test=project(0X580c7e,"test",10,0,304,248,"./text_file/") 
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
    localdic0 = {
        'location': '潭子區',
        'price': '1080',
        'size': '58',
        'age': '26',
        'format': '4/2/3/'
    }
    localdic1 = {
        'location': '北區',
        'price': '498',
        'format': '2/2/1/',
        'size': '21',
        'age': '27'
    }
    localdic2 = {
        'location': '太平區',
        'price': '668',
        'format': '4/2/2/',
        'size': '36',
        'age': '26'
    }
    for i in range(3):
        if first == True:
            print("run!!")
            name1 = 'final31'
            name2 = 'final32'
            for f in os.listdir('../house_web/static/screenshot'):
                if f.startswith(name1):
                    num1 += 1
                if f.startswith(name2):
                    num2 += 1
            first = False
            print(num1,num2)
        if i == 0:
            loaded_model = joblib.load('./house_model/潭子區_model')     #載入模型
            n = 9
            test = np.array([localdic0['age'],localdic0['size'],n])       #屋齡/坪數/間數
        elif i == 1:
            loaded_model = joblib.load('./house_model/北區_model')     #載入模型
            n = 5
            test = np.array([localdic1['age'],localdic1['size'],n])       #屋齡/坪數/間數
        else:
            loaded_model = joblib.load('./house_model/太平區_model')     #載入模型
            n = 8
            test = np.array([localdic2['age'],localdic2['size'],n])       #屋齡/坪數/間數
        test = test.reshape(1,-1)
        poly_reg =PolynomialFeatures(degree=2)
        test_ploy =poly_reg.fit_transform(test)
        pred = loaded_model.predict(test_ploy)
        print(pred)
        if i == 0:
            if int(localdic0['price']) < int(pred)*4:      #價格低於預測標準(目前pred*4)，放入第一優先index
                testall.append(localdic0)
                test1.append(localdic0)
            elif int(localdic0['price']) < int(pred)*7:    #價格低於預測標準(目前pred*7)，放入第二優先index
                testall.append(localdic0)
                test2.append(localdic0)
            else:
                localdic1 = {}
        elif i == 1:
            if int(localdic1['price']) < int(pred)*4:      #價格低於預測標準(目前pred*4)，放入第一優先index
                testall.append(localdic1)
                test1.append(localdic1)
            elif int(localdic1['price']) < int(pred)*7:    #價格低於預測標準(目前pred*7)，放入第二優先index
                testall.append(localdic1)
                test2.append(localdic1)
            else:
                localdic1 = {}
        else:
            if int(localdic2['price']) < int(pred)*4:      #價格低於預測標準(目前pred*4)，放入第一優先index
                testall.append(localdic2)
                test1.append(localdic2)
            elif int(localdic2['price']) < int(pred)*7:    #價格低於預測標準(目前pred*7)，放入第二優先index
                testall.append(localdic2)
                test2.append(localdic2)
            else:
                localdic2 = {}
        print(len(test1),len(test2))
    with open('./123.json',"w",encoding='utf-8') as j:
        json.dump(test1,j,indent=4,ensure_ascii=False)
    with open('./456.json',"w",encoding='utf-8') as j:
        json.dump(test2,j,indent=4,ensure_ascii=False)