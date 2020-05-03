# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import pvlib
import Error as E
import IAM_ashrae
import IAM_pysical_bruto
import IAM_Martin
df=pd.read_excel('C://Users/juanj/OneDrive/Escritorio/TFG/Datos_filtrados_IIIV_temp26.xls',encoding='utf-8')
df['IAM_aoi_']=(df['ISC_IIIV/DII (A m2/W)'])/(df['ISC_IIIV/DII (A m2/W)'].max())

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
plt.ylabel('IAM')
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

