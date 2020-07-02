# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 16:57:10 2020

@author: juanj
"""

from pvlib.location import Location
import CPVClass
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import Error as E

import datetime


#Datos:
#localización
lat=40.453
lon=-3.727
alt=667
tz='Europe/Berlin'
#orientación
surface_tilt=30
surface_azimuth=180
#AOILIMIT
AOILIMIT=55.0





#Se construye el objeto Si_CPVSystem

Mi_Si_CPV=CPVClass.Flat_CPVSystem(surface_tilt=surface_tilt, surface_azimuth=surface_azimuth,
                 AOILIMIT=AOILIMIT,albedo=None, surface_type=None,
                 module=None, module_type='glass_polymer',
                 module_parameters=None,
                 temperature_model_parameters=None,
                 modules_per_string=1, strings_per_inverter=1,
                 inverter=None, inverter_parameters=None,
                 racking_model='open_rack', losses_parameters=None, name=None,
                 iam_parameters=None)

Mi_Si_CPV.module_parameters_Si={'gamma_ref': 2.13, 'mu_gamma': 0.002, 'I_L_ref':2.355,
                'I_o_ref': 0.0000147,'R_sh_ref': 3000, 'R_sh_0':8000,
                'R_sh_exp': 5.5,'R_s': 0.35,'alpha_sc':0.0,'EgRef':1.121,
                'irrad_ref': 400,'temp_ref':25, 'cells_in_series':4,
                'eta_m':0.16, 'alpha_absorption':0.9}

Mi_Si_CPV.temperature_model_parameters={'u_c': 29.0,'u_v':0}

Mi_Si_CPV.iam_parameters={'a3':0.000121,'a2':-0.023926,
                        'a1':1.539450,'b': 0.03,'valor_norm':0.0008938270669770386}


Flat_location=Location(latitude=lat,longitude=lon,tz=tz,altitude=alt)



Localized_Mi_Si_CPV=CPVClass.LocalizedFlat_CVSystem(Mi_Si_CPV,Flat_location)


Hola=Localized_Mi_Si_CPV.get_aoi(solar_zenith=Solar_position['zenith'], solar_azimuth=Solar_position['azimuth'])

#%%
#'pdc0': 25,'gamma_pdc':-0.005 son para comprobar que fuuncionen las funcione, pero no esta correctamente seleccionado
# Mi_CPV.inverter_parameters={'pdc0': 25, 'eta_inv_nom': 0.96 ,'eta_inv_ref':0.9637}


tz='Europe/Berlin'
pd.plotting.register_matplotlib_converters()#ESTA SENTENCIA ES NECESARIA PARA DIBUJAR DATE.TIMES


df=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/Datos_filtrados_Si.csv',encoding='utf-8')


#SE filtran los datos que no correspondan a una tendencia clara de la potencia.
Si=df[(df['aoi']>=AOILIMIT)]
Fecha=pd.DatetimeIndex(Si['Date Time'])
Si=Si.set_index(Fecha)
Si=Si.drop(['Date Time'],axis=1)

#Se limpian un poco los datos de potencia por medio de la mediana 
limSup=Si['aoi'].max()
limInf=Si['aoi'].min()
Rango=limSup-limInf
n_intervalos=100
porcent_mediana=20
incremento=Rango/n_intervalos
for i in range(n_intervalos):
    AUX=Si[Si['aoi']>limInf+i*incremento]
    AUX=AUX[AUX['aoi']<=limInf+incremento*(1+i)]
    Mediana=E.mediana(AUX['PMP_estimated_Si (W)'].values)
    DEBAJO=AUX[AUX['PMP_estimated_Si (W)']<(Mediana*(1-porcent_mediana/100))]   
    Si=Si.drop(DEBAJO.index[:],axis=0)
    ENCIMA=AUX[AUX['PMP_estimated_Si (W)']>(Mediana*(1+porcent_mediana/100))]
    Si=Si.drop(ENCIMA.index[:],axis=0)




#%%%


# CPV['DII_efectiva_tercer_grado (W/m2)']=CPV['DII (W/m2)']*E.calc_iam(CPV['aoi'].values,'Tercer grado')
# CPV['DII_efectiva_segundo_grado (W/m2)']=CPV['DII (W/m2)']*E.calc_iam(CPV['aoi'].values,'Segundo grado')
# CPV['DII_efectiva_primer_grado (W/m2)']=CPV['DII (W/m2)']*E.calc_iam(CPV['aoi'].values,'Primer grado')
# CPV['ISC_IIIV/DII_efectiva_tercer_grado (W/m2)']=CPV['ISC_measured_IIIV (A)']/CPV['DII_efectiva_tercer_grado (W/m2)']
# CPV['ISC_IIIV/DII_efectiva_segundo_grado (W/m2)']=CPV['ISC_measured_IIIV (A)']/CPV['DII_efectiva_segundo_grado (W/m2)']
# CPV['ISC_IIIV/DII_efectiva_primer_grado (W/m2)']=CPV['ISC_measured_IIIV (A)']/CPV['DII_efectiva_primer_grado (W/m2)']


Si['Irra_vista_efectiva (W/m2)']=((Si['Irra_vista (W/m2)'].values)*Mi_Si_CPV.get_iam(Si['aoi'],iam_model='Tercer grado'))
Si['ISC_Si/Irra_vista_efectiva (A m2/W)']=((Si['ISC_measured_Si (A)'].values)/(Si['Irra_vista_efectiva (W/m2)'].values))
# filt_x=df_filt_Si['T_Amb (°C)'].values
# filt_y=df_filt_Si['ISC_Si/Irra_vista_efectiva (A m2/W)'].values

fig=plt.figure(figsize=(30,15))
plt.plot(Si['aoi'],Si['DII_efectiva_tercer_grado (W/m2)'],'o',markersize=4,label='DII_corregida')   
plt.plot(Si['aoi'],Si['DII (W/m2)'],'o',markersize=4,label='DII')
plt.xlabel('Ángulo de incidencia (º)')
plt.ylabel('Irradiancia (W/m2)')
plt.legend()
plt.title("Comparación de la irradiancia corregida")

#%% Cálculo de la temperatura de cell, no tengo muy claro que el uc sea el correcto


temp_cell=Mi_CPV.pvsyst_celltemp(poa_global=CPV['DII_efectiva_tercer_grado (W/m2)'], temp_air=CPV['T_Amb (°C)'], wind_speed=CPV['Wind Speed (m/s)']) 
temp_cell_=Mi_CPV.pvsyst_celltemp(poa_global=CPV['DII (W/m2)'], temp_air=CPV['T_Amb (°C)'], wind_speed=CPV['Wind Speed (m/s)'])

fig=plt.figure(figsize=(30,15))
plt.plot(CPV.index[:].time,temp_cell,'o',markersize=2,label='Temperatura con DII corregida')   
plt.plot(CPV.index[:].time,temp_cell_,'o',markersize=2,label='Temperatura con DII')
plt.xlabel('Horas')
plt.ylabel('Temperatura de célula (°C)')
plt.legend()
plt.title("Temperatura de célula a lo largo de las horas de un día ")

#%% Cálculo I_sc y la potencia y comparación con los datos
Five_parameters=Mi_CPV.calcparams_pvsyst(CPV['DII_efectiva_tercer_grado (W/m2)'], temp_cell)
Five_parameters_=Mi_CPV.calcparams_pvsyst(CPV['DII (W/m2)'], temp_cell_)

Curvas=Mi_CPV.singlediode(photocurrent=Five_parameters[0], saturation_current=Five_parameters[1],
                                  resistance_series=Five_parameters[2],resistance_shunt=Five_parameters[3], 
                                  nNsVth=Five_parameters[4],ivcurve_pnts=100, method='lambertw')
Curvas_=Mi_CPV.singlediode(photocurrent=Five_parameters_[0], saturation_current=Five_parameters_[1],
                                  resistance_series=Five_parameters_[2],resistance_shunt=Five_parameters_[3], 
                                  nNsVth=Five_parameters_[4],ivcurve_pnts=100, method='lambertw')

#Representamos unas cuantas curavs iv
plt.figure(figsize=(30,15))
plt.plot(CPV['aoi'],Curvas_['i_sc'],'o',markersize=2,label='Sin IAM')
plt.plot(CPV['aoi'],Curvas['i_sc'],'o',markersize=2,label='IAM_tercer_grado')
plt.plot(CPV['aoi'],CPV['ISC_measured_IIIV (A)'],'o',markersize=2,label='Datos medidos de ISC_IIIV')
# plt.plot(Curvas_2['v'][165],Curvas_2['i'][165],'--',markersize=2,label='IAM_segundo_grado')
# plt.plot(Curvas_1['v'][165],Curvas_1['i'][165],'--',markersize=2,label='IAM_primer_grado')
# plt.plot(Curvas['v'][165],Curvas['i'][165],'--',markersize=2,label='GII')
plt.plot()
plt.xlabel('Voltaje (III-V) (V)')
plt.ylabel('Corriente (III-V) (A)')
plt.title('Curvas I-V para validar el proceso anterior')
plt.legend()

plt.figure(figsize=(30,15))
plt.plot(CPV['aoi'],CPV['PMP_estimated_IIIV (W)'],'o',markersize=2,label='Datos ')
plt.plot(CPV['aoi'],Curvas_['p_mp'],'o',markersize=2,label='Sin IAM')
plt.plot(CPV['aoi'],Curvas['p_mp'],'o',markersize=2,label='IAM_tercer_grado')
plt.xlabel('Ángulo de incidencia (°)')
plt.ylabel('Puntos de máxima potencia (W)')
plt.title('Comparación de los resultados con los datos estimados de potencias en funcion del iam')
plt.legend()
