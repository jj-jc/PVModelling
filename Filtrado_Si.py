# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 20:46:59 2020

@author: juanj
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pvlib
import Error 
import matplotlib.colors 
import matplotlib.cm
#Datos del módulo CPV
#localización
lat=40.453
lon=-3.727
alt=667
tz='Europe/Berlin'
#orientación
surface_tilt=30
surface_azimuth=180
#localizamos el sistema
#ponemos el limite de nuestro módulo
AOILimit=55




df=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/Entradas.csv')
Fecha=pd.DatetimeIndex(df['Date Time'])
df=df.set_index(Fecha)
df=df.drop(['Date Time'],axis=1)
###Criterios de filtrado para datos del III-V
###Potencia estimada <0.001 ( un valor tan bajo no aporta información, de hecho puede empeorar el estudio)
###criterios de Marcos, SMR, DNI,AM,viento
CPV_location=pvlib.location.Location(latitude=lat,longitude=lon,tz=tz,altitude=alt)
Solar_position=CPV_location.get_solarposition(Fecha, pressure=None, temperature=df['T_Amb (°C)'])
filt_df=df
Irradiancias=CPV_location.get_clearsky(times=Fecha, model='ineichen', solar_position=Solar_position, dni_extra=None)


date=np.array(['2019-05-30'])
for i in range(0,len(filt_df.index[:])):
    if(i==0):
        date[0]=str(filt_df.index[0].date())
    elif(filt_df.index[i-1].date()!=filt_df.index[i].date()):
        date=np.append(date,str(filt_df.index[i].date()))




#para limipar los valores de DNI para tener un día claro
#
#for i in filt_df.index[:]:
#    Cambio=filt_df.loc[i]['DNI (W/m2)']-Irradiancias.loc[i]['dni']
#    if Cambio<=0:
#        filt_df=filt_df.drop(i,axis=0)
#        



Solar_position=CPV_location.get_solarposition(filt_df.index[:], pressure=None, temperature=filt_df['T_Amb (°C)'])

POA=pvlib.irradiance.get_total_irradiance(surface_tilt=surface_tilt, surface_azimuth=surface_azimuth,
                                          solar_zenith=Solar_position['zenith'], solar_azimuth=Solar_position['azimuth'], 
                                          dni=filt_df['DNI (W/m2)'], ghi=filt_df['GHI (W/m2)'], dhi=filt_df['DHI (W/m2)'],
                                          dni_extra=None, airmass=None, albedo=0.25, surface_type=None, model='isotropic', 
                                          model_perez='allsitescomposite1990')

filt_df['DII (W/m2)']=POA['poa_direct']
filt_df['GII (W/m2)']=POA['poa_global']
filt_df['Difusa (W/m2)']=POA['poa_diffuse']

filt_df2=filt_df[(filt_df['aoi']<=AOILimit)]
filt_df2['ISC_Si/Difusa (A m2/W)']=filt_df['ISC_measured_Si (A)']/filt_df['Difusa (W/m2)']
filt_df3=filt_df[(filt_df['aoi']>AOILimit)]
filt_df3['ISC_Si/GII (A m2/W)']=filt_df['ISC_measured_Si (A)']/filt_df['GII (W/m2)']
filt_df=pd.concat([filt_df2,filt_df3], axis=0)
filt_df=filt_df.sort_index()





x=filt_df['aoi']
y1=filt_df['ISC_Si/Difusa (A m2/W)']
y2=filt_df['ISC_Si/GII (A m2/W)']

x_aoi=filt_df['aoi']
x_temp=filt_df['T_Amb (°C)']
x_AM=filt_df['airmass_relative']

fig, ax=plt.subplots(figsize=(30,15))
#ax.plot(filt_df['aoi'],filt_df['ISC_IIIV/DII (A m2/W)'],'o',markersize=3)
ax.plot(x_aoi,filt_df['PMP_estimated_IIIV (W)'],'o',markersize=2)
ax.plot(x_aoi,filt_df['ISC_measured_Si (A)'],'o',markersize=2)
#plt.ylim(0,0.025)
ax.set_xlabel('AOI (°)')
ax.set_ylabel('ISC_measured_Si (A)')
ax.set_title("Datos")
plt.legend()


#AOI
fig, ax=plt.subplots(figsize=(30,15))
#ax.plot(filt_df['aoi'],filt_df['ISC_IIIV/DII (A m2/W)'],'o',markersize=3)
ax.plot(x_aoi,y1,'o',markersize=2)
ax.plot(x_aoi,y2,'o',markersize=2)
#plt.ylim(0,0.025)
ax.set_xlabel('AOI (°)')
ax.set_ylabel('ISC_measured_IIIV/DII (A m2/W)')
ax.set_title("Datos")
plt.legend()
#T_Amb
fig, ax=plt.subplots(figsize=(30,15))
ax.plot(x_temp,y1,'o',markersize=2)
#plt.ylim(0,0.0015)
ax.set_xlabel('T_Amb (°C)')
ax.set_ylabel('ISC_measured_IIIV/DII (A m2/W)')
ax.set_title("Datos")
plt.legend()
#airmass_relative
fig, ax=plt.subplots(figsize=(30,15))
ax.plot(x_AM,y1,'o',markersize=2)
#plt.ylim(0,0.0015)
ax.set_xlabel('airmass_relative')
ax.set_ylabel('ISC_measured_IIIV/DII (A m2/W)')
ax.set_title("Datos")
plt.legend()
















#
#
#
#
#
#
#date=np.array(['2019-05-30'])
#for i in range(0,len(filt_df.index[:])):
#    if(i==0):
#        date[0]=str(filt_df.index[0].date())
#    elif(filt_df.index[i-1].date()!=filt_df.index[i].date()):
#        date=np.append(date,str(filt_df.index[i].date()))
#for i in date:
#    fig=plt.figure(figsize=(30,15))
#    fig.add_subplot(121)
#    plt.plot(filt_df[i].index[:].time,filt_df[i]['GII-DII'],label='GII-DII')    
##    plt.plot(df[i].index[:].time,df[i]['GNI (W/m2)'],label='GHI')
##    plt.plot(df[i].index[:].time,df[i]['GII-DII'],label='GII-DII')
##    plt.plot(df[i].index[:].time,df[i]['GII (W/m2)'],label='GII')
#
#    plt.xlabel('Hora')
#    plt.ylabel('Irradiancia (W/m2)')
#    plt.legend()
#    plt.title("Datos de irradiancias "+ str(i))
#    fig.add_subplot(122)
#    plt.plot(filt_df[i].index[:].time,filt_df[i]['Difusa'], label='Difusa')    
##    plt.plot(filt_df[i].index[:].time,filt_df[i]['GNI (W/m2)'],label='GHI')
#    plt.plot(filt_df[i].index[:].time,filt_df[i]['GII-DII'],label='GII-DII')
##    plt.plot(filt_df[i].index[:].time,filt_df[i]['GII (W/m2)'],label='GII')
#    plt.xlabel('Hora')
#    plt.ylabel('Irradiancia (W/m2)')
#    plt.legend()
#    plt.title("Datos de irradiancias filtrados "+str(i))
#
#
#
#
#
#

