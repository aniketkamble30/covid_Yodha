import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import adjustText as aT
from matplotlib.colors import LinearSegmentedColormap
import math
from datetime import datetime
import os

def make_map():
    
    dt = datetime.now()
    print(dt.month)
    datestring=str(dt.day)+str(dt.month)
    state_list=[]
    folder_path='static/img/plots/'+datestring

    print(folder_path)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        df = pd.read_csv('https://api.covid19india.org/csv/latest/state_wise.csv')
        texts=[]
        cmap = LinearSegmentedColormap.from_list("", ["#09FF00","#FFD900","#FFD900","#FFD900","#FF7B00","#FF7B00","#FF0000","#FF0000"])
        data_for_map = df[['State','Confirmed']]

        fp = "gadm36_IND_1.shp"
        map_df = gpd.read_file(fp)



        map_df["center"] = map_df["geometry"].representative_point()
        za_points = map_df.copy()
        za_points.set_geometry("center", inplace = True)

        merged = map_df.set_index('NAME_1').join(data_for_map.set_index('State'))
        state_list=merged['Confirmed'].tolist()
        state_list = [0 if math.isnan(x) else x for x in state_list]
        state_list=[int(i) for i in state_list]
        state_list = ["" if x==0 else x for x in state_list]
        state_list[5]=""
        state_list[26]=""
        merged.fillna(0, inplace=True)
        fig, ax = plt.subplots(1, figsize=(10, 6))
        ax.axis('off')
        ax.set_title('Cases' , fontdict={'fontsize': '25', 'fontweight' : '3'})
        aT.adjust_text(texts, force_points=0.3, force_text=0.8, expand_points=(1,1), expand_text=(1,1))
        for x, y, label in zip(za_points.geometry.x-0.5, za_points.geometry.y, state_list):
                texts.append(plt.text(x, y, label, fontsize = 8))
        merged.plot(column='Confirmed', cmap=cmap, linewidth=0.8, ax=ax, edgecolor='0.9', legend=True)
        plt.savefig(folder_path+'/india.png')
        
        
        df = pd.read_csv('https://api.covid19india.org/csv/latest/district_wise.csv')
        cmap = LinearSegmentedColormap.from_list("", ["#09FF00","#FFD900","#FFD900","#FFD900","#FF7B00","#FF7B00","#FF0000","#FF0000"])
        
        
        data_for_map = df[['District','Confirmed']]
        data_for_map.loc[338, ['District']]="Mumbai City"
        data_for_map.loc[322, ['District']]="Ahmadnagar"
        data_for_map.loc[331, ['District']]="Garhchiroli"
        data_for_map.loc[332, ['District']]="Gondiya"
        data_for_map.loc[79, ['District']]="Aurangabaaad"
        data_for_map.loc[326, ['District']]="Bid"
        data_for_map.loc[328, ['District']]="Buldana"
        
        data_for_map.loc[339, ['Confirmed']]=data_for_map.loc[338, ['Confirmed']]
        data_for_map.loc[338, ['Confirmed']]=0


        fp = "gadm36_IND_2.shp"
        map_df = gpd.read_file(fp)

        state_list=["Maharashtra","Gujarat","Andhra Pradesh","Arunachal Pradesh","Assam","Bihar","Chhattisgarh","Goa","Haryana","Himachal Pradesh","Jammu and Kashmir","Jharkhand","Karnataka","Kerala","Madhya Pradesh","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Punjab","Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal","Andaman and Nicobar","Chandigarh","Dadra and Nagar Haveli","Daman and Diu","Lakshadweep","NCT of Delhi","Puducherry"]
        for n in range(0,len(state_list)):
            map_df1 = map_df[map_df['NAME_1']==state_list[n]]
            texts=[]
            map_df1["center"] = map_df1["geometry"].representative_point()
            za_points = map_df1.copy()
            za_points.set_geometry("center", inplace = True)
            
            merged = map_df1.set_index('NAME_2').join(data_for_map.set_index('District'))
            
            dist_list=merged['Confirmed'].tolist()
            
            dist_list = [0 if math.isnan(x) else x for x in dist_list]
           
            dist_list=[int(i) for i in dist_list]
            
            merged.fillna(0, inplace=True)
            fig, ax = plt.subplots(1, figsize=(10, 6))
            ax.axis('off')
            ax.set_title('Cases in %s' % state_list[n], fontdict={'fontsize': '25', 'fontweight' : '3'})
            aT.adjust_text(texts, force_points=0.3, force_text=0.8, expand_points=(1,1), expand_text=(1,1))
            for x, y, label in zip(za_points.geometry.x, za_points.geometry.y, dist_list):
                    texts.append(plt.text(x, y, label, fontsize = 8))
                   
            merged.plot(column='Confirmed', cmap=cmap, linewidth=0.8, ax=ax, edgecolor='0.9', legend=True)
            plt.savefig(folder_path+'/%s.png'%state_list[n])
    else:
        print("Plots already exist")

if __name__ == '__main__':      
    make_map()
