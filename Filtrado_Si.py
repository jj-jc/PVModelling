# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 20:46:59 2020

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

filt_df=df[(df['PMP_estimated_Si (W)']>0.1)]
filt_df2=filt_df[(df['DifusaI (W/m2)']>50)]
