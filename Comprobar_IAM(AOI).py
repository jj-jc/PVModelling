# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 10:45:56 2020

@author: juanj
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import pvlib
import Error as E
df=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/Datos_filtrados.csv',encoding='utf-8')
#se introduce euna columna aue corresponde al index al escribir
df=df.set_index(pd.DatetimeIndex(df['Date Time']))
df=df.drop(['Date Time'],axis=1)
#filtramos el date frame en función del aoi para que las funciones de cálculo del IAM no de valores nan además 
#de que los valores en aois altos no son representativos para el la parte de III-V
df=df[(df['aoi']<55)]

#para verificar los parametros calculados.
P_nor=np.array(df['PMP_estimated_IIIV (W)'])/np.array(df['PMP_estimated_IIIV (W)'].max())
AOI=np.array(df['aoi'])
COS=np.cos(AOI/180*math.pi)

AUX=np.array(P_nor/COS)
y=np.array(pvlib.iam.physical(aoi=AOI, n=0.9000000357627869,K=10.900008201599121, L=0.10000000149011612))
y_ashrae=np.array(pvlib.iam.ashrae(aoi=AOI,b=1.1779999732971191))
y_physical=np.array(pvlib.iam.physical(aoi=AOI, n=0.9000000357627869,K=10.900008201599121, L=0.10000000149011612))

y_Martin=np.array(pvlib.iam.martin_ruiz(aoi=AOI,a_r=3140001.0))


plt.figure(figsize=(30,15))
plt.plot(AOI,AUX,'o',markersize=2,label='IAM(AOI)')
plt.plot(AOI,y_physical,'o',markersize=2,label='funcion_physical')
plt.plot(AOI,y_ashrae,'o',markersize=2,label='ashrae')
plt.plot(AOI,y_Martin,'o',markersize=2,label='Martin')
plt.legend()
plt.show()


print(E.Determination_coefficient(AUX,y_physical))


df=df[(df['T_Amb (°C)']<20)]
df=df[(df['T_Amb (°C)']>15)]

#para verificar los parametros calculados.
P_nor=np.array(df['PMP_estimated_IIIV (W)'])/np.array(df['PMP_estimated_IIIV (W)'].max())
AOI=np.array(df['aoi'])
COS=np.cos(AOI/180*math.pi)

AUX=np.array(P_nor/COS)
y=np.array(pvlib.iam.physical(aoi=AOI, n=0.9000000357627869,K=10.900008201599121, L=0.10000000149011612))
y_ashrae=np.array(pvlib.iam.ashrae(aoi=AOI,b=1.1779999732971191))
y_physical=np.array(pvlib.iam.physical(aoi=AOI, n=0.9000000357627869,K=10.900008201599121, L=0.10000000149011612))

y_Martin=np.array(pvlib.iam.martin_ruiz(aoi=AOI,a_r=3140001.0))


plt.figure(figsize=(30,15))
plt.plot(AOI,AUX,'o',markersize=2,label='IAM(AOI)')
plt.plot(AOI,y_physical,'o',markersize=2,label='funcion_physical')
plt.plot(AOI,y_ashrae,'o',markersize=2,label='ashrae')
plt.plot(AOI,y_Martin,'o',markersize=2,label='Martin')
plt.legend()
plt.show()


print(E.Determination_coefficient(AUX,y_physical))











