from datetime import datetime,timedelta
import os
from map_maker import make_map

def plot_day():
    make_map()
    dt = datetime.now()
    datestring=str(dt.day)+str(dt.month)              #current date
    print(datestring)
    yestdate=dt+timedelta(days=-1)
    yeststring=str(yestdate.day)+str(yestdate.month)  #yesterdays date
    print(yeststring)
    
    day_folder=[]
    st=os.scandir('static/img/plots')
    for fl in st:
        day_folder.append(str(fl)[11:-2])
            
    if datestring in day_folder:
        return datestring
    else:
        return yeststring
    
if __name__ == '__main__':
    plot_day()
    