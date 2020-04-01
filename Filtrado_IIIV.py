# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 10:30:55 2020

@author: juanj
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/Datos.csv')
df=df.set_index(pd.DatetimeIndex(df['Date Time']))
df=df.drop(['Date Time'],axis=1)
###Criterios de filtrado para datos del III-V
###Potencia estimada <0.001 ( un valor tan bajo no aporta información, de hecho puede empeorar el estudio)
###criterios de Marcos, SMR, DNI,AM,viento

df=df[(df['PMP_estimated_IIIV (W)']>0.1)]
df=df[(df['DII (W/m2)']>100)]
df=df[(df['T_Amb (°C)']>10)]


'''Calular media por horas de todos los dias'''

AUX=pd.DataFrame(df['DII (W/m2)'])
AUX.insert(0,'Horas',AUX.index.hour)
AUX=pd.DataFrame(AUX.groupby(['Horas']))
AUX=AUX.rename(columns={0: 'Horas',1:'Grupo'})
AUX=AUX.set_index(AUX['Horas'])
AUX=AUX.drop(['Horas'],axis=1)
Media_DII=pd.DataFrame({'Medias':AUX.index},index=AUX.index)
for i in range(len(AUX.index)):
    Media_DII.iloc[i]['Medias']=AUX.iloc[i]['Grupo']['DII (W/m2)'].mean()



filt_df2=df





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

#este es el cógido para encontrar las fechas de los datos, por lo que tiene que estar después del filtrado
date=np.array(['2019-05-30'])
for i in range(len(df.index[:])):
    if(i==0):
        date[0]=str(df.index[0].date())
    elif(df.index[i-1].date()!=df.index[i].date()):
        date=np.append(date,str(df.index[i].date()))


#fig=plt.figure(figsize=(20,15))    
#for i in date:
#    plt.plot(df[i].index[:].time,df[i]['aoi'], label='Fecha:'+i)
#plt.xlabel('Hora')
#plt.ylabel('aoi (°)')
#plt.legend()
#plt.title("Ángulo de incidencia")
#
#fig=plt.figure(figsize=(20,15))    
#for i in date:
#    plt.plot(df[i].index[:].time,df[i]['airmass_relative'], label='Fecha:'+i)
#plt.xlabel('Hora')
#plt.ylabel('')
#plt.legend()
#plt.title("Masa de aire relativa")
#
#fig=plt.figure(figsize=(20,15))    
#for i in date:
#    plt.plot(df[i].index[:].time,df[i]['T_Amb (°C)'], label='Fecha:'+i)
#plt.xlabel('Hora')
#plt.ylabel('Temperatura (°C)')
#plt.legend()
#plt.title("Temperatura ambiente")
#
#fig=plt.figure(figsize=(20,15))    
#for i in date:
#    plt.plot(df[i].index[:].time,df[i]['DII (W/m2)'], label='Fecha:'+i)
#plt.xlabel('Hora')
#plt.ylabel('Irradiancia (W/m2)')
#plt.legend()
#plt.title("Irradiancia directa sobre plano inclinado")



ErrorPercent=20
#para limipar los valores de DII
filt_df3=filt_df2
for i in range(0,len(filt_df2.index[:])):
    H=filt_df2.index[i].hour
    Media_Hora=Media_DII.loc[H]['Medias']
    Cambio=abs(filt_df2.iloc[i]['DII (W/m2)']-Media_Hora)
    Margen=(ErrorPercent/100)*(Media_Hora)
    if Cambio>Margen:
        filt_df3=filt_df3.drop(filt_df2.index[i],axis=0)
        AUX.loc[H]['Grupo']=AUX.loc[H]['Grupo'].drop(filt_df2.index[i],axis=0)
        Media_DII.loc[H]['Medias']=AUX.loc[H]['Grupo']['DII (W/m2)'].mean()
        
        
    


for i in date:
    fig=plt.figure(figsize=(20,15))
    plt.plot(df[i].index[:].time,df[i]['DII (W/m2)'], label='Fecha:'+i)
    plt.plot(filt_df3[i].index[:].time,filt_df3[i]['DII (W/m2)'], label='Fecha:'+i)
    
    plt.xlabel('Hora')
    plt.ylabel('Irradiancia (W/m2)')
    plt.legend()
    plt.title("Irradiancia directa sobre plano inclinado")
    
fig=plt.figure(figsize=(20,15))
plt.plot(Media_DII.index,Media_DII['Medias'])
plt.xlabel('Hora')
plt.ylabel('Irradiancia (W/m2)')
plt.title("Media de irradiancia directa por horas")


'''Este es el código para dibujar la nube de puntos con el filtrado'''
x=filt_df3['aoi']
y1=filt_df3['ISC_IIIV/DII (A m2/W)']
x_aoi=filt_df3['aoi']
x_temp=filt_df3['T_Amb (°C)']
x_AM=filt_df3['airmass_relative']

#AOI
fig, ax=plt.subplots(figsize=(20,15))
ax.plot(x_aoi,y1,'o',markersize=2)
#plt.ylim(0,0.0015)
ax.set_xlabel('AOI (°)')
ax.set_ylabel('ISC_measured_IIIV/DII (A m2/W)')
ax.set_title("Datos")
plt.legend()
#T_Amb
fig, ax=plt.subplots(figsize=(20,15))
ax.plot(x_temp,y1,'o',markersize=2)
#ax.ylimit(0,0.0015)
ax.set_xlabel('T_Amb (°C)')
ax.set_ylabel('ISC_measured_IIIV/DII (A m2/W)')
ax.set_title("Datos")
plt.legend()
#airmass_relative
fig, ax=plt.subplots(figsize=(20,15))
ax.plot(x_AM,y1,'o',markersize=2)
#ax.ylimit(0,0.0015)
ax.set_xlabel('airmass_relative')
ax.set_ylabel('ISC_measured_IIIV/DII (A m2/W)')
ax.set_title("Datos")
plt.legend()


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