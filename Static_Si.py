# -*- coding: utf-8 -*-
"""
Created on Fri May 22 13:23:45 2020

@author: juanj
"""

import pvlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from cpvtopvlib import cpvsystem
import Error as E



#AOILIMIT
AOILIMIT=55.0




#%%Código para la parte de silicio


df=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/Datos_filtrados_Si.csv',encoding='utf-8')




Max_temp=27.0
Min_temp=19.0
df=df[(df['T_Amb (°C)']>=Min_temp)]
df=df[((df['T_Amb (°C)'])<=Max_temp)] 


#------ parámetros de MArcos
module_parameters={'gamma_ref': 5.389, 'mu_gamma': 0.002, 'I_L_ref':3.058,
                'I_o_ref': 0.00000000045,'R_sh_ref': 18194, 'R_sh_0':73000,
                'R_sh_exp': 5.50,'R_s': 0.01,'alpha_sc':0.00,'EgRef':3.91,
                'irrad_ref': 1000,'temp_ref':25, 'cells_in_series':42,'cells'
                'eta_m':0.29, 'alpha_absorption':0.9}



# SistemaCPV=cpvsystem.StaticCPVSystem(module_parameters=module_parameters, 
#                                      modules_per_string=1,string_per_inverter=1,
#                                      racking_model='freestanding')

df_filt_Si=df[(df['aoi']<AOILIMIT)]

temp_cell=pvlib.temperature.pvsyst_cell(poa_global=df_filt_Si['GII (W/m2)'], 
                                        temp_air=df_filt_Si['T_Amb (°C)'],
                                        wind_speed=df_filt_Si['Wind Speed (m/s)'], 
                                        u_c=29.0, u_v=0.0, 
                                        eta_m=0.1, alpha_absorption=0.9)

# y_poli,RR_poli,a_s,b=E.regresion_polinomica(df_filt_temp['aoi'].values,df_filt_temp['ISC_IIIV/DII (A m2/W)'].values,2)
# Valor_normalizar=y_poli.max()
# Valor_normalizar=0.00096
# IAM=y_poli/Valor_normalizar

# # iam=y_poli
# effective_irradiance=df_filt_temp['DII (W/m2)']*IAM



# Five_parameters=SistemaCPV.calcparams_pvsyst(effective_irradiance, temp_cell)
# Five_parameters1=SistemaCPV.calcparams_pvsyst(df_filt_temp['DII (W/m2)'], temp_cell)


# Curvas=pvlib.pvsystem.singlediode(photocurrent=Five_parameters[0], saturation_current=Five_parameters[1],
#                                  resistance_series=Five_parameters[2],resistance_shunt=Five_parameters[3], 
#                                  nNsVth=Five_parameters[4],ivcurve_pnts=100, method='lambertw')
# Curvas1=pvlib.pvsystem.singlediode(photocurrent=Five_parameters1[0], saturation_current=Five_parameters1[1],
#                                  resistance_series=Five_parameters1[2],resistance_shunt=Five_parameters1[3], 
#                                  nNsVth=Five_parameters1[4],ivcurve_pnts=100, method='lambertw')

# #Representamos unas cuantas curavs iv
# plt.figure(figsize=(30,15))

# plt.plot(Curvas['v'][0],Curvas['i'][0],'--',markersize=2,label='IAM(AOI)')
# plt.plot(Curvas['v'][5],Curvas['i'][5],'--',markersize=2,label='IAM(AOI)')
# plt.plot(Curvas['v'][10],Curvas['i'][10],'--',markersize=2,label='IAM(AOI)')
# plt.plot(Curvas['v'][50],Curvas['i'][50],'--',markersize=2,label='IAM(AOI)')

# #Comparamos los datos de Pmp con los calculados
# plt.figure(figsize=(30,15))
# plt.plot(df_filt_temp['aoi'],Curvas['p_mp'],'o',markersize=2,label='con iam')
# plt.plot(df_filt_temp['aoi'],Curvas1['p_mp'],'o',markersize=2,label='sin iam')
# plt.plot(df_filt_temp['aoi'],df_filt_temp['PMP_estimated_IIIV (W)'],'o',markersize=2,label='Datos ')
# plt.legend()
