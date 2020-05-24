import numpy as np
import pandas as pd
import csv
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import pandas as pd
import matplotlib.pyplot as plt


def current_stats():
    dataset = pd.read_csv('https://api.covid19india.org/csv/latest/case_time_series.csv')
    dataset=dataset.dropna()
    
    
    def listtostr(s):  
        res = str(s)[1:-1]   
        return (float(res))
    
    
    dataset = dataset[-1:]
    
    
    data_list=dataset.iloc[0, :].values
    total=str(data_list[2])
    total_recovered=str(data_list[4])
    total_deaths=str(data_list[6])
    active=str(data_list[2]-data_list[4]-data_list[6])
    new_cases=str(data_list[1])
    new_recoveries=str(data_list[3])
    new_deaths=str(data_list[5])
    
    print("Data for "+data_list[0]+"\n"+"Total cases: "+str(data_list[2])+" Total recoveries: "+str(data_list[4])+" Total deaths: "+str(data_list[6])+"\n"+"New cases: "+str(data_list[1])+" New recoveries: "+str(data_list[3])+ " New deaths: "+str(data_list[5])+"\nActive cases: "+str(data_list[2]-data_list[4]-data_list[6]))
    
    return total, total_recovered, total_deaths, active, new_cases, new_recoveries, new_deaths

current_stats()