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
import Error 



#AOILIMIT
AOILIMIT=55.0




#Código para la parte de silicio


df=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/Datos_filtrados_Si.csv',encoding='utf-8')

df_filt_Si=df[(df['aoi']>AOILIMIT)]



# df_iv=pd.merge(df_iv,df_iv_)
#%%Comprobación curvas obtenidas

# module_parameters_Si={'gamma_ref': 4.514, 'mu_gamma': 0.44, 'I_L_ref':1.802,
#                 'I_o_ref': 0.002309,'R_sh_ref': 3200, 'R_sh_0':128000,
#                 'R_sh_exp': 5.5,'R_s': 0.22,'alpha_sc':0.04,'EgRef':1.121,
#                 'irrad_ref': 306,'temp_ref':40, 'cells_in_series':4,
#                 'eta_m':0.1, 'alpha_absorption':1}




# temp_cell=pvlib.temperature.pvsyst_cell(poa_global=306, 
#                                         temp_air=11.413,
#                                         wind_speed=1.191, 
#                                         u_c=10.0, u_v=0.0, 
#                                         eta_m=0.1, alpha_absorption=1)


# Five_parameters1=pvlib.pvsystem.calcparams_pvsyst(306, temp_cell, alpha_sc=module_parameters_Si['alpha_sc'],
#                                  gamma_ref=module_parameters_Si['gamma_ref'], mu_gamma=module_parameters_Si['mu_gamma'],
#                                  I_L_ref=module_parameters_Si['I_L_ref'], I_o_ref=module_parameters_Si['I_o_ref'],
#                                  R_sh_ref=module_parameters_Si['R_sh_ref'], R_sh_0=module_parameters_Si['R_sh_0'], 
#                                  R_s=module_parameters_Si['R_s'], cells_in_series=module_parameters_Si['cells_in_series'], 
#                                  R_sh_exp=module_parameters_Si['R_sh_exp'], EgRef=module_parameters_Si['EgRef'], 
#                                  irrad_ref=module_parameters_Si['irrad_ref'], temp_ref=temp_cell)

# Curvas=pvlib.pvsystem.singlediode(photocurrent=Five_parameters1[0], saturation_current=Five_parameters1[1],
#                                   resistance_series=Five_parameters1[2],resistance_shunt=Five_parameters1[3], 
#                                   nNsVth=Five_parameters1[4],ivcurve_pnts=100, method='lambertw')

# plt.figure(figsize=(30,15))
# # plt.plot(Curvas1['v'],Curvas1['i'],'--',markersize=2,label='300')
# plt.plot(Curvas['v'],Curvas['i'],'--',markersize=2,label='306 con temp_cell')
# plt.plot(df_iv['V[V]'],df_iv['I[A]'],'--',markersize=2,label='Datos_300')
# # plt.plot(df_iv_['V[V]'],df_iv_['I[A]'],'--',markersize=2,label='Datos_190')
# plt.title('Comparación de las curvas obtenidas con los datos')
# plt.xlabel('V[V]')
# plt.ylabel('I[A]')
# plt.legend()

#%%
# Max_temp=27.0
# Min_temp=19.0
# df=df[(df['T_Amb (°C)']>=Min_temp)]
# df=df[((df['T_Amb (°C)'])<=Max_temp)] 


#------ parámetros de MArcos
# module_parameters={'gamma_ref': 5.389, 'mu_gamma': 0.002, 'I_L_ref':3.058,
#                 'I_o_ref': 0.00000000045,'R_sh_ref': 18194, 'R_sh_0':73000,
#                 'R_sh_exp': 5.50,'R_s': 0.01,'alpha_sc':0.00,'EgRef':3.91,
#                 'irrad_ref': 1000,'temp_ref':25, 'cells_in_series':42,'cells'
#                 'eta_m':0.29, 'alpha_absorption':0.9}4,7421,8024,514



# module_parameters_Si={'gamma_ref': 4.514, 'mu_gamma': 0.44, 'I_L_ref':1.802,
#                 'I_o_ref': 0.002309,'R_sh_ref': 3200, 'R_sh_0':128000,
#                 'R_sh_exp': 5.5,'R_s': 0.22,'alpha_sc':0.04,'EgRef':1.121,
#                 'irrad_ref': 300,'temp_ref':40, 'cells_in_series':3,
#                 'eta_m':0.1, 'alpha_absorption':0.9}

# SistemaCPV=cpvsystem.StaticCPVSystem(module_parameters=module_parameters_Si, 
#                                       modules_per_string=1,string_per_inverter=1,
#                                       racking_model='freestanding')
# # SistemaCPV=cpvsystem.StaticCPVSystem(module_parameters=module_parameters, 
# #                                      modules_per_string=1,string_per_inverter=1,
# #                                      racking_model='freestanding')



# temp_cell=pvlib.temperature.pvsyst_cell(poa_global=df_filt_Si['Irra_vista (W/m2)'], 
#                                         temp_air=df_filt_Si['T_Amb (°C)'],
#                                         wind_speed=df_filt_Si['Wind Speed (m/s)'], 
#                                         u_c=29.0, u_v=0.0, 
#                                         eta_m=0.1, alpha_absorption=0.9)


# y_poli,RR_poli,a_s,b=E.regresion_polinomica(df_filt_temp['aoi'].values,df_filt_temp['ISC_IIIV/DII (A m2/W)'].values,2)
# Valor_normalizar=y_poli.max()
# Valor_normalizar=0.00096
# IAM=y_poli/Valor_normalizar

# # iam=y_poli
# effective_irradiance=df_filt_temp['DII (W/m2)']*IAM



# Five_parameters=SistemaCPV.calcparams_pvsyst(200, 40)
# Five_parameters1=SistemaCPV.calcparams_pvsyst(300, 40)


# Curvas=pvlib.pvsystem.singlediode(photocurrent=Five_parameters[0], saturation_current=Five_parameters[1],
#                                   resistance_series=Five_parameters[2],resistance_shunt=Five_parameters[3], 
#                                   nNsVth=Five_parameters[4],ivcurve_pnts=100, method='lambertw')
# Curvas1=pvlib.pvsystem.singlediode(photocurrent=Five_parameters1[0], saturation_current=Five_parameters1[1],
#                                   resistance_series=Five_parameters1[2],resistance_shunt=Five_parameters1[3], 
#                                   nNsVth=Five_parameters1[4],ivcurve_pnts=100, method='lambertw')
# Curvas2=pvlib.pvsystem.singlediode(photocurrent=Five_parameters2[0], saturation_current=Five_parameters2[1],
#                                   resistance_series=Five_parameters2[2],resistance_shunt=Five_parameters2[3], 
#                                   nNsVth=Five_parameters2[4],ivcurve_pnts=100, method='lambertw')

# #COMPROBACIÓN CURVAS IV



# plt.figure(figsize=(30,15))
# plt.plot(Curvas1['v'],Curvas1['i'],'--',markersize=2,label='300')
# plt.plot(Curvas['v'],Curvas['i'],'--',markersize=2,label='200')
# plt.plot(df_iv['V[V]'],df_iv['I[A]'],'--',markersize=2,label='Datos_300')
# plt.plot(df_iv_['V[V]'],df_iv_['I[A]'],'--',markersize=2,label='Datos_190')
# plt.title('Comparación de las curvas obtenidas con los datos')
# plt.xlabel('V[V]')
# plt.ylabel('I[A]')
# plt.legend()
#%%AHora com

# module_parameters_Si={'gamma_ref': 4.514, 'mu_gamma': 0.44, 'I_L_ref':1.802,
#                 'I_o_ref': 0.002309,'R_sh_ref': 3200, 'R_sh_0':128000,
#                 'R_sh_exp': 5.5,'R_s': 0.22,'alpha_sc':0.04,'EgRef':1.121,
#                 'irrad_ref': 300,'temp_ref':40, 'cells_in_series':3,
#                 'eta_m':0.1, 'alpha_absorption':0.9}

# SistemaCPV=cpvsystem.StaticCPVSystem(module_parameters=module_parameters_Si, 
#                                       modules_per_string=1,string_per_inverter=1,
#                                       racking_model='freestanding')
# # SistemaCPV=cpvsystem.StaticCPVSystem(module_parameters=module_parameters, 
# #                                      modules_per_string=1,string_per_inverter=1,
# #                                      racking_model='freestanding')




# df_filt_Si=df[(df['aoi']>AOILIMIT)]

# plt.figure(figsize=(30,15))
# plt.plot(df_filt_Si['aoi'],df_filt_Si['PMP_estimated_Si (W)'],'o',markersize=2,label='Datos ')


# plt.xlabel('V[V]')
# plt.ylabel('I[A]')
# plt.legend()



# limSup=df_filt_Si['aoi'].max()
# limInf=df_filt_Si['aoi'].min()
# Rango=limSup-limInf
# n_intervalos=100
# porcent_mediana=20
# incremento=Rango/n_intervalos
# for i in range(n_intervalos):
#     AUX=df_filt_Si[df_filt_Si['aoi']>limInf+i*incremento]
#     AUX=AUX[AUX['aoi']<=limInf+incremento*(1+i)]
#     Mediana=E.mediana(AUX['PMP_estimated_Si (W)'].values)
#     DEBAJO=AUX[AUX['PMP_estimated_Si (W)']<(Mediana*(1-porcent_mediana/100))]   
#     df_filt_Si=df_filt_Si.drop(DEBAJO.index[:],axis=0)
#     ENCIMA=AUX[AUX['PMP_estimated_Si (W)']>(Mediana*(1+porcent_mediana/100))]
#     df_filt_Si=df_filt_Si.drop(ENCIMA.index[:],axis=0)
    
    
# plt.figure(figsize=(30,15))
# plt.plot(df_filt_Si['aoi'],df_filt_Si['PMP_estimated_Si (W)'],'o',markersize=2,label='300')


# plt.xlabel('V[V]')
# plt.ylabel('I[A]')
# plt.legend()
#%%

df_filt_Si['Irra_vista_efectiva (W/m2)']=((df_filt_Si['Irra_vista (W/m2)'].values)*Error.calc_iam_Si(df_filt_Si['aoi'].values,'Tercer grado'))
df_filt_Si['ISC_Si/Irra_vista_efectiva (A m2/W)']=((df_filt_Si['ISC_measured_Si (A)'].values)/(df_filt_Si['Irra_vista_efectiva (W/m2)'].values))
filt_x=df_filt_Si['T_Amb (°C)'].values
filt_y=df_filt_Si['ISC_Si/Irra_vista_efectiva (A m2/W)'].values



temp_cell=pvlib.temperature.pvsyst_cell(poa_global=df_filt_Si['Irra_vista (W/m2)'], 
                                        temp_air=df_filt_Si['T_Amb (°C)'],
                                        wind_speed=df_filt_Si['Wind Speed (m/s)'], 
                                        u_c=29.0, u_v=0.0, 
                                        eta_m=0.1, alpha_absorption=1)

temp_cell1=pvlib.temperature.pvsyst_cell(poa_global=df_filt_Si['Irra_vista_efectiva (W/m2)'], 
                                        temp_air=df_filt_Si['T_Amb (°C)'],
                                        wind_speed=df_filt_Si['Wind Speed (m/s)'], 
                                        u_c=29.0, u_v=0.0, 
                                        eta_m=0.1, alpha_absorption=1)

plt.figure(figsize=(30,15))
plt.plot(df_filt_Si['aoi'],df_filt_Si['Irra_vista (W/m2)'],'o',markersize=2,label='irradiciancia vista')
plt.plot(df_filt_Si['aoi'],df_filt_Si['Irra_vista_efectiva (W/m2)'],'o',markersize=2,label='irradiciancia vista efectiva')
plt.legend()


plt.figure(figsize=(30,15))
plt.plot(df_filt_Si['aoi'],temp_cell,'o',markersize=2,label='temperatura célula con irradiciancia vista')
plt.plot(df_filt_Si['aoi'],temp_cell1,'o',markersize=2,label='temperatura célula con irradiciancia vista efectiva')
plt.plot(df_filt_Si['aoi'],df_filt_Si['T_Amb (°C)'],'o',markersize=2,label='temperatura ambiente ')
plt.legend()

# y_poli,RR_poli,a_s,b=E.regresion_polinomica(df_filt_temp['aoi'].values,df_filt_temp['ISC_IIIV/DII (A m2/W)'].values,2)
# Valor_normalizar=y_poli.max()
# Valor_normalizar=0.00096
# IAM=y_poli/Valor_normalizar

# # iam=y_poli
# effective_irradiance=df_filt_temp['DII (W/m2)']*IAM

Five_parameters=SistemaCPV.calcparams_pvsyst(df_filt_Si['Irra_vista (W/m2)'], temp_cell)
Five_parameters1=SistemaCPV.calcparams_pvsyst(df_filt_Si['Irra_vista_efectiva (W/m2)'], temp_cell1)

Five_parameters=SistemaCPV.calcparams_pvsyst(df_filt_Si['Irra_vista (W/m2)'], 40)
Five_parameters1=SistemaCPV.calcparams_pvsyst(df_filt_Si['Irra_vista_efectiva (W/m2)'], 40)


# plt.figure(figsize=(30,15))
# plt.plot(df_filt_Si['aoi'],Five_parameters[4],'o',markersize=2,label='Irradiancia vista')
# plt.plot(df_filt_Si['aoi'],Five_parameters1[4],'o',markersize=2,label='Irradiancia efectiva')


#%%
# Curvas=pvlib.pvsystem.singlediode(photocurrent=Five_parameters[0], saturation_current=Five_parameters[1],
#                                   resistance_series=Five_parameters[2],resistance_shunt=Five_parameters[3], 
#                                   nNsVth=Five_parameters[4],
#                                   ivcurve_pnts=511,
#                                   method='newton')

# Curvas1=pvlib.pvsystem.singlediode(photocurrent=Five_parameters1[0], saturation_current=Five_parameters1[1],
#                                   resistance_series=Five_parameters1[2],resistance_shunt=Five_parameters1[3], 
#                                   nNsVth=Five_parameters1[4],ivcurve_pnts=511, method='newton')


Curvas=pvlib.pvsystem.singlediode(photocurrent=Five_parameters[0], saturation_current=Five_parameters[1],
                                  resistance_series=Five_parameters[2],resistance_shunt=Five_parameters[3], 
                                  nNsVth=Five_parameters[4],
                                  ivcurve_pnts=100,
                                  method='lambertw')

Curvas1=pvlib.pvsystem.singlediode(photocurrent=Five_parameters1[0], saturation_current=Five_parameters1[1],
                                  resistance_series=Five_parameters1[2],resistance_shunt=Five_parameters1[3], 
                                  nNsVth=Five_parameters1[4],ivcurve_pnts=100, method='lambertw')
# Curvas2=pvlib.pvsystem.singlediode(photocurrent=Five_parameters2[0], saturation_current=Five_parameters2[1],
#                                   resistance_series=Five_parameters2[2],resistance_shunt=Five_parameters2[3], 
#                                   nNsVth=Five_parameters2[4],ivcurve_pnts=100, method='lambertw')

# #COMPROBACIÓN CURVAS IV



plt.figure(figsize=(30,15))
plt.plot(df_filt_Si['aoi'],Curvas['p_mp'],'o',markersize=2,label='Potencia con Irradiancia vista')
plt.plot(df_filt_Si['aoi'],Curvas1['p_mp'],'o',markersize=2,label='Potencia con Irradiancia vista efectiva')
plt.plot(df_filt_Si['aoi'],df_filt_Si['PMP_estimated_Si (W)'],'o',markersize=2,label='Datos potencia')
plt.ylim(0,5)
# plt.plot(df_iv['V[V]'],df_iv['I[A]'],'--',markersize=2,label='Datos_300')
# plt.plot(df_iv_['V[V]'],df_iv_['I[A]'],'--',markersize=2,label='Datos_190')
plt.title('Comparación de las curvas obtenidas con los datos')
plt.xlabel('V[V]')
plt.ylabel('I[A]')
plt.legend()
Error_iam_Si=Error.RMSE(df_filt_Si['PMP_estimated_Si (W)'],Curvas1['p_mp'])
print('El error cuadrático medio de la aproximación es de: ' + str(Error_iam_Si))



# plt.figure(figsize=(30,15))
# plt.plot(df_filt_Si['airmass_relative'],df_filt_Si['ISC_Si/Irra_vista_efectiva (A m2/W)'],'o',markersize=2,label='IAM(AOI)')
# plt.legend()

# plt.figure(figsize=(30,15))
# plt.plot(df_filt_Si['T_Amb (°C)'],df_filt_Si['ISC_Si/Irra_vista_efectiva (A m2/W)'],'o',markersize=2,label='IAM(AOI)')
# plt.legend()
# #Comparamos los datos de Pmp con los calculados
# plt.figure(figsize=(30,15))
# plt.plot(df_filt_temp['aoi'],Curvas['p_mp'],'o',markersize=2,label='con iam')
# plt.plot(df_filt_temp['aoi'],Curvas1['p_mp'],'o',markersize=2,label='sin iam')
# plt.plot(df_filt_temp['aoi'],df_filt_temp['PMP_estimated_IIIV (W)'],'o',markersize=2,label='Datos ')
# plt.legend()
