# INITIALISATION
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import cross_val_score
from joblib import dump,load



# STARTING
housing = pd.read_csv('Boston.csv')
# print(housing.head())
# print(housing.info())
# print(housing.describe())






# TRAIN TEST SPLITTING

split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
for train_index, test_index in split.split(housing, housing["chas"]):
    strat_train_set = housing.loc[train_index]
    strat_test_set = housing.loc[test_index]
    
housing = strat_train_set




# CO-RELATIONS

corr_matrix = housing.corr()
corr_matrix['medv'].sort_values(ascending=False)

housing1 = strat_train_set.drop('medv',axis=1)
housing_labels = strat_train_set['medv'].copy()




# ATTRIBUTE COMBINATIONS

housing['taxrm'] = housing['tax']/housing['rm']
print(housing)





# MISSING ATTRIBUTES
from sklearn.impute import SimpleImputer
imputer = SimpleImputer(strategy='median')
imputer.fit(housing1)

x = imputer.transform(housing1)
hrTemp = pd.DataFrame(x,columns=housing1.columns)






# PIPELINE

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

myPipe = Pipeline([
    ('imputer',SimpleImputer(strategy='median')),
    ('std',StandardScaler()),
])

hr = myPipe.fit_transform(hrTemp)






# SELECTING MODEL

model = RandomForestRegressor()
model.fit(hr,housing_labels)




# PRE-EVALUATION TESTING
someLabels = housing_labels.iloc[:5]
someData = housing1.iloc[:5]

finalData = myPipe.fit_transform(someData)
model.predict(finalData)
print(list(someLabels))






# EVALUATING THE MODEL

predictions = model.predict(hr)
MSE = mean_squared_error(housing_labels,predictions)
rmse = np.sqrt(MSE)

print(MSE)





# CROSS-VALIDATION

scores = cross_val_score(model,hr,housing_labels, scoring='neg_mean_squared_error',cv=10)
rmseScores = np.sqrt(-scores)

def eval (scores):
    print('-------------------------------')
    print('Scores : ',scores)
    print('-------------------------------')
    print('Mean : ', scores.mean())
    print('-------------------------------')
    print('STD : ', scores.std())
    print('-------------------------------')
    print('RMSE : ',rmseScores)
    print('-------------------------------')

    
eval(rmseScores)





# SAVING THE MODEL

dump(model,'DragonRealEstates.joblib')







# TESTING THE MODEL ON TEST DATA

test = strat_test_set.drop('medv',axis=1)
testt = strat_test_set['medv'].copy()
finalPrepared = myPipe.transform(test)
finalPredictions = model.predict(finalPrepared)
finalMSE = mean_squared_error(testt,finalPredictions)
finalRMSE = np.sqrt(finalMSE)
results = list(finalPredictions)

print(finalRMSE)
for i,re in enumerate(results):
    print(f'{i}. ', re)
    
    
print(finalPrepared[5])
