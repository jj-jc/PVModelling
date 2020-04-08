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
import IAM_ashrae
import IAM_pysical_bruto
df=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/Datos_filtrados.csv',encoding='utf-8')
#se introduce euna columna aue corresponde al index al escribir
df=df.set_index(pd.DatetimeIndex(df['Date Time']))
df=df.drop(['Date Time'],axis=1)
#filtramos el date frame en función del aoi para que las funciones de cálculo del IAM no de valores nan además 
#de que los valores en aois altos no son representativos para el la parte de III-V
df=df[(df['aoi']<55)]

#para verificar los parametros calculados.
P_nor=np.array(df['PMP_estimated_IIIV (W)'])/np.array(df['PMP_estimated_IIIV (W)'].max())

COS=np.cos(df['aoi']/180*math.pi)

df['P_nor']=np.array(P_nor/COS)
y=np.array(pvlib.iam.physical(aoi=df['aoi'], n=0.9000000357627869,K=10.900008201599121, L=0.10000000149011612))
y_ashrae=np.array(pvlib.iam.ashrae(aoi=df['aoi'],b=1.1779999732971191))
y_physical=np.array(pvlib.iam.physical(aoi=df['aoi'], n=0.9000000357627869,K=10.900008201599121, L=0.10000000149011612))

y_Martin=np.array(pvlib.iam.martin_ruiz(aoi=df['aoi'],a_r=3140001.0))


plt.figure(figsize=(30,15))
plt.plot(df['aoi'],df['P_nor'],'o',markersize=2,label='IAM(AOI)')
plt.plot(df['aoi'],y_physical,'o',markersize=2,label='funcion_physical')
plt.plot(df['aoi'],y_ashrae,'o',markersize=2,label='ashrae')
plt.plot(df['aoi'],y_Martin,'o',markersize=2,label='Martin')
plt.legend()
plt.show()


print(E.Determination_coefficient(df['P_nor'],y_physical))
print(E.Determination_coefficient(df['P_nor'],y_ashrae))



limSup=df['T_Amb (°C)'].max()
limInf=df['T_Amb (°C)'].min()
Rango=limSup-limInf
n_intervalos=5
porcent_mediana=20
incremento=Rango/n_intervalos

for i in range(n_intervalos):
    lim_inf=limInf+i*incremento
    lim_sup=limInf+incremento*(1+i)
    AUX=df[df['T_Amb (°C)']>lim_inf]
    AUX=AUX[AUX['T_Amb (°C)']<=lim_sup]
    RR_ashrae,b=IAM_ashrae.regresion_ashrae(AUX['aoi'],AUX['P_nor'])
    RR_physical,n,k,l =IAM_pysical_bruto.regresion_pysical(AUX['aoi'],AUX['P_nor'])
    y_ashrae=np.array(pvlib.iam.ashrae(aoi=AUX['aoi'],b=b))
    y_pysical=np.array(pvlib.iam.physical(aoi=np.array(AUX['aoi']),n=n,K=k,L=l))
    plt.figure(figsize=(30,15))
    plt.plot(df['aoi'],df['P_nor'],'o',markersize=2,label='todos los datos')
    plt.plot(AUX['aoi'],AUX['P_nor'],'o',markersize=2,label='datos estudiados')
    plt.plot(AUX['aoi'],y_ashrae,'o',markersize=2,label='regresión por ashrae')
    plt.plot(AUX['aoi'],y_pysical,'o',markersize=2,label='regresión por pysical')
    plt.xlabel('Ángulo de incidencia (°)')
    plt.ylabel('Factor de utilización IAM')
    plt.text(12, 0.4,'Temperaturas entre: '+ str(lim_inf)[:str(lim_inf).find(".")]+ ' y '+ str(lim_sup)[:str(lim_sup).find(".")], fontsize=15)
    plt.text(12, 0.35,'El coeficiente de determinación para ashrae es:  ' + str(RR_ashrae)[:str(RR_ashrae).find(".")+5], fontsize=15)
    plt.text(12, 0.30,'El valor del parámetro b usado es: ' + str(b)[:str(b).find(".")+3], fontsize=15)
    plt.text(25, 0.35,'El coeficiente de determinación para physical es:  ' + str(RR_physical)[:str(RR_physical).find(".")+5], fontsize=15)
    plt.text(25, 0.30,'El valor del parámetro n usado es: ' + str(n)[:str(n).find(".")+3], fontsize=15)
    plt.text(25, 0.25,'El valor del parámetro k usado es: ' + str(k)[:str(k).find(".")+3], fontsize=15)
    plt.text(25, 0.20,'El valor del parámetro l usado es: ' + str(l)[:str(l).find(".")+3], fontsize=15)
    plt.legend()
    plt.show()




#
#df=df[(df['T_Amb (°C)']<20)]
#df=df[(df['T_Amb (°C)']>15)]
#
##para verificar los parametros calculados.
#P_nor=np.array(df['PMP_estimated_IIIV (W)'])/np.array(df['PMP_estimated_IIIV (W)'].max())
#AOI=np.array(df['aoi'])
#COS=np.cos(AOI/180*math.pi)
#
#AUX=np.array(P_nor/COS)
#y=np.array(pvlib.iam.physical(aoi=AOI, n=0.9000000357627869,K=10.900008201599121, L=0.10000000149011612))
#y_ashrae=np.array(pvlib.iam.ashrae(aoi=AOI,b=1.1779999732971191))
#y_physical=np.array(pvlib.iam.physical(aoi=AOI, n=0.9000000357627869,K=10.900008201599121, L=0.10000000149011612))
#y_Martin=np.array(pvlib.iam.martin_ruiz(aoi=AOI,a_r=3140001.0))
#
#
#plt.figure(figsize=(30,15))
#plt.plot(AOI,AUX,'o',markersize=2,label='IAM(AOI)')
#plt.plot(AOI,y_physical,'o',markersize=2,label='funcion_physical')
#plt.plot(AOI,y_ashrae,'o',markersize=2,label='ashrae')
#plt.plot(AOI,y_Martin,'o',markersize=2,label='Martin')
#plt.legend()
#plt.show()
#
#
#print(E.Determination_coefficient(AUX,y_physical))
#print(E.Determination_coefficient(AUX,y_ashrae))











