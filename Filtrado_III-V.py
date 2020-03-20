# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 20:46:37 2020

@author: juanj
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/Datos.csv',encoding= 'unicode_escape')
df=df.set_index(pd.DatetimeIndex(df['Date Time']))
df=df.drop(['Date Time'],axis=1)


###Criterios de filtrado para datos del III-V
###Potencia estimada <0.001 ( un valor tan bajo no aporta información, de hecho puede empeorar el estudio)
###criterios de Marcos, SMR, DNI,AM,viento

filt_df=df[(df['PMP_estimated_IIIV (W)']>0.1)]
filt_df2=filt_df[(df['DII (W/m2)']>100)]
##filt_df=filt_df[(filt_df['aoi']<60.00)]
###En la base de datos estaba con dos espacios"
#filt_df=filt_df[(filt_df['SMR_Top_Mid (n.d.)']!='   NaN')]
#filt_df[['SMR_Top_Mid (n.d.)']] = filt_df[['SMR_Top_Mid (n.d.)']].apply(pd.to_numeric)
#
#filt_df=filt_df[(filt_df['SMR_Top_Mid (n.d.)']<1.10)]
#filt_df=filt_df[(filt_df['SMR_Top_Mid (n.d.)']>0.7)]
#filt_df=filt_df[(filt_df['DII (W/m2)']>600.00)]
#filt_df=filt_df[(filt_df['Wind Speed (m/s)']<10.00)]
#filt_df=filt_df[(filt_df['airmass_relative']<10.00)]
#filt_df=filt_df.set_index(np.arange(0,len(filt_df)))

#'''vemos los datos representados tras el primer filtrado'''
#
#
#'''Este es el código para dibujar la nube de puntos con el filtrado'''
#x=filt_df['aoi']
#y1=filt_df['ISC/DII']
#x_aoi=filt_df['aoi']
#x_temp=filt_df['T_Amb (°C)']
#x_AM=filt_df['airmass_relative']
#
##AOI
#fig, ax=plt.subplots(figsize=(10,7))
#ax.plot(x_aoi,y1,'o',markersize=2)
##plt.ylim(0,0.0015)
#ax.set_xlabel('AOI (°)')
#ax.set_ylabel('ISC_measured_IIIV/DII (A m2/W)')
#ax.set_title("Datos")
#plt.legend()
##T_Amb
#fig, ax=plt.subplots(figsize=(10,7))
#ax.plot(x_temp,y1,'o',markersize=2)
##ax.ylimit(0,0.0015)
#ax.set_xlabel('T_Amb (°C)')
#ax.set_ylabel('ISC_measured_IIIV/DII (A m2/W)')
#ax.set_title("Datos")
#plt.legend()
##airmass_relative
#fig, ax=plt.subplots(figsize=(10,7))
#ax.plot(x_AM,y1,'o',markersize=2)
##ax.ylimit(0,0.0015)
#ax.set_xlabel('airmass_relative')
#ax.set_ylabel('ISC_measured_IIIV/DII (A m2/W)')
#ax.set_title("Datos")
#plt.legend()
#
#'''Hay que mejorar el filtrado'''
#
#
#filt_df=filt_df[(filt_df['ISC/DII']<0.0012)]
#filt_df=filt_df[(filt_df['ISC/DII']>0.0004)]
#media_ISCDII=filt_df['ISC/DII'].mean()
#limit_sup=media_ISCDII+0.0003
#limit_inf=media_ISCDII-0.0003
#filt_df=filt_df[filt_df['ISC/DII']>limit_inf]
#filt_df=filt_df[filt_df['ISC/DII']<limit_sup]
#
#
#
#
#'''Este es el código para dibujar la nube de puntos con el filtrado'''
#x=filt_df['aoi']
#y1=filt_df['ISC/DII']
#x_aoi=filt_df['aoi']
#x_temp=filt_df['T_Amb (°C)']
#x_AM=filt_df['airmass_relative']
#
#
##AOI
#fig, ax=plt.subplots(figsize=(10,7))
#ax.plot(x_aoi,y1,'o',markersize=2)
#ax.set_ylim(0,0.0015)
#ax.set_xlabel('AOI (°)')
#ax.set_ylabel('ISC_measured_IIIV/DII (A m2/W)')
#ax.set_title("Datos")
#plt.legend()
##T_Amb
#fig, ax=plt.subplots(figsize=(10,7))
#ax.plot(x_temp,y1,'o',markersize=2)
#ax.set_ylim(0,0.0015)
#ax.set_xlabel('T_Amb (°C)')
#ax.set_ylabel('ISC_measured_IIIV/DII (A m2/W)')
#ax.set_title("Datos")
#plt.legend()
##airmass_relative
#fig, ax=plt.subplots(figsize=(10,7))
#ax.plot(x_AM,y1,'o',markersize=2)
#ax.set_ylim(0,0.0015)
#ax.set_xlabel('airmass_relative')
#ax.set_ylabel('ISC_measured_IIIV/DII (A m2/W)')
#ax.set_title("Datos")
#plt.legend()
#
#'''Potencias'''
#
#y1=filt_df['PMP_estimated_IIIV (W)']
##y2=filt_df['PMP_estimated_Si (W)']
#x_aoi=filt_df['aoi']
#x_temp=filt_df['T_Amb (°C)']
#x_AM=filt_df['airmass_relative']
#
##Potencia en función del aoi
#fig, ax=plt.subplots(figsize=(10,7))
#ax.plot(x_aoi,y1,'o',markersize=2,label='PMP_estimated_IIIV (W)')
##ax.plot(x_aoi,y2,'o',markersize=2,label='PMP_estimated_Si (W)')
##ax.ylimit(0,0.0015)
#ax.set_xlabel('AOI (°)')
#ax.set_ylabel('Potencia (W)')
#ax.set_title("Potencias en función de AOI")
#plt.legend()
#
#
##Potencia en función de la temp
#fig, ax=plt.subplots(figsize=(10,7))
#ax.plot(x_temp,y1,'o',markersize=2,label='PMP_estimated_IIIV (W)')
##ax.plot(x_temp,y2,'o',markersize=2,label='PMP_estimated_Si (W)')
##ax.ylimit(0,0.0015)
#ax.set_xlabel('Temp (°C)')
#ax.set_ylabel('Potencia (W)')
#ax.set_title("Potencias en función de Temp")
#plt.legend()
#
##Potencia en función del airmass
#fig, ax=plt.subplots(figsize=(10,7))
#ax.plot(x_AM,y1,'o',markersize=2,label='PMP_estimated_IIIV (W)')
##ax.plot(x_AM,y2,'o',markersize=2,label='PMP_estimated_Si (W)')
##ax.ylimit(0,0.0015)
#ax.set_xlabel('Airmass')
#ax.set_ylabel('Potencia (W)')
#ax.set_title("Potencias en función de Airmass")
#plt.legend()
#
