# ## Temperature in degree Celsius,
# ## humidity in fraction of 100%,
# ## global radiation in 100 W/m2,
# ## precipitation amounts in centimeter,
# ## sunshine in hours,
# ## pressure in 1000 hPa

from os import system
system("cls")
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestRegressor

data = pd.read_csv('weather.csv')
data = data.dropna()

y = data['_precipitation'].copy()
x = data.drop('_precipitation', axis=1)

xTrain, xTest =x[:3300],x[3300:]
yTrain, yTest =y[:3300],y[3300:]

model = RandomForestRegressor()
model.fit(xTrain,yTrain)



attributes = ['DATE','MONTH','cloud_cover','humidity','pressure','global_radiation','sunshine','temp_mean','temp_max']
inputAttr = []

for i in attributes:
    inputAttr.append(input(f'{i} : '))

arr = np.array(inputAttr)
arr = np.reshape(arr,(1,-3))
output = model.predict(arr)
prec = round(output[0],2)
system("cls")
print("---------------------------------------------------------------------------------")
print(f"| Predicted Rainfall According To The Weather Conditions Specified Is : {prec} cm |")
print("---------------------------------------------------------------------------------")