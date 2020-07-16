# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 11:03:31 2020

@author: juanj
"""


# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 20:46:37 2020

@author: juanj
"""
import CPVClass
import pandas as pd
import numpy as np
import pvlib
df=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/Datos_filtrados_IIIV.csv',encoding='utf-8')
df=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/Entradas.csv',encoding='utf-8')


plt.figure(figsize=(30,15))
plt.plot(df['aoi'],df['PMP_estimated_IIIV (W)'],'o',markersize=2,label='sin UF')

plt.xlabel('Ángulo de incidencia (º)')
plt.ylabel('Potencia (III-V)(W)')
plt.title('Comparación de los resultados con los datos estimados de potencias en funcion del UF')
plt.legend()