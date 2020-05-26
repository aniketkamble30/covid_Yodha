import numpy as np
import pandas as pd
import csv
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import pandas as pd
import matplotlib.pyplot as plt

dataset = pd.read_csv('https://api.covid19india.org/csv/latest/case_time_series.csv')
dataset=dataset.dropna()
# del dataset['Date']
# del dataset['Month']

def listtostr(s):  
    res = str(s)[1:-1]   
    return (float(res))

def india_pred(i):
    
        X=[]
        y=[]
        y = dataset.iloc[:, i].values
        for n in range(1,len(y)+1):
            X.append([n])

        poly_reg = PolynomialFeatures(degree = 4)
        X_poly = poly_reg.fit_transform(X)
        poly_reg.fit(X_poly, y)
        lin_reg_2 = LinearRegression()
        lin_reg_2.fit(X_poly, y)
        growth_rate = np.exp(np.diff(np.log(y))) - 1
        str(list(growth_rate).pop()*100)+'%'
        growth_rate=str("{:.1f}".format(list(growth_rate).pop()*100))+' %'
        prediction=lin_reg_2.predict(poly_reg.fit_transform([[len(y)+1]]))
        
#         plt.scatter(X, y, color = 'red')
#         predline=[]
#         for n in range(0,130):
#             predline.append([n])
#         #predline = predline[40:]    
#         plt.plot(predline, lin_reg_2.predict(poly_reg.fit_transform(predline)), color = 'blue')

#         plt.title(dataset.columns[i])
#         plt.xlabel('Days')
#         plt.ylabel('Cases')
#         plt.show()

        return prediction,growth_rate
    
    
    
# dataset = dataset[:-1]
prediction=[]
growth_rate=[]
current=[]
    
def pred_list():
    cols=[2,4,6]
    
    for i in cols:
        pred,grow =india_pred(i)
        prediction.append(listtostr(pred))
        growth_rate.append(grow)  
    
    #print(prediction)
    #print("Next day prediction for India: \n Cases: "+"{:.2f}".format(prediction[0])+" Recovered: "+"{:.2f}".format(prediction[1])+"Deaths: "+"{:.2f}".format(prediction[2])+" Case growth rate: "+growth_rate[0])
    
    predicted_cases=prediction[0]
    predicted_recover=prediction[1]
    predicted_deaths=prediction[2]
    growth=growth_rate[0]
    
    return predicted_cases, predicted_deaths, predicted_recover,growth
    
    
pred_list()