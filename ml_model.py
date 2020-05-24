import numpy as np
import pandas as pd
import csv
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import pandas as pd

dataset = pd.read_csv('district_timeline.csv')
del dataset['Date']
del dataset['Month']

def listtostr(s):  
    res = str(s)[1:-1]   
    return (res)

def generate_pred(i):
    
        X=[]
        y=[]
        y = dataset.iloc[:, i].values
        for n in range(1,len(y)+1):
            X.append([n])

        poly_reg = PolynomialFeatures(degree = 3)
        X_poly = poly_reg.fit_transform(X)
        poly_reg.fit(X_poly, y)
        lin_reg_2 = LinearRegression()
        lin_reg_2.fit(X_poly, y)
        growth_rate = np.exp(np.diff(np.log(y))) - 1
        str(list(growth_rate).pop()*100)+'%'
        growth_rate=str("{:.1f}".format(list(growth_rate).pop()*100))+' %'
        prediction=lin_reg_2.predict(poly_reg.fit_transform([[len(y)+1]]))
        return prediction,growth_rate

prediction=[]
growth_rate=[]
current=[]
def pred_maha():
    for i in range(0,5):
        pred,grow =generate_pred(i)
        prediction.append(listtostr(pred))
        growth_rate.append(grow)  
    
   
    #for i in range(0,5):
    #   print("Next day prediction for "+dataset.columns[i]+" is "+prediction[i]+" Case growth rate: "+growth_rate[i])
    
    pm=prediction[0]
    pp=prediction[1]
    pt=prediction[2]
    pnag=prediction[3]
    pnas=prediction[4]
    
    gm=growth_rate[0]
    gp=growth_rate[1]
    gt=growth_rate[2]
    gnag=growth_rate[3]
    gnas=growth_rate[4]
    
    return prediction,growth_rate
        
pred_maha()