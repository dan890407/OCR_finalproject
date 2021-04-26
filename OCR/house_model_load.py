import numpy as np
import joblib
from sklearn.preprocessing import  PolynomialFeatures

loaded_model = joblib.load(r'./house_model/南區_model')     #地區
test = np.array([24,60.43,8])       #屋齡/坪數/間數
test = test.reshape(1,-1)
poly_reg =PolynomialFeatures(degree=2)
test_ploy =poly_reg.fit_transform(test)
pred = loaded_model.predict(test_ploy)
print(pred)