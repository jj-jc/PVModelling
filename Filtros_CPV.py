# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 13:09:38 2020

@author: juanj
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import Error 
import plotly.graph_objects as go

from mpl_toolkits.axes_grid1 import host_subplot
#Codigo para poder expresar las gráfcas en plotly
import plotly.io as pio
pio.renderers.default='browser'


#AOILIMIT
AOILIMIT=55.0
# Valor_normalizar=0.00091802
# VALOR_NORMALIZAR=0.00096




#%% PARA LOS CPV
df=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/Datos_filtrados_IIIV.csv',encoding='utf-8')

df=df[(df['aoi']<AOILIMIT)]
df['DII_efectiva (W/m2)']=df['DII (W/m2)']*Error.calc_iam(df['aoi'].values,'Tercer grado')
df['ISC_IIIV/DII_efectiva (A m2/W)']=df['ISC_measured_IIIV (A)']/df['DII_efectiva (W/m2)']


#%% La parte del iam
Data_IAM=df
Data_IAM=Data_IAM[Data_IAM['Wind Dir. (m/s)']>=133.0]
Data_IAM=Data_IAM[Data_IAM['Wind Dir. (m/s)']<143]
Data_IAM=Data_IAM[Data_IAM['Wind Speed (m/s)']>=1.4]
Data_IAM=Data_IAM[Data_IAM['Wind Speed (m/s)']<2.5]
Data_IAM=Data_IAM[Data_IAM['T_Amb (°C)']>=26.0]
Data_IAM=Data_IAM[Data_IAM['T_Amb (°C)']<28]

df_extrapola=Data_IAM
df_extrapola=df_extrapola[df_extrapola['aoi']>=10.0]
df_extrapola=df_extrapola[df_extrapola['aoi']<30]
yr_extrapola, RR_extrapola, a_s_extrapola, b_extrapola=Error.regresion_polinomica(df_extrapola['aoi'].values, df_extrapola['ISC_IIIV/DII (A m2/W)'].values, 1)
x_añadir=np.arange(0,12,.5)
y_añadir=x_añadir*a_s_extrapola[1]+b_extrapola

'''AHORA VOY A CREAR DOS VECTORES QUE RECOGERÁN TODOS LOS DATOS A APROXIMAR'''
x_regresion=np.concatenate((x_añadir,Data_IAM['aoi'].values))
y_regresion=np.concatenate((y_añadir,Data_IAM['ISC_IIIV/DII (A m2/W)'].values))


IAM=pd.DataFrame({'aoi':x_regresion,'ISC_IIIV/DII (A m2/W)':y_regresion})



#%% La parte del uf_temp


Data_UF_temp=df
Data_UF_temp=Data_UF_temp[(Data_UF_temp['airmass_relative']>=1.0)]
Data_UF_temp=Data_UF_temp[(Data_UF_temp['airmass_relative']<1.1)]
# filt_x=filt_df_temp['T_Amb (°C)'].values
# filt_y=filt_df_temp['ISC_IIIV/DII_efectiva (A m2/W)'].values

UF_temp=pd.DataFrame({'T_Amb (°C)':Data_UF_temp['T_Amb (°C)'].values,'ISC_IIIV/DII_efectiva (A m2/W)':Data_UF_temp['ISC_IIIV/DII_efectiva (A m2/W)'].values})

#%% La parte del uf_am


Data_UF_am=df
Data_UF_am=Data_UF_am[Data_UF_am['Wind Speed (m/s)']>=0.9]
Data_UF_am=Data_UF_am[Data_UF_am['Wind Speed (m/s)']<1.1]
Data_UF_am=Data_UF_am[Data_UF_am['T_Amb (°C)']>=20]
Data_UF_am=Data_UF_am[Data_UF_am['T_Amb (°C)']<28]

UF_am=pd.DataFrame({'airmass':Data_UF_am['airmass_relative'].values,'ISC_IIIV/DII_efectiva (A m2/W)':Data_UF_am['ISC_IIIV/DII_efectiva (A m2/W)'].values})


#%% PARA LOS de silicio

df_si=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/Datos_filtrados_Si.csv',encoding='utf-8')

greater_AOI=df_si[(df_si['aoi']>AOILIMIT)]

#%% IAM








#%%  Se guardan todos en un archivo de excel para tenerlos a mano
writer = pd.ExcelWriter('C://Users/juanj/OneDrive/Escritorio/TFG/datos_para_calcular.xlsx', engine='xlsxwriter')
IAM.to_excel(writer, sheet_name='Cálculo_iam_CPV')
UF_am.to_excel(writer, sheet_name='Cálculo_uf_am_CPV')
UF_temp.to_excel(writer, sheet_name='Cálculo_uf_temp_CPV')
writer.save()
writer.close()
