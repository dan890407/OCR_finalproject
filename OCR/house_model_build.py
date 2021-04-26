import numpy as np
import pandas as pd
import joblib  
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import  PolynomialFeatures
from sklearn.linear_model import LinearRegression

dataset = pd.read_csv(r"109年台中房屋買賣.csv")

a = dataset.loc[dataset['地區']=='??區']    #篩選特定區域

X = a[['屋齡','坪數','間數']].values    #間數為房+廳+衛
y = a['總價(萬)'].values
X_train, y_train= X, y

poly_reg =PolynomialFeatures(degree=2)
X_ploy =poly_reg.fit_transform(X_train)
regressor = LinearRegression()
regressor.fit(X_ploy, y_train)

print(regressor.coef_)
print(regressor.intercept_)

joblib.dump(regressor,'??區_model')