import pandas as pd
from sklearn.linear_model import SGDRegressor
from sklearn.metrics import mean_squared_error

data = pd.read_csv('cars.csv')
data = data.dropna()


transmission_encoded = pd.get_dummies(data['Transmission'])
fuel_type_encoded = pd.get_dummies(data['Fuel_Type'])
location_encoded = pd.get_dummies(data['Location'])
df_encoded = pd.concat([data, transmission_encoded, fuel_type_encoded,location_encoded], axis=1)
df_encoded.drop(['Transmission', 'Fuel_Type'], axis=1, inplace=True)
df_encoded['Mileage'] = df_encoded['Mileage'].str.replace(' kmpl', '').astype(float)
df_encoded['Engine'] = df_encoded['Engine'].str.replace(' CC', '').astype(float)
df_encoded['Power'] = df_encoded['Power'].str.replace(' bhp', '').astype(float)

y = df_encoded['Price'].copy()
x = df_encoded.drop(['Name','Price','New_Price', 'S.No.','Owner_Type','Location'], axis=1)

xTrain, xTest =x[:700],x[700:]
yTrain, yTest =y[:700],y[700:]

model = SGDRegressor()
model.fit(xTrain,yTrain)

yPredicted = model.predict(xTest)
print("MSE : ",mean_squared_error(yTest,yPredicted))