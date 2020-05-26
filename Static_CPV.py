# -*- coding: utf-8 -*-

import pvlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from cpvtopvlib import cpvsystem
import Error as E



#AOILIMIT
AOILIMIT=55.0





#%%código para cuando aoi<AOILIMIT
df=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/IIIV.csv',encoding='utf-8')
# Media_temp=df['T_Amb (°C)'].mean()
# df=df[(df['T_Amb (°C)']<Media_temp+3)]
# df=df[(df['T_Amb (°C)']>Media_temp-3)]



Max_temp=27.0
Min_temp=19.0
df=df[(df['T_Amb (°C)']>=Min_temp)]
df=df[((df['T_Amb (°C)'])<=Max_temp)] 


# #Se recogen los datos de 26º unicamente
# df=pd.read_excel('C://Users/juanj/OneDrive/Escritorio/TFG/Datos_filtrados_IIIV_temp26.xls',encoding='utf-8')



#------ parámetros de MArcos
module_parameters={'gamma_ref': 5.524, 'mu_gamma': 0.003, 'I_L_ref':0.96,
                'I_o_ref': 0.00000000017,'R_sh_ref': 5226, 'R_sh_0':21000,
                'R_sh_exp': 5.50,'R_s': 0.01,'alpha_sc':0.00,'EgRef':3.91,
                'irrad_ref': 1000,'temp_ref':25, 'cells_in_series':12,
                'eta_m':0.32, 'alpha_absorption':0.9}



SistemaCPV=cpvsystem.StaticCPVSystem(module_parameters=module_parameters, 
                                      modules_per_string=1,string_per_inverter=1,
                                      racking_model='freestanding')

df_filt_temp=df[(df['aoi']<AOILIMIT)]

temp_cell=pvlib.temperature.pvsyst_cell(poa_global=df_filt_temp['GII (W/m2)'], temp_air=df_filt_temp['T_Amb (°C)'], wind_speed=df_filt_temp['Wind Speed (m/s)'], u_c=29.0, u_v=0.0, eta_m=0.1, alpha_absorption=0.9)

# y_poli,RR_poli,a_s,b=E.regresion_polinomica(df_filt_temp['aoi'].values,df_filt_temp['ISC_IIIV/DII (A m2/W)'].values,2)
# # Valor_normalizar=y_poli.max()
# Valor_normalizar=0.00096
# IAM=y_poli/Valor_normalizar

# iam=y_poli
effective_irradiance=df_filt_temp['DII_efectiva'].values



Five_parameters=SistemaCPV.calcparams_pvsyst(effective_irradiance, temp_cell)
Five_parameters1=SistemaCPV.calcparams_pvsyst(df_filt_temp['DII (W/m2)'], temp_cell)


Curvas=pvlib.pvsystem.singlediode(photocurrent=Five_parameters[0], saturation_current=Five_parameters[1],
                                  resistance_series=Five_parameters[2],resistance_shunt=Five_parameters[3], 
                                  nNsVth=Five_parameters[4],ivcurve_pnts=100, method='lambertw')
Curvas1=pvlib.pvsystem.singlediode(photocurrent=Five_parameters1[0], saturation_current=Five_parameters1[1],
                                  resistance_series=Five_parameters1[2],resistance_shunt=Five_parameters1[3], 
                                  nNsVth=Five_parameters1[4],ivcurve_pnts=100, method='lambertw')

#Representamos unas cuantas curavs iv

plt.figure(figsize=(30,15))
plt.plot(Curvas['v'][0],Curvas['i'][0],'--',markersize=2,label='IAM(AOI)')
plt.plot(Curvas['v'][5],Curvas['i'][5],'--',markersize=2,label='IAM(AOI)')
plt.plot(Curvas['v'][10],Curvas['i'][10],'--',markersize=2,label='IAM(AOI)')
plt.plot(Curvas['v'][50],Curvas['i'][50],'--',markersize=2,label='IAM(AOI)')
plt.xlabel('Voltaje (III-V) (V)')
plt.ylabel('Corriente (III-V) (A)')
plt.title('Curvas I-V para validar el proceso anterior')
plt.legend()

#Comparamos los datos de Pmp con los calculados
plt.figure(figsize=(30,15))
plt.plot(df_filt_temp['aoi'],Curvas['p_mp'],'o',markersize=2,label='con iam')
plt.plot(df_filt_temp['aoi'],Curvas1['p_mp'],'o',markersize=2,label='sin iam')
plt.plot(df_filt_temp['aoi'],df_filt_temp['PMP_estimated_IIIV (W)'],'o',markersize=2,label='Datos ')
plt.xlabel('Ángulo de incidencia (°)')
plt.ylabel('Puntos de máxima potencia (W)')
plt.title('Comparación de los resultados con los datos estimados de potencias en funcion del iam')
plt.legend()

UF=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/UF.csv',encoding='utf-8')

Max_temp=27.0
Min_temp=19.0
UF=UF[(UF['temp']>=Min_temp)]
UF=UF[((UF['temp'])<=Max_temp)] 



#Ahora hay que buscar los pesos que mejor describan las potencias.
w_am=0.5
w_temp=0.5

# UF_total=w_am*UF['UF_am']+w_temp*UF['UF_temp']
# Potencia_estimada=Curvas['p_mp']*UF_total



Potencias_estimadas=pd.DataFrame(columns=['Potencias_estimadas (W)','diferencias', 'RMSE'])
datos_potencia=df_filt_temp['PMP_estimated_IIIV (W)'].values

aux=np.arange(0,1,0.01)
for i in aux:
    w_am=i
    w_temp=1-w_am    
    UF_total=w_am*UF['UF_am']+w_temp*UF['UF_temp']   
    estimacion=Curvas['p_mp']*UF_total
    Juntos=[estimacion,datos_potencia-estimacion,E.RMSE(datos_potencia,estimacion)]    
    Potencias_estimadas.loc['w_am='+str(i)]=Juntos
    

   
index=Potencias_estimadas[Potencias_estimadas['RMSE']==Potencias_estimadas['RMSE'].min()].index[0]


plt.figure(figsize=(30,15))
plt.plot(df_filt_temp['aoi'],Curvas['p_mp'],'o',markersize=2,label='sin UF')
plt.plot(df_filt_temp['aoi'],Potencias_estimadas['Potencias_estimadas (W)'][index],'o',markersize=2,label='Con UF')
plt.plot(df_filt_temp['aoi'],df_filt_temp['PMP_estimated_IIIV (W)'],'o',markersize=2,label='Datos ')
plt.xlabel('Ángulo de incidencia (°)')
plt.ylabel('Potencia (III-V)(W)')
plt.title('Comparación de los resultados con los datos estimados de potencias en funcion del UF')
plt.legend()

plt.figure(figsize=(30,15))
plt.plot(df_filt_temp['aoi'],Potencias_estimadas['diferencias'][index],'o',markersize=4,label='Residuos de las potencias calculadas ')
plt.xlabel('Ángulo de incidencia (°)')
plt.ylabel('Potencia (III-V)(W)')
plt.title('Residuos de las potencias calculadas con los datos estimados')
plt.legend()
print('El error cuadrático medio de las estimaciones es de: ' + str(Potencias_estimadas['RMSE'][index]))



plt.figure(figsize=(30,15))
plt.plot(df_filt_temp['T_Amb (°C)'],Potencias_estimadas['diferencias'][index],'o',markersize=4,label='Residuos de las potencias calculadas ')
plt.xlabel('Temperatura ambiente (°C)')
plt.ylabel('Potencia (III-V)(W)')
plt.title('Residuos de las potencias calculadas con los datos estimados')
plt.legend()
print('El error cuadrático medio de las estimaciones es de: ' + str(Potencias_estimadas['RMSE'][index]))

plt.figure(figsize=(30,15))
plt.plot(df_filt_temp['airmass_relative'],Potencias_estimadas['diferencias'][index],'o',markersize=4,label='Residuos de las potencias calculadas ')
plt.xlabel('airmass (n.d.)')
plt.ylabel('Potencia (III-V)(W)')
plt.title('Residuos de las potencias calculadas con los datos estimados')
plt.legend()
print('El error cuadrático medio de las estimaciones es de: ' + str(Potencias_estimadas['RMSE'][index]))



# plt.figure(figsize=(30,15))
# plt.plot(df_filt_temp['aoi'],Potencias_estimadas['Potencias_estimadas (W)'][index],'o',markersize=4,label='Potencia estimada')
# plt.plot(df_filt_temp['aoi'],datos_potencia,'o',markersize=4,label='Datos de potencia')
# plt.legend()





#%%CÓDIGO PARA CUANDO AOI>AOILIMIT ,no corre prisa es mas importante el silicio

# df_filt_AOILIMIT=df[(df['aoi']>AOILIMIT)]
# temp_cell=pvlib.temperature.pvsyst_cell(poa_global=df_filt_AOILIMIT['GII (W/m2)'], 
#                                         temp_air=df_filt_AOILIMIT['T_Amb (°C)'], 
#                                         wind_speed=df_filt_AOILIMIT['Wind Speed (m/s)'], 
#                                         u_c=29.0, u_v=0.0, eta_m=0.1, alpha_absorption=0.9)

# y_poli,RR_poli,a_s,b=E.regresion_polinomica(df_filt_AOILIMIT['aoi'].values,df_filt_AOILIMIT['ISC_IIIV/DII (A m2/W)'].values,2)

# Valor_normalizar=0.00096
# IAM=y_poli/Valor_normalizar


# effective_irradiance=df_filt_AOILIMIT['DII (W/m2)']*IAM



# Five_parameters=SistemaCPV.calcparams_pvsyst(effective_irradiance, temp_cell)
# Five_parameters1=SistemaCPV.calcparams_pvsyst(df_filt_AOILIMIT['DII (W/m2)'], temp_cell)


# Curvas=pvlib.pvsystem.singlediode(photocurrent=Five_parameters[0], saturation_current=Five_parameters[1],
#                                   resistance_series=Five_parameters[2],resistance_shunt=Five_parameters[3], 
#                                   nNsVth=Five_parameters[4],ivcurve_pnts=100, method='lambertw')
# Curvas1=pvlib.pvsystem.singlediode(photocurrent=Five_parameters1[0], saturation_current=Five_parameters1[1],
#                                   resistance_series=Five_parameters1[2],resistance_shunt=Five_parameters1[3], 
#                                   nNsVth=Five_parameters1[4],ivcurve_pnts=100, method='lambertw')

# # #Representamos unas cuantas curavs iv
# plt.figure(figsize=(30,15))

# plt.plot(Curvas['v'][0],Curvas['i'][0],'--',markersize=2,label='IAM(AOI)')
# plt.plot(Curvas['v'][5],Curvas['i'][5],'--',markersize=2,label='IAM(AOI)')
# plt.plot(Curvas['v'][10],Curvas['i'][10],'--',markersize=2,label='IAM(AOI)')
# plt.plot(Curvas['v'][50],Curvas['i'][50],'--',markersize=2,label='IAM(AOI)')

# #Comparamos los datos de Pmp con los calculados
# plt.figure(figsize=(30,15))
# plt.plot(df_filt_AOILIMIT['aoi'],Curvas['p_mp'],'o',markersize=2,label='con iam')
# plt.plot(df_filt_AOILIMIT['aoi'],Curvas1['p_mp'],'o',markersize=2,label='sin iam')
# plt.plot(df_filt_AOILIMIT['aoi'],df_filt_AOILIMIT['PMP_estimated_IIIV (W)'],'o',markersize=2,label='Datos ')
# plt.legend()

# # UF=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/UF.csv',encoding='utf-8')

# # Max_temp=27.0
# # Min_temp=19.0
# # UF=UF[(UF['temp']>=Min_temp)]
# # UF=UF[((UF['temp'])<=Max_temp)] 



# # #Ahora hay que buscar los pesos que mejor describan las potencias.
# # w_am=0.5
# # w_temp=0.5

# # UF_total=w_am*UF['UF_am']+w_temp*UF['UF_temp']
# # Potencia_estimada=Curvas['p_mp']*UF_total

# # plt.figure(figsize=(30,15))
# # plt.plot(df_filt_temp['aoi'],Curvas['p_mp'],'o',markersize=2,label='con iam')
# # plt.plot(df_filt_temp['aoi'],Potencia_estimada,'o',markersize=2,label='sin iam')
# # plt.plot(df_filt_temp['aoi'],df_filt_temp['PMP_estimated_IIIV (W)'],'o',markersize=2,label='Datos ')
# # plt.legend()

# # Potencias_estimadas=pd.DataFrame(columns=['Potencias_estimadas (W)','diferencias', 'RMSE'])
# # datos_potencia=df_filt_temp['PMP_estimated_IIIV (W)'].values

# # aux=np.arange(0,1,0.01)
# # for i in aux:
# #     w_am=i
# #     w_temp=1-w_am    
# #     UF_total=w_am*UF['UF_am']+w_temp*UF['UF_temp']   
# #     estimacion=Curvas['p_mp']*UF_total
# #     Juntos=[estimacion,datos_potencia-estimacion,E.RMSE(datos_potencia,estimacion)]    
# #     Potencias_estimadas.loc['w_am='+str(i)]=Juntos
    

   
# # index=Potencias_estimadas[Potencias_estimadas['RMSE']==Potencias_estimadas['RMSE'].min()].index[0]


# # plt.figure(figsize=(30,15))
# # plt.plot(df_filt_temp['aoi'],Potencias_estimadas['diferencias'][index],'o',markersize=4,label='con iam')
# # plt.legend()

# # plt.figure(figsize=(30,15))
# # plt.plot(df_filt_temp['aoi'],Potencias_estimadas['Potencias_estimadas (W)'][index],'o',markersize=4,label='Potencia estimada')
# # plt.plot(df_filt_temp['aoi'],datos_potencia,'o',markersize=4,label='Datos de potencia')
# # plt.legend()


