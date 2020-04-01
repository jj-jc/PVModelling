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

df=pd.read_excel('C://Users/juanj/OneDrive/Escritorio/TFG/Datos_filtrados.xlsx')
#se introduce euna columna aue corresponde al index al escribir
df=df.drop(['Unnamed: 0'], axis=1)

#para verificar los parametros calculados.
P_nor=df['PMP_estimated_IIIV (W)']/df['PMP_estimated_IIIV (W)'].max()
AOI=np.array(df['aoi'])
COS=np.cos(AOI/180*math.pi)

AUX=P_nor/COS
y=np.array(pvlib.iam.physical(aoi=AOI, n=0.9000000357627869,K=10.900008201599121, L=0.10000000149011612))
plt.figure(figsize=(10,7))
plt.plot(AOI,AUX,'o',markersize=2,label='IAM(AOI)')
plt.plot(AOI,y,'o',markersize=2,label='funcion_physical')
plt.legend()
plt.show()
