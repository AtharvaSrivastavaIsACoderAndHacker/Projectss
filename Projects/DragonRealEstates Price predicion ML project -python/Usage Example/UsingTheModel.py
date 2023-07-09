# Using The Model By The Help Of JOBLIB
from joblib import load
import numpy as np
from os import system

system('cls')


model = load('DragonRealEstates.joblib')


features = np.array([[ -45.90445211 , -0.05682237 , -3.81649658  , 2.53014901  , 0.,
   6.85486499 , 111.56211193  , 58.04465406 , -1.43103098 , -0.46163305,
   0.4667206  ,  1.70753116, -333.48490145  , 1.71779137]])


print(model.predict(features))
