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
pd.plotting.register_matplotlib_converters()#ESTA SENTENCIA ES NECESARIA PARA DIBUJAR DATE.TIMES

#Se construye el objeto Si_SiSystem

Mi_Si_CPV=CPVClass.Flat_CPVSystem(surface_tilt=surface_tilt, surface_azimuth=surface_azimuth,
                 albedo=None, surface_type=None,
                 module=None, 
                 module_Flat_parameters=None,
                 temperature_model_Flat_parameters=None,
                 modules_per_string=1, strings_per_inverter=1,
                 inverter=None, inverter_parameters=None, 
                 losses_parameters=None, name=None,
                 iam_Flat_parameters=None, uf_parameters=None)

Mi_Si_CPV.module_Flat_parameters={'gamma_ref': 2.13, 'mu_gamma': 0.002, 'I_L_ref':2.355,
                'I_o_ref': 0.0000147,'R_sh_ref': 3000, 'R_sh_0':8000,
                'R_sh_exp': 5.5,'R_s': 0.35,'alpha_sc':0.0,'EgRef':1.121,
                'irrad_ref': 400,'temp_ref':25, 'cells_in_series':4,
                'eta_m':0.16, 'alpha_absorption':0.9}

Mi_Si_CPV.temperature_model_Flat_parameters={'u_c': 29.0,'u_v':0}
# Mi_Si_CPV.iam_Flat_parameters={'a3': 0.00015150050021614284,'a2':-0.02987855934621265,
#                         'a1':1.9229049866733197,'b':-39.58930494613328,'valor_norm':0.005027867032371985}


Mi_Si_CPV.iam_Flat_parameters={'a3': 0.000089,'a2': -0.017687,
                        'a1':1.129321,'b':-22.488592,'valor_norm':0.00515}

Flat_location=Location(latitude=lat,longitude=lon,tz=tz,altitude=alt)

Localized_Mi_Si_CPV=CPVClass.LocalizedFlat_CPVSystem(Mi_Si_CPV,Flat_location)



#%%
#'pdc0': 25,'gamma_pdc':-0.005 son para comprobar que fuuncionen las funcione, pero no esta correctamente seleccionado
# Mi_Si.inverter_parameters={'pdc0': 25, 'eta_inv_nom': 0.96 ,'eta_inv_ref':0.9637}


df=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/filt_df_Si.csv',encoding='utf-8')


Si=df[(df['aoi']>AOILIMIT)]
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

Si['Irra_vista_efectiva (W/m2)']=((Si['Irra_vista (W/m2)'].values)*Mi_Si_CPV.get_iam(Si['aoi'],iam_model='Third degree'))
Si['ISC_Si/Irra_vista_efectiva (A m2/W)']=((Si['ISC_measured_Si (A)'].values)/(Si['Irra_vista_efectiva (W/m2)'].values))


# # filt_x=df_filt_Si['T_Amb (ºC)'].values
# # filt_y=df_filt_Si['ISC_Si/Irra_vista_efectiva (A m2/W)'].values

fig=plt.figure(figsize=(30,15))
plt.plot(Si['aoi'],Si['Irra_vista_efectiva (W/m2)'],'o',markersize=4,label='Irradiancia efectiva')   
plt.plot(Si['aoi'],Si['Irra_vista (W/m2)'],'o',markersize=4,label='Irradiancia')   
plt.xlabel('Ángulo de incidencia (º)')
plt.ylabel('Irradiancia (W/m2)')
plt.legend()
plt.title("Comparación de la irradiancia corregida")

#%%

Irradianccia_afecta_temp=Si['Irra_vista_efectiva (W/m2)']+Si['Difusa']
temp_cell=Mi_Si_CPV.pvsyst_celltemp(poa_global=Irradianccia_afecta_temp, temp_air=Si['T_Amb (ºC)'], wind_speed=Si['Wind Speed (m/s)']) 
temp_cell_=Mi_Si_CPV.pvsyst_celltemp(poa_global=Si['Irra_vista (W/m2)'], temp_air=Si['T_Amb (ºC)'], wind_speed=Si['Wind Speed (m/s)'])

# fig=plt.figure(figsize=(30,15))
# plt.plot(Si.index[:].time,temp_cell,'o',markersize=2,label='Temperatura con DII corregida')   
# plt.plot(Si.index[:].time,temp_cell_,'o',markersize=2,label='Temperatura con DII')
# plt.xlabel('Horas')
# plt.ylabel('Temperatura de célula (ºC)')
# plt.legend()
# plt.title("Temperatura de célula a lo largo de las horas de un día ")

#%% Cálculo I_sc y la potencia y comparación con los datos


Five_parameters=Mi_Si_CPV.calcparams_pvsyst(Si['Irra_vista_efectiva (W/m2)'], temp_cell)
Five_parameters_=Mi_Si_CPV.calcparams_pvsyst(Si['Irra_vista (W/m2)'], temp_cell_)

Curvas=Mi_Si_CPV.singlediode(photocurrent=Five_parameters[0], saturation_current=Five_parameters[1],
                                  resistance_series=Five_parameters[2],resistance_shunt=Five_parameters[3], 
                                  nNsVth=Five_parameters[4],ivcurve_pnts=100, method='lambertw')
Curvas_=Mi_Si_CPV.singlediode(photocurrent=Five_parameters_[0], saturation_current=Five_parameters_[1],
                                  resistance_series=Five_parameters_[2],resistance_shunt=Five_parameters_[3], 
                                  nNsVth=Five_parameters_[4],ivcurve_pnts=100, method='lambertw')


Diferencia_potencia_=Curvas['p_mp']-Si['PMP_estimated_Si (W)'].values
Diferencia_potencia_dat=Curvas_['p_mp']-Si['PMP_estimated_Si (W)'].values




plt.figure(figsize=(30,15))
plt.plot(Si['aoi'],Si['PMP_estimated_Si (W)'],'o',markersize=2,label='Datos')
plt.plot(Si['aoi'],Curvas_['p_mp'],'o',markersize=2,label='Sin corregir')
plt.plot(Si['aoi'],Curvas['p_mp'],'o',markersize=2,label='Corregido con IAM')
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.xlabel('Ángulo de incidencia (º)',fontsize=30)
plt.ylabel('Puntos de máxima potencia (W)',fontsize=30)
plt.title('Comparación de los resultados con los datos estimados de potencias en funcion del ángulo de incidencia',fontsize=40)
plt.legend(fontsize=30,markerscale=3)

RMS_potencia=E.RMSE(Si['PMP_estimated_IIIV (W)'],Curvas['p_mp'])
MAE_potencia=E.MAE(Si['PMP_estimated_IIIV (W)'], Curvas['p_mp'])
Datos_max=Si['PMP_estimated_IIIV (W)'].max()
Datos_min=Si['PMP_estimated_IIIV (W)'].min()
Datos_media=sum(Si['PMP_estimated_IIIV (W)'].values)/len(Si['PMP_estimated_IIIV (W)'].values)
Potencia_max=Curvas['p_mp'].max()
Potencia_min=Curvas['p_mp'].min()
Potencia_media=sum(Curvas['p_mp'])/len(Curvas['p_mp'])



plt.figure(figsize=(30,15))
plt.plot(Si['aoi'],Diferencia_potencia_,'o',markersize=2,label='Corregido con IAM')
plt.plot(Si['aoi'],Diferencia_potencia_dat,'o',markersize=2,label='Sin corregir')
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.xlabel('Ángulo de incidencia (º)',fontsize=30)
plt.ylabel('Error de potencia (W)',fontsize=30)
plt.title('Residuos en función del ángulo de incidencia',fontsize=40)
plt.legend(fontsize=30,markerscale=3)

plt.figure(figsize=(30,15))
plt.plot(Si['airmass_relative'],Diferencia_potencia_,'o',markersize=2,label='Corregido con IAM')
plt.plot(Si['airmass_relative'],Diferencia_potencia_dat,'o',markersize=2,label='Sin corregir')
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.xlabel('Masa del aire (n.d.)',fontsize=30)
plt.ylabel('Errores de potencia (W)',fontsize=30)
plt.title('Residuos en función de la masa del aire',fontsize=40)
plt.legend(fontsize=30,markerscale=3)

plt.figure(figsize=(30,15))
plt.plot(Si['T_Amb (ºC)'],Diferencia_potencia_,'o',markersize=2,label='Corregido con IAM')
plt.plot(Si['T_Amb (ºC)'],Diferencia_potencia_dat,'o',markersize=2,label='Sin corregir')
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.xlabel('Temperatura ambiente (ºC)',fontsize=30)
plt.ylabel('Errores de potencia (W)',fontsize=30)
plt.title('Residuos en función de la temperatura',fontsize=40)
plt.legend(fontsize=30,markerscale=3)


# #Representamos unas cuantas curavs iv
# plt.figure(figsize=(30,15))
# plt.plot(Si['aoi'],Curvas_['i_sc'],'o',markersize=2,label='Sin IAM')
# plt.plot(Si['aoi'],Curvas['i_sc'],'o',markersize=2,label='IAM_tercer_grado')
# plt.plot(Si['aoi'],Si['ISC_measured_Si (A)'],'o',markersize=2,label='Datos medidos de ISC_Si')
# # plt.plot(Curvas_2['v'][165],Curvas_2['i'][165],'--',markersize=2,label='IAM_segundo_grado')
# # plt.plot(Curvas_1['v'][165],Curvas_1['i'][165],'--',markersize=2,label='IAM_primer_grado')
# # plt.plot(Curvas['v'][165],Curvas['i'][165],'--',markersize=2,label='GII')
# plt.plot()
# plt.xlabel('Voltaje (Si) (V)')
# plt.ylabel('Corriente (Si) (A)')
# plt.title('Curvas I-V para validar el proceso anterior')
# plt.legend()
