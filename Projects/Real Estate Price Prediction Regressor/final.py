import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
from os import system
system('cls')


data = pd.read_csv('Real estate.csv')
data = data.drop('No',axis=1)
data = data.dropna()


y = data['priceUnitArea'].copy()
x = data.drop('priceUnitArea', axis=1)


xTrain, xTest =x[:340],x[340:]
yTrain, yTest =y[:340],y[340:]


from sklearn.ensemble import RandomForestRegressor
model = RandomForestRegressor()
model.fit(xTrain,yTrain)


yPredicted = model.predict(xTest)
MSE = mean_squared_error(yTest,yPredicted)









print('USAGE')

attributes = ['transaction date','age','distanceNearestMRT','convenienceStores','latitude','longitude']
inputAttr = []

for i in attributes:
    inputAttr.append(input(f'{i} : '))

arr = np.array(inputAttr)
arr = np.reshape(arr,(1,-3))
output = model.predict(arr)

system('cls')
print("MSE : ",MSE)
print(output)