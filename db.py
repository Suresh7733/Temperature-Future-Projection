from flask import Flask, render_template ,session
import netCDF4 as nc
import pandas as pd
import numpy as np
import os 
from plots import ploter

def result(latitude,longitude):
 historicalData =nc.Dataset("static\\data\\Historical_temperature_data.nc")
 imdData =nc.Dataset("static\\data\\IMD_Temperature_Data.nc")
 futureData1 =nc.Dataset("static\\data\\Future_temperature_data1.nc")
 futureData2 =nc.Dataset("static\\data\\Future_temperature_data2.nc")
 coordinates =[0,0,0,0]
 historicalCordinates =[0,0,0,0]
 def search(data,lat,lon):
    ans =[-1,-1,-1,-1]
    for i in range(0,362): 
        if(data['lat'][i]>=lat):
            j=i
            while(j<362 and data['lat'][j]==lat and data['lon'][j]>=lon):
                if(data['lon'][j]==lon):
                    return [j]
                j+=1
            while(j<362 and data['lat'][j]==lat):
                j+=1 
            k=i-1
            while(k>=0):
              if(data['lon'][k]<lon ):
                   l=k+1
                   while(l<362 and data['lon'][l]<=lon and data['lat'][l]==data['lat'][k]):
                      l+=1
                   while(l<362 and data['lat'][l]==data['lat'][k]):
                       while(j<362):
                             if(data['lon'][j]==data['lon'][k] ):
                               m =j+1
                               while(m<362 and data['lat'][m]==data['lat'][j]):
                                   if(data['lon'][m]==data['lon'][l]):
                                       ans[0]=j
                                       ans[1]=m
                                       ans[2]=k
                                       ans[3]=l
                                       return ans
                                   m+=1
                             j+=1 
                       l+=1      
              k-=1               
    return []



 def bilinearInterpolation(data,cordinates):
    size =len(data['tasmax'])
    array = np.zeros(size,float)
    x  = float(latitude)
    y  = float(longitude)
    x1 = float(data['lat'][cordinates[0]])
    x2 = float(data['lat'][cordinates[1]])
    y1 = float(data['lon'][cordinates[2]])
    y2 = float(data['lon'][cordinates[3]])
    q11= data['tasmax'][:,cordinates[0],cordinates[2]]
    q12=data['tasmax'][:,cordinates[1],cordinates[3]]
    q21=data['tasmax'][:,cordinates[0],cordinates[2]]
    q22=data['tasmax'][:,cordinates[1],cordinates[3]]
    for i in range(0,size):
        Q11 = float(q11[i])
        Q12=float(q12[i])
        Q21=float(q21[i])
        Q22=float(q22[i])
        r1  =(((x2-x)/(x2-x1))*Q11)+(((x-x1)/(x2-x1))*Q21)
        r2  =(((x2-x)/(x2-x1))*Q12)+(((x-x1)/(x2-x1))*Q22)
        p   = (((y2-y)/(y2-y1))*r1)+(((y-y1)/(y2-y1))*r2)
        array[i] =p;
    return array

 def bilinearInterpolationIMD(data,cordinates):
    array = np.zeros(14610,float)
    x =float(latitude)
    y=float(longitude)
    x1=float(data['lat'][cordinates[2]])
    x2=float(data['lat'][cordinates[1]])
    y1=float(data['lon'][cordinates[0]])
    y2=float(data['lon'][cordinates[1]])
    q11=data['tasmax'][cordinates[2],:]
    q12=data['tasmax'][cordinates[3],:]
    q21=data['tasmax'][cordinates[0],:]
    q22=data['tasmax'][cordinates[1],:]
    for i in range(0,14610):
        Q11 = float(q11[i])
        Q12=float(q12[i])
        Q21=float(q21[i])
        Q22=float(q22[i])
        r1 =(((x2-x)/(x2-x1))*Q11)+(((x-x1)/(x2-x1))*Q21)
        r2 =(((x2-x)/(x2-x1))*Q12)+(((x-x1)/(x2-x1))*Q22)
        p = (((y2-y)/(y2-y1))*r1)+(((y-y1)/(y2-y1))*r2)
        array[i] =p;
    return array

 def  coordinate(data,coordinates):
    i=0
    n=len(data['lat'])
    while(i<n):
        if(data['lat'][i]>latitude):
            coordinates[0]=i-1
            coordinates[1]=i
            break
        if(data['lat'][i]==latitude):
            coordinates[0]=i-1
            coordinates[1]=i+1
            break
        i+=1
    n =len(data['lon'])
    i=0
    while(i<n):
        if(data['lon'][i]>longitude):
            coordinates[2]=i-1
            coordinates[3]=i
            break
        if(data['lon'][i]==longitude):
            coordinates[2]=i-1
            coordinates[3]=i+1
            break
        i+=1
            
    return coordinates


 coor =search(imdData,latitude,longitude)
 obsdata = np.zeros(14610,float)
 if(len(coor)==0):
   raise Exception("IMD DATA is not available for provide Latitude and Longitude please try again another Latitude and Longitude")
 elif(len(coor)==1):
    obsdata =imdData['tasmax'][coor[0]][:]
 if(len(coor)==4):
    obsdata=bilinearInterpolationIMD(imdData,coor)
    
 coordinate(historicalData,historicalCordinates)
 coordinate(futureData1,coordinates)
 def conversion(data):
     for i in range(0,len(data)):
         data[i]=data[i]-273
     return data

 historicalarray =conversion(bilinearInterpolation(historicalData, historicalCordinates))
 futurearray1 = conversion(bilinearInterpolation(futureData1,coordinates))
 futurearray2 = conversion(bilinearInterpolation(futureData2,coordinates)[1:])

 date_range = pd.date_range(start='1975-01-01', end='2014-12-31', freq='D')
 temp_df = pd.DataFrame({'temp': historicalarray}, index=date_range)
 historicalMean = temp_df.groupby(temp_df.index.month).mean()['temp']

 date_range = pd.date_range(start='2021-01-01', end='2060-12-31', freq='D')
 temp_df1 = pd.DataFrame({'temp':futurearray1}, index=date_range)
 futuremean1 = temp_df1.groupby(temp_df1.index.month).mean()['temp']

 date_range = pd.date_range(start='2061-01-01', end='2100-12-31', freq='D')
 temp_df2 = pd.DataFrame({'temp':futurearray2}, index=date_range)
 futuremean2 = temp_df2.groupby(temp_df2.index.month).mean()['temp']



 date_range = pd.date_range(start='1975-01-01', end='2014-12-31', freq='D')
 temp_df = pd.DataFrame({'temp': historicalarray}, index=date_range)
 historicalMax = temp_df.groupby(temp_df.index.month).max()['temp']

 date_range = pd.date_range(start='2021-01-01', end='2060-12-31', freq='D')
 temp_df = pd.DataFrame({'temp': futurearray1}, index=date_range)
 FutureMax1 = temp_df.groupby(temp_df.index.month).max()['temp']
 
 date_range = pd.date_range(start='2061-01-01', end='2100-12-31', freq='D')
 temp_df = pd.DataFrame({'temp': futurearray2}, index=date_range)
 FutureMax2 = temp_df.groupby(temp_df.index.month).max()['temp']




 cf1 =[0,0,0,0,0,0,0,0,0,0,0,0]
 cf2 =[0,0,0,0,0,0,0,0,0,0,0,0]
 for i in range(0,12):
    cf1[i] =float(futuremean1.iloc[i])-float(historicalMean.iloc[i])
    cf2[i] =float(futuremean2.iloc[i])-float(historicalMean.iloc[i])

 start_date = '2021-01-01'
 end_date = '2060-12-31'
 dates = pd.date_range(start_date, end_date)
 month_nums = [date.month for date in dates]
 temperature =[]
 for i, month_num in enumerate(month_nums):
    month_factor = cf1[month_num-1]
    temperature.append(obsdata[i] + month_factor)

 start_date = '2061-01-01'
 end_date = '2100-12-31'
 arr =obsdata[0:14609]
 dates2 = pd.date_range(start_date, end_date)
 month_nums = [date.month for date in dates2]
 temperature2 =[]

 for i, month_num in enumerate(month_nums):
    month_factor = cf2[month_num-1]
    temperature2.append(arr[i] + month_factor)
    
 ploter(obsdata,historicalarray,futurearray1,futurearray2,historicalMean,futuremean1,futuremean2,historicalMax,FutureMax1,FutureMax2)
 df = pd.DataFrame({'Date': dates, 'TemperatureData': temperature})
 df2 = pd.DataFrame({'Date': dates2, 'TemperatureData': temperature2})
 csv1_path = 'static\\Future_Temperature_Projection_2021-2060.csv'
 df.to_csv(csv1_path, index=False)
 csv2_path = 'static\\Future_Temperature_Projection_2061-2100.csv'
 df2.to_csv(csv2_path, index=False)
 return csv1_path,csv2_path



