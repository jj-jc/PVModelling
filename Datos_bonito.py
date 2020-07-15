# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 09:09:46 2020

@author: juanjo
"""

import pandas as pd
import matplotlib.pyplot as plt
import pvlib 
<<<<<<< HEAD

=======
import numpy as np
>>>>>>> 44dd62b3a9cabcb24671889f2522ef353a3f5cc1
pd.plotting.register_matplotlib_converters()#ESTA SENTENCIA ES NECESARIA PARA DIBUJAR DATE.TIMES


df=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/InsolightMay2019.csv',encoding= 'unicode_escape')


#Datos del módulo
#localización
lat=40.453
lon=-3.727
alt=667
tz='Europe/Berlin'
#orientación
surface_tilt=30
surface_azimuth=180


# se localiza el sistema
CPV_location=pvlib.location.Location(latitude=lat,longitude=lon,tz=tz,altitude=alt)

#Se crea un DatetimeIndex para indexar posteriormente el dataFrame
Fecha=pd.DatetimeIndex(df['Date Time'],tz=tz)

Solar_position=CPV_location.get_solarposition(Fecha, pressure=None, 
                                              temperature=df['T_Amb (°C)'])

AOI=pd.DataFrame(pvlib.irradiance.aoi(surface_tilt=surface_tilt, surface_azimuth=surface_azimuth, 
                                      solar_zenith=Solar_position['zenith'], solar_azimuth=Solar_position['azimuth']))

AM=CPV_location.get_airmass(times=Fecha, solar_position=Solar_position,model='simple')

# Se introducen las entradas al DataFrame
AM=AM.set_index([pd.Series(df.index)])
AOI=AOI.set_index([pd.Series(df.index)])
df=pd.concat([df,AM['airmass_relative'],AOI],axis=1)
df=df.set_index(Fecha)
df=df.drop(['Date Time'],axis=1)

AOI_projection=pvlib.irradiance.aoi_projection(surface_tilt=surface_tilt, surface_azimuth=surface_azimuth, 
                                     solar_zenith=Solar_position['zenith'], 
                                     solar_azimuth=Solar_position['azimuth'])

df['DII']=AOI_projection*df['DNI (W/m2)']
df['GII']=AOI_projection*df['GNI (W/m2)']

#almaceno los datos en otro excel
df.to_csv("C://Users/juanj/OneDrive/Escritorio/TFG/Entradas.csv")

fig=plt.figure(figsize=(30,20))
plt.plot(df['aoi'],df['DNI (W/m2)'],'o',markersize='2',label='DNI')   
plt.plot(df['aoi'],df['DII (W/m2)'],'o',markersize='4',label='DII_datos') 
plt.plot(df['aoi'],df['DII'],'o',markersize='2',label='DII')   
plt.xlabel('Hora')
plt.ylabel('Irradiancia (W/m2)')
plt.legend()

fig=plt.figure(figsize=(30,20))
plt.plot(df['aoi'],df['GNI (W/m2)'],'o',markersize='2',label='GNI')   
plt.plot(df['aoi'],df['GII (W/m2)'],'o',markersize='4',label='GII_datos') 
plt.plot(df['aoi'],df['GII'],'o',markersize='2',label='GII')   
plt.xlabel('Hora')
plt.ylabel('Irradiancia (W/m2)')
plt.legend()


#%% PARA OBSERVAR LA DIFERENCIA LAS COMPONENTES DE LAS IRRADIANCIAS
# date=np.array(['2019-05-30'])
# for i in range(0,len(df.index.values)):
#     if(i==0):
#         date[0]=str(df.index[0].date())
#     elif(df.index[i-1].date()!=df.index[i].date()):
#         date=np.append(date,str(df.index[i].date()))
     
# #Para visualizar los datos
# pd.plotting.register_matplotlib_converters()#ESTA SENTENCIA ES NECESARIA PARA DIBUJAR DATE.TIMES
# for i in date:
#     fig=plt.figure(figsize=(30,20))
#     plt.plot(df[str(i)].index[:].time,df[str(i)]['DNI (W/m2)'], label='DNI')    
#     plt.plot(df[str(i)].index[:].time,df[str(i)]['GNI (W/m2)'],label='GNI')
#     plt.plot(df[str(i)].index[:].time,df[str(i)]['DII (W/m2)'],label='DII')
#     plt.plot(df[str(i)].index[:].time,df[str(i)]['GII (W/m2)'],label='GII')
#     plt.xlabel('Hora')
#     plt.ylabel('Irradiancia (W/m2)')
#     plt.legend()
#     plt.title("Datos de irradiancias "+str(i))




#%%
date='2019-06-01'
fig=plt.figure(figsize=(15,10))
plt.plot(df[str(date)].index[:].time,df[str(date)]['PMP_estimated_IIIV (W)'], label='III-V')    
plt.plot(df[str(date)].index[:].time,df[str(date)]['PMP_estimated_Si (W)'],label='Si')
plt.xlabel('Hora',fontsize=15)
plt.ylabel('Potencia (W)',fontsize=15)
plt.legend()
plt.title("Datos de potencias "+str(date),fontsize=20)

fig=plt.figure(figsize=(15,10))
plt.plot(df[str(date)].index[:].time,df[str(date)]['ISC_measured_IIIV (A)'], label='III-V')    
plt.plot(df[str(date)].index[:].time,df[str(date)]['ISC_measured_Si (A)'],label='Si')
plt.xlabel('Hora',fontsize=15)
plt.ylabel('Intensidad (A)',fontsize=15)
plt.legend()
plt.title("Datos de intensidades "+str(date),fontsize=20)







