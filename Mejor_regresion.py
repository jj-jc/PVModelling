# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 10:35:39 2020

@author: juanj
"""

import pvlib 
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt 
import Error as E
#Este script servirá para comparar los tres métodos utilizados para la regresión de 
#la nube de puntos.

df=pd.read_excel('C://Users/juanj/OneDrive/Escritorio/TFG/Insolight_CPV_AOI_response.xlsx',encoding= 'unicode_escape')
# df=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/InsolightMay2019.csv',encoding= 'unicode_escape')
#recogemos los datos en un dataframe
df_CPV_AOI_response=pd.DataFrame(data=np.array(df.iloc[2:10,:],dtype='float64'), columns=np.array(df.iloc[1,:]))
Datos=df_CPV_AOI_response['UF (AOI) - Losses additional to cos(AOI) ']

x=df_CPV_AOI_response['Angle']
y_datos=df_CPV_AOI_response['UF (AOI) - Losses additional to cos(AOI) ']  

y_ashrae=np.array(pvlib.iam.ashrae(aoi=x,b=1.1779999732971191))
y_physical=np.array(pvlib.iam.physical(aoi=x, n=0.9000000357627869,K=10.900008201599121, L=0.10000000149011612))
y_Martin=np.array(pvlib.iam.martin_ruiz(aoi=x,a_r=3140001.0))

plt.figure(figsize=(20,15))
plt.title("Comparación de los diferentes modelos de IAM con los datos de respuesta")
plt.plot(x,y_datos,'o',markersize=2,label='Datos')
plt.plot(x,y_ashrae,'--',markersize=2,label='Método de la secante (Ashrae)')
plt.plot(x,y_physical,'--',markersize=2,label='Método físico (tres parámetros)')
plt.plot(x,y_Martin,'--',markersize=2,label='Método pérdidas por ángulo de incidencia (Martín_Ruiz)')
plt.legend()
plt.xlabel('Ángulo de incidencia (º)')
plt.ylabel('Factor de utilización IAM')
plt.text(2, 0.55,'El coeficiente de determinación del método de la secante es:  ' + str(E.Determination_coefficient(y_datos,y_ashrae)), fontsize=15)
plt.text(2, 0.5,'El coeficiente de determinación del método físico es: ' + str(E.Determination_coefficient(y_datos,y_physical)), fontsize=15)
plt.text(2, 0.45,'El coeficiente de determinación del método Martín_Ruiz es: ' + str(E.Determination_coefficient(y_datos,y_Martin)), fontsize=15)
plt.show()





















