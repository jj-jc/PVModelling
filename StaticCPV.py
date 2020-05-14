# -*- coding: utf-8 -*-

import pvlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from cpvtopvlib import cpvsystem




df=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/Datos_filtrados.csv',encoding='utf-8')
Media_temp=df['T_Amb (°C)'].mean()
df=df[(df['T_Amb (°C)']<Media_temp+3)]
df=df[(df['T_Amb (°C)']>Media_temp-3)]
df=df[(df['aoi']<55)]

#Se recogen los datos de 26º unicamente
df=pd.read_excel('C://Users/juanj/OneDrive/Escritorio/TFG/Datos_filtrados_IIIV_temp26.xls',encoding='utf-8')
#Este es el valor de b obtenido para el modelo de ashrae 
B=0.584099999999952

#df=df[(df['DNI (W/m2)']>600)]
#------ parámetros de MArcos
module_parameters={'gamma_ref': 5.524, 'mu_gamma': 0.003, 'I_L_ref':0.96,
               'I_o_ref': 0.00000000017,'R_sh_ref': 5226, 'R_sh_0':21000,
               'R_sh_exp': 5.50,'R_s': 0.01,'alpha_sc':0.00,'EgRef':3.91,
               'irrad_ref': 1000,'temp_ref':25, 'cells_in_series':12,
               'eta_m':0.32, 'alpha_absorption':0.9}

SistemaCPV=cpvsystem.StaticCPVSystem(module_parameters=module_parameters, 
                                     modules_per_string=1,string_per_inverter=1,
                                     racking_model='freestanding')
temp_cell=SistemaCPV.pvsyst_celltemp(df['GNI (W/m2)'], df['T_Amb (°C)'],df['Wind Speed (m/s)'])

#·con el parámetro de ashrae generamos los IAM necesarios
iam=np.array(pvlib.iam.ashrae(aoi=df['aoi'],b=B))
# iam=y_poli
effective_irradiance=df['DII (W/m2)']*iam



Five_parameters=SistemaCPV.calcparams_pvsyst(effective_irradiance, temp_cell)
Five_parameters1=SistemaCPV.calcparams_pvsyst(df['DII (W/m2)'], temp_cell)


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

#Comparamos los datos de Pmp con los calculados
plt.figure(figsize=(30,15))
plt.plot(df['aoi'],Curvas['p_mp'],'o',markersize=2,label='con iam')
plt.plot(df['aoi'],Curvas1['p_mp'],'o',markersize=2,label='sin iam')
plt.plot(df['aoi'],df['PMP_estimated_IIIV (W)'],'o',markersize=2,label='Datos ')
plt.legend()

#plt.figure(figsize=(30,15))
#
#plt.plot(Curvas1['v'][0],Curvas1['i'][0],'--',markersize=2,label='IAM(AOI)')
#plt.plot(Curvas1['v'][5],Curvas1['i'][5],'--',markersize=2,label='IAM(AOI)')
#plt.plot(Curvas1['v'][10],Curvas1['i'][10],'--',markersize=2,label='IAM(AOI)')
#plt.plot(Curvas1['v'][50],Curvas1['i'][50],'--',markersize=2,label='IAM(AOI)')
#plt.figure(figsize=(30,15))
#plt.plot(df['aoi'],Curvas1['p_mp'],'o',markersize=2)
#plt.plot(df['aoi'],df['PMP_estimated_IIIV (W)'],'o',markersize=2)

