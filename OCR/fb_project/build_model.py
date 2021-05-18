import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder,OneHotEncoder,StandardScaler,PolynomialFeatures
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error,mean_absolute_error,r2_score
import joblib

dataset = pd.read_csv(r"台中住宅(切割後).csv")

X = dataset.iloc[:,0:5].values      #區域/屋齡/建坪/間數/車位
y = dataset.iloc[:,5].values        #價錢
y = y.reshape(-1,1)

labelencoder_X0 = LabelEncoder()    #將文字轉為數字
labelencoder_X4 = LabelEncoder()
X[:,0] = labelencoder_X0.fit_transform(X[:,0])
X[:,4] = labelencoder_X4.fit_transform(X[:,4])

ct = ColumnTransformer(transformers = [('區域',OneHotEncoder(),[0]),
                                        ('車位',OneHotEncoder(),[4])],
                                        remainder = 'passthrough')    #二元特徵
X = ct.fit_transform(X)
X = X.toarray()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2,random_state=0)   #切割成訓練和測試，80%訓練20%測試

sc_X = StandardScaler()             #資料標準化
X_train = sc_X.fit_transform(X_train)
X_test = sc_X.transform(X_test)

poly_reg =PolynomialFeatures(degree=2)  #二次方程式
X_train =poly_reg.fit_transform(X_train)
regressor = LinearRegression()      #線性回歸
regressor.fit(X_train, y_train)

X_test =poly_reg.fit_transform(X_test)
y_pred = regressor.predict(X_test)      #預測
'''for i  in range(10):
    print(y_pred[(i+1)*200],y_test[(i+1)*200])
print(r2_score(y_test, y_pred))'''

mse_valid = mean_squared_error(y_test, y_pred)      #均方誤差
mae_valid = mean_absolute_error(y_test, y_pred)     #平均絕對誤差

'''print(mse_valid,mae_valid)'''

joblib.dump(labelencoder_X0,'label_location')
joblib.dump(labelencoder_X4,'label_car')
joblib.dump(ct,'columntransformer')
joblib.dump(sc_X,'standardscaler')
joblib.dump(regressor,'house_predict_model')
