# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 13:09:38 2020

@author: juanj
"""

import pandas as pd
import numpy as np
import Error 
#AOILIMIT
AOILIMIT=55.0

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
Data_IAM=Data_IAM[Data_IAM['T_Amb (ºC)']>=26.0]
Data_IAM=Data_IAM[Data_IAM['T_Amb (ºC)']<28]

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

UF_temp=pd.DataFrame({'T_Amb (ºC)':Data_UF_temp['T_Amb (ºC)'].values,'ISC_IIIV/DII_efectiva (A m2/W)':Data_UF_temp['ISC_IIIV/DII_efectiva (A m2/W)'].values})
#%% La parte del uf_am

Data_UF_am=df
Data_UF_am=Data_UF_am[Data_UF_am['T_Amb (ºC)']>=19]
Data_UF_am=Data_UF_am[Data_UF_am['T_Amb (ºC)']<22]
#filtrado para búsqueda de la línea de tendencia:
filtrado_eliminar=Data_UF_am[Data_UF_am['ISC_IIIV/DII_efectiva (A m2/W)']<0.00085]
filtrado_eliminar=filtrado_eliminar[filtrado_eliminar['airmass_relative']<1.3]                  
Data_UF_am=Data_UF_am.drop(filtrado_eliminar.index[:],axis=0)

filtrado_eliminar=Data_UF_am[Data_UF_am['ISC_IIIV/DII_efectiva (A m2/W)']>0.00076]
filtrado_eliminar=filtrado_eliminar[filtrado_eliminar['airmass_relative']>1.44]     
Data_UF_am=Data_UF_am.drop(filtrado_eliminar.index[:],axis=0)

UF_am=pd.DataFrame({'airmass':Data_UF_am['airmass_relative'].values,'ISC_IIIV/DII_efectiva (A m2/W)':Data_UF_am['ISC_IIIV/DII_efectiva (A m2/W)'].values})
#%% La parte de Si
df_si=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/filt_df_Si.csv',encoding='utf-8')
# Smaller AOILIMIT
smaller_AOI=df_si[(df_si['aoi']<AOILIMIT)]

smaller_AOI=smaller_AOI[smaller_AOI['T_Amb (ºC)']>=30.0]
# smaller_AOI=smaller_AOI[smaller_AOI['T_Amb (ºC)']>=30]
smaller_AOI=smaller_AOI[smaller_AOI['Wind Speed (m/s)']>=0.8]
smaller_AOI=smaller_AOI[smaller_AOI['Wind Speed (m/s)']<1.2]
smaller_AOI=smaller_AOI[smaller_AOI['Wind Dir. (m/s)']>=79.0]
smaller_AOI=smaller_AOI[smaller_AOI['Wind Dir. (m/s)']<=150.0]

Data_smaller_Si=pd.DataFrame({'aoi':smaller_AOI['aoi'].values,'ISC_Si/Irra_vista (A m2/W)':smaller_AOI['ISC_Si/Irra_vista (A m2/W)'].values})
# greater AOILIMT
greater_AOI=df_si[(df_si['aoi']>AOILIMIT)]

greater_AOI=greater_AOI[greater_AOI['T_Amb (ºC)']>=30.0]
greater_AOI=greater_AOI[greater_AOI['T_Amb (ºC)']<32]


Data_greater_Si=pd.DataFrame({'aoi':greater_AOI['aoi'].values,'ISC_Si/Irra_vista (A m2/W)':greater_AOI['ISC_Si/Irra_vista (A m2/W)'].values})

#%%  Se guardan todos en un archivo de excel para tenerlos a mano
writer = pd.ExcelWriter('C://Users/juanj/OneDrive/Escritorio/TFG/datos_para_calcular.xlsx', engine='xlsxwriter')
IAM.to_excel(writer, sheet_name='Cálculo_iam_CPV')
UF_am.to_excel(writer, sheet_name='Cálculo_uf_am_CPV')
UF_temp.to_excel(writer, sheet_name='Cálculo_uf_temp_CPV')
Data_smaller_Si.to_excel(writer, sheet_name='Cálculo_iam_Si_smaller')
Data_greater_Si.to_excel(writer, sheet_name='Cálculo_iam_Si_greater')
writer.save()
writer.close()
