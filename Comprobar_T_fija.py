# -*- coding: utf-8 -*-

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
import IAM_Martin
df=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/Datos_filtrados.csv',encoding='utf-8')
#se introduce euna columna aue corresponde al index al escribir
df=df.set_index(pd.DatetimeIndex(df['Date Time']))
df=df.drop(['Date Time'],axis=1)
#filtramos el date frame en función del aoi para que las funciones de cálculo del IAM no de valores nan además 
#de que los valores en aois altos no son representativos para el la parte de III-V

df=df[(df['aoi']<55)]


#Se limita la temperatura para que esta no afecte al estudio de los datos en función del ángulo
Media_temp=df['T_Amb (°C)'].mean()
df=df[(df['T_Amb (°C)']<Media_temp+3)]
df=df[(df['T_Amb (°C)']>Media_temp-3)]

#--------------------------------------normalizamos la potencia estimada en la base de datos para comparar iams
P_nor=np.array(df['PMP_estimated_IIIV (W)'])/np.array(df['PMP_estimated_IIIV (W)'].max())
COS=np.cos(df['aoi']/180*math.pi)
df['IAM_aoi']=np.array(P_nor/COS)

#--------------------se calcula el iam en funcion de isc/dii-------------
df['IAM_aoi_']=df['ISC_IIIV/DII (A m2/W)']/(df['ISC_IIIV/DII (A m2/W)'].max())

#-------------------datos obtenidos para parametros de funciones de iam-----------------
b=1.1779999732971191
n=0.9000000357627869
k=10.900008201599121
l=0.10000000149011612


#--------------probamos con los parametros obtenidos--------------------------------
y_ashrae=np.array(pvlib.iam.ashrae(aoi=df['aoi'],b=b))
y_physical=np.array(pvlib.iam.physical(aoi=df['aoi'], n=n,K=k, L=l))
y_Martin=np.array(pvlib.iam.martin_ruiz(aoi=df['aoi'],a_r=3140001.0))

RR_physical=E.Determination_coefficient(df['IAM_aoi'],y_physical)
RR_ashrae=E.Determination_coefficient(df['IAM_aoi'],y_ashrae)

plt.figure(figsize=(30,15))
plt.plot(df['aoi'],df['IAM_aoi'],'o',markersize=2,label='IAM(AOI)')
plt.plot(df['aoi'],y_physical,'o',markersize=2,label='funcion_physical')
plt.plot(df['aoi'],y_ashrae,'o',markersize=2,label='ashrae')
plt.plot(df['aoi'],y_Martin,'o',markersize=2,label='Martin')
plt.xlabel('Ángulo de incidencia (°)')
plt.ylabel('Coeficiente de utilización')
plt.title("Regresiones de diferentes funciones para el coeficiente de utilización en función del ángulo de incidencia",fontsize=20)
#plt.text(12, 0.35,'El coeficiente de determinación para ashrae es:  ' + str(RR_ashrae)[:str(RR_ashrae).find(".")+5], fontsize=15)
#plt.text(12, 0.30,'El valor del parámetro b usado es: ' + str(b)[:str(b).find(".")+3], fontsize=15)
#plt.text(25, 0.35,'El coeficiente de determinación para physical es:  ' + str(RR_physical)[:str(RR_physical).find(".")+5], fontsize=15)
#plt.text(25, 0.30,'El valor del parámetro n usado es: ' + str(n)[:str(n).find(".")+3], fontsize=15)
#plt.text(25, 0.25,'El valor del parámetro k usado es: ' + str(k)[:str(k).find(".")+3], fontsize=15)
#plt.text(25, 0.20,'El valor del parámetro l usado es: ' + str(l)[:str(l).find(".")+3], fontsize=15)
plt.legend()
plt.show()
print('El coeficiente de determinación para ashrae es:  ' + str(RR_ashrae)[:str(RR_ashrae).find(".")+5])
print('El valor del parámetro b usado es: ' + str(b)[:str(b).find(".")+3])
print('El coeficiente de determinación para physical es:  ' + str(RR_physical)[:str(RR_physical).find(".")+5])
print('El valor del parámetro n usado es: ' + str(n)[:str(n).find(".")+3])
print('El valor del parámetro k usado es: ' + str(k)[:str(k).find(".")+3])
print('El valor del parámetro l usado es: ' + str(l)[:str(l).find(".")+3])







#--------------probamos con los parametros obtenidos y con la normalizacion del isc/DII--------------------------------
y_ashrae=np.array(pvlib.iam.ashrae(aoi=df['aoi'],b=b))
y_physical=np.array(pvlib.iam.physical(aoi=df['aoi'], n=n,K=k, L=l))
y_martin_ruiz=np.array(pvlib.iam.martin_ruiz(aoi=df['aoi'],a_r=3140001.0))

RR_physical=E.Determination_coefficient(df['IAM_aoi_'],y_physical)
RR_ashrae=E.Determination_coefficient(df['IAM_aoi_'],y_ashrae)
RR_martin=E.regresion_lineal(df['IAM_aoi_'],y_martin_ruiz)
plt.figure(figsize=(30,15))
plt.plot(df['aoi'],df['IAM_aoi_'],'o',markersize=2,label='IAM(AOI)')
plt.plot(df['aoi'],y_physical,'o',markersize=2,label='funcion_physical')
plt.plot(df['aoi'],y_ashrae,'o',markersize=2,label='ashrae')
plt.plot(df['aoi'],y_martin_ruiz,'o',markersize=2,label='Martin')
plt.xlabel('Ángulo de incidencia (°)')
plt.ylabel('Coeficiente de utilización')
plt.title("Regresiones de diferentes funciones para el coeficiente de utilización en función del ángulo de incidencia",fontsize=20)
#plt.text(12, 0.35,'El coeficiente de determinación para ashrae es:  ' + str(RR_ashrae)[:str(RR_ashrae).find(".")+5], fontsize=15)
#plt.text(12, 0.30,'El valor del parámetro b usado es: ' + str(b)[:str(b).find(".")+3], fontsize=15)
#plt.text(25, 0.35,'El coeficiente de determinación para physical es:  ' + str(RR_physical)[:str(RR_physical).find(".")+5], fontsize=15)
#plt.text(25, 0.30,'El valor del parámetro n usado es: ' + str(n)[:str(n).find(".")+3], fontsize=15)
#plt.text(25, 0.25,'El valor del parámetro k usado es: ' + str(k)[:str(k).find(".")+3], fontsize=15)
#plt.text(25, 0.20,'El valor del parámetro l usado es: ' + str(l)[:str(l).find(".")+3], fontsize=15)
plt.legend()
plt.show()
print('El coeficiente de determinación para ashrae es:  ' + str(RR_ashrae)[:str(RR_ashrae).find(".")+5])
print('El valor del parámetro b usado es: ' + str(b)[:str(b).find(".")+3])
print('El coeficiente de determinación para physical es:  ' + str(RR_physical)[:str(RR_physical).find(".")+5])
print('El valor del parámetro n usado es: ' + str(n)[:str(n).find(".")+3])
print('El valor del parámetro k usado es: ' + str(k)[:str(k).find(".")+3])
print('El valor del parámetro l usado es: ' + str(l)[:str(l).find(".")+3])
print('El coeficiente de determinación para Martin es:  ' + str(RR_martin)[:str(RR_martin).find(".")+5])






#----------------------------Se hace el fitting con los datos que se tienen---------------


RR_ashrae,b=IAM_ashrae.regresion_ashrae(df['aoi'],df['IAM_aoi'])
RR_physical,n,k,l =IAM_pysical_bruto.regresion_pysical(df['aoi'],df['IAM_aoi'])
RR_martin_ruiz,a_r=IAM_Martin.regresion_martin_ruiz(df['aoi'],df['IAM_aoi'])

y_ashrae=np.array(pvlib.iam.ashrae(aoi=df['aoi'],b=b))
y_pysical=np.array(pvlib.iam.physical(aoi=np.array(df['aoi']),n=n,K=k,L=l))
y_martin_ruiz=np.array(pvlib.iam.martin_ruiz(aoi=df['aoi'],a_r=a_r))

plt.figure(figsize=(30,15))
plt.plot(df['aoi'],df['IAM_aoi'],'o',markersize=2,label='todos los datos')
plt.plot(df['aoi'],y_ashrae,'o',markersize=2,label='regresión por ashrae')
plt.plot(df['aoi'],y_pysical,'o',markersize=2,label='regresión por pysical')
plt.plot(df['aoi'],y_martin_ruiz,'o',markersize=2,label='regresión por martin_ruiz')
plt.xlabel('Ángulo de incidencia (°)')
plt.ylabel('Factor de utilización IAM')
#    plt.text(12, 0.4,'Temperaturas entre: '+ str(lim_inf)[:str(lim_inf).find(".")]+ '°C y '+ str(lim_sup)[:str(lim_sup).find(".")]+'°C', fontsize=15)
#    plt.text(12, 0.35,'El coeficiente de determinación para ashrae es:  ' + str(RR_ashrae)[:str(RR_ashrae).find(".")+5], fontsize=15)
#    plt.text(12, 0.30,'El valor del parámetro b usado es: ' + str(b)[:str(b).find(".")+3], fontsize=15)
#    plt.text(25, 0.35,'El coeficiente de determinación para physical es:  ' + str(RR_physical)[:str(RR_physical).find(".")+5], fontsize=15)
#    plt.text(25, 0.30,'El valor del parámetro n usado es: ' + str(n)[:str(n).find(".")+3], fontsize=15)
#    plt.text(25, 0.25,'El valor del parámetro k usado es: ' + str(k)[:str(k).find(".")+3], fontsize=15)
#    plt.text(25, 0.20,'El valor del parámetro l usado es: ' + str(l)[:str(l).find(".")+3], fontsize=15)
plt.legend()
plt.show()
print('El coeficiente de determinación para ashrae es:  ' + str(RR_ashrae)[:str(RR_ashrae).find(".")+5])
print('El valor del parámetro b usado es: ' + str(b)[:str(b).find(".")+3])
print('El coeficiente de determinación para physical es:  ' + str(RR_physical)[:str(RR_physical).find(".")+5])
print('El valor del parámetro n usado es: ' + str(n)[:str(n).find(".")+3])
print('El valor del parámetro k usado es: ' + str(k)[:str(k).find(".")+3])
print('El valor del parámetro l usado es: ' + str(l)[:str(l).find(".")+3])
print('El coeficiente de determinación para martin_ruiz es:  ' + str(RR_martin_ruiz)[:str(RR_martin_ruiz).find(".")+5])
print('El valor del parámetro ar usado es: ' + str(a_r))
   

#-----------------fitting con los datos de normalizacion de ISC/DII------------



RR_ashrae,b=IAM_ashrae.regresion_ashrae(df['aoi'],df['IAM_aoi_'])
RR_physical,n,k,l =IAM_pysical_bruto.regresion_pysical(df['aoi'],df['IAM_aoi_'])
RR_martin_ruiz,a_r=IAM_Martin.regresion_martin_ruiz(df['aoi'],df['IAM_aoi_'])

y_ashrae=np.array(pvlib.iam.ashrae(aoi=df['aoi'],b=b))
y_pysical=np.array(pvlib.iam.physical(aoi=np.array(df['aoi']),n=n,K=k,L=l))
y_martin_ruiz=np.array(pvlib.iam.martin_ruiz(aoi=df['aoi'],a_r=a_r))

plt.figure(figsize=(30,15))
plt.plot(df['aoi'],df['IAM_aoi_'],'o',markersize=2,label='todos los datos')
plt.plot(df['aoi'],y_ashrae,'o',markersize=2,label='regresión por ashrae')
plt.plot(df['aoi'],y_pysical,'o',markersize=2,label='regresión por pysical')
plt.plot(df['aoi'],y_martin_ruiz,'o',markersize=2,label='regresión por martin_ruiz')
plt.xlabel('Ángulo de incidencia (°)')
plt.ylabel('Factor de utilización IAM')
#    plt.text(12, 0.4,'Temperaturas entre: '+ str(lim_inf)[:str(lim_inf).find(".")]+ '°C y '+ str(lim_sup)[:str(lim_sup).find(".")]+'°C', fontsize=15)
#    plt.text(12, 0.35,'El coeficiente de determinación para ashrae es:  ' + str(RR_ashrae)[:str(RR_ashrae).find(".")+5], fontsize=15)
#    plt.text(12, 0.30,'El valor del parámetro b usado es: ' + str(b)[:str(b).find(".")+3], fontsize=15)
#    plt.text(25, 0.35,'El coeficiente de determinación para physical es:  ' + str(RR_physical)[:str(RR_physical).find(".")+5], fontsize=15)
#    plt.text(25, 0.30,'El valor del parámetro n usado es: ' + str(n)[:str(n).find(".")+3], fontsize=15)
#    plt.text(25, 0.25,'El valor del parámetro k usado es: ' + str(k)[:str(k).find(".")+3], fontsize=15)
#    plt.text(25, 0.20,'El valor del parámetro l usado es: ' + str(l)[:str(l).find(".")+3], fontsize=15)
plt.legend()
plt.show()
print('El coeficiente de determinación para ashrae es:  ' + str(RR_ashrae)[:str(RR_ashrae).find(".")+5])
print('El valor del parámetro b usado es: ' + str(b)[:str(b).find(".")+3])
print('El coeficiente de determinación para physical es:  ' + str(RR_physical)[:str(RR_physical).find(".")+5])
print('El valor del parámetro n usado es: ' + str(n)[:str(n).find(".")+3])
print('El valor del parámetro k usado es: ' + str(k)[:str(k).find(".")+3])
print('El valor del parámetro l usado es: ' + str(l)[:str(l).find(".")+3])
print('El coeficiente de determinación para martin_ruiz es:  ' + str(RR_martin_ruiz)[:str(RR_martin_ruiz).find(".")+5])
print('El valor del parámetro ar usado es: ' + str(a_r))