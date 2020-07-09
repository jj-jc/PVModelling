# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 09:56:02 2020

@author: juanj
"""


from pvlib.location import Location
import CPVClass
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import Error as E

import datetime



#Se construye el objeto CPVSystem

Mi_CPV=CPVClass.CPVSystem(surface_tilt=30, surface_azimuth=180,
                 AOILIMIT=55.0,albedo=None, surface_type=None,
                 module=None, module_type='glass_polymer',
                 module_parameters=None,
                 temperature_model_parameters=None,
                 modules_per_string=1, strings_per_inverter=1,
                 inverter=None, inverter_parameters=None,
                 racking_model='open_rack', losses_parameters=None, name=None,
                 iam_parameters=None)

Mi_CPV.module_CPV_parameters={'gamma_ref': 5.524, 'mu_gamma': 0.003, 'I_L_ref':0.96,
                'I_o_ref': 0.00000000017,'R_sh_ref': 5226, 'R_sh_0':21000,
                'R_sh_exp': 5.50,'R_s': 0.01,'alpha_sc':0.00,'EgRef':3.91,
                'irrad_ref': 1000,'temp_ref':25, 'cells_in_series':12,
                'eta_m':0.32, 'alpha_absorption':0.9, 'pdc0': 25,'gamma_pdc':-0.005 }

Mi_CPV.temperature_model_parameters={'u_c': 10.0,'u_v':0}

Mi_CPV.iam_CPV_parameters={'a3':-8.315977512579898e-06,'a2':0.00039212250547851236,
                        'a1':-0.006006260890940105,'valor_norm':0.0008938270669770386}



Mi_CPV.uf_parameters={'m1_am':0.172793, 'thld_am':1.285187 ,'m2_am':-0.408000,
                      'm_temp':-0.006439, 'thld_temp':15.18,
                      'w_am':0.41400000000000003,'w_temp': 0.464}

#'pdc0': 25,'gamma_pdc':-0.005 son para comprobar que fuuncionen las funcione, pero no esta correctamente seleccionado
Mi_CPV.inverter_parameters={'pdc0': 25, 'eta_inv_nom': 0.96 ,'eta_inv_ref':0.9637}






tz='Europe/Berlin'

#AOILIMIT
AOILIMIT=55.0
pd.plotting.register_matplotlib_converters()#ESTA SENTENCIA ES NECESARIA PARA DIBUJAR DATE.TIMES


df=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/Datos_filtrados_IIIV.csv',encoding='utf-8')



#SE filtran los datos que no correspondan a una tendencia clara de la potencia.
CPV=df[(df['aoi']<=AOILIMIT)]
Fecha=pd.DatetimeIndex(CPV['Date Time'])
CPV=CPV.set_index(Fecha)
CPV=CPV.drop(['Date Time'],axis=1)
CPV_=CPV
#Se limpian un poco los datos de potencia por medio de la mediana 
limSup=CPV['aoi'].max()
limInf=CPV['aoi'].min()
Rango=limSup-limInf
n_intervalos=100
porcent_mediana=20
incremento=Rango/n_intervalos
for i in range(n_intervalos):
    AUX=CPV[CPV['aoi']>limInf+i*incremento]
    AUX=AUX[AUX['aoi']<=limInf+incremento*(1+i)]
    Mediana=E.mediana(AUX['PMP_estimated_IIIV (W)'].values)
    DEBAJO=AUX[AUX['PMP_estimated_IIIV (W)']<(Mediana*(1-porcent_mediana/100))]   
    CPV=CPV.drop(DEBAJO.index[:],axis=0)
    ENCIMA=AUX[AUX['PMP_estimated_IIIV (W)']>(Mediana*(1+porcent_mediana/100))]
    CPV=CPV.drop(ENCIMA.index[:],axis=0)

plt.figure(figsize=(30,15))
plt.plot(CPV_['aoi'],CPV_['PMP_estimated_IIIV (W)'],'o',markersize=2,label='Datos')
plt.plot(CPV['aoi'],CPV['PMP_estimated_IIIV (W)'],'o',markersize=2,label='Datos filtrados con mediana')
plt.xlabel('Ángulo de incidencia (°)')
plt.ylabel('Potencia (III-V)(W)')
plt.title('Visualizar los datos filtrados por la mediana')
plt.legend()


CPV=E.mediana_filter(data=CPV,colum_intervals='aoi',columna_filter='DII (W/m2)',n_intervalos=20,porcent_mediana=10)

plt.figure(figsize=(30,15))
plt.plot(CPV['aoi'],CPV['DII (W/m2)'],'o',markersize=2,label='Datos ')
plt.plot(CPV['aoi'],CPV['DII (W/m2)'],'o',markersize=2,label='Datos filtrado con mediana de DII')
plt.xlabel('Ángulo de incidencia (°)')
plt.ylabel('Potencia (III-V)(W)')
plt.title('Comparación de los resultados con los datos estimados de potencias en funcion del UF')
plt.legend()

# CPV['DII_efectiva_tercer_grado (W/m2)']=CPV['DII (W/m2)']*E.calc_iam(CPV['aoi'].values,'Tercer grado')
# CPV['DII_efectiva_segundo_grado (W/m2)']=CPV['DII (W/m2)']*E.calc_iam(CPV['aoi'].values,'Segundo grado')
# CPV['DII_efectiva_primer_grado (W/m2)']=CPV['DII (W/m2)']*E.calc_iam(CPV['aoi'].values,'Primer grado')
# CPV['ISC_IIIV/DII_efectiva_tercer_grado (W/m2)']=CPV['ISC_measured_IIIV (A)']/CPV['DII_efectiva_tercer_grado (W/m2)']
# CPV['ISC_IIIV/DII_efectiva_segundo_grado (W/m2)']=CPV['ISC_measured_IIIV (A)']/CPV['DII_efectiva_segundo_grado (W/m2)']
# CPV['ISC_IIIV/DII_efectiva_primer_grado (W/m2)']=CPV['ISC_measured_IIIV (A)']/CPV['DII_efectiva_primer_grado (W/m2)']

''' lo he comentado para poder ejecutar todo sin tner que ejectuar todo , luego hay que descomentarlo------------------------------------------------ 
CPV['DII_efectiva_tercer_grado (W/m2)']=CPV['DII (W/m2)']*Mi_CPV.get_iam(CPV['aoi'],iam_model='Tercer grado')


fig=plt.figure(figsize=(30,15))
plt.plot(CPV['aoi'],CPV['DII_efectiva_tercer_grado (W/m2)'],'o',markersize=4,label='DII con iam')   
plt.plot(CPV['aoi'],CPV['DII (W/m2)'],'o',markersize=4,label='DII')
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
Five_parameters=Mi_CPV.calcparams_cpvsyst(CPV['DII_efectiva_tercer_grado (W/m2)'], temp_cell)
Five_parameters_=Mi_CPV.calcparams_cpvsyst(CPV['DII (W/m2)'], temp_cell_)

Curvas=Mi_CPV.singlediode(photocurrent=Five_parameters[0], saturation_current=Five_parameters[1],
                                  resistance_series=Five_parameters[2],resistance_shunt=Five_parameters[3], 
                                  nNsVth=Five_parameters[4],ivcurve_pnts=100, method='lambertw')
Curvas_=Mi_CPV.singlediode(photocurrent=Five_parameters_[0], saturation_current=Five_parameters_[1],
                                  resistance_series=Five_parameters_[2],resistance_shunt=Five_parameters_[3], 
                                  nNsVth=Five_parameters_[4],ivcurve_pnts=100, method='lambertw')


Potencia=Curvas['p_mp']*Mi_CPV.get_uf(CPV['airmass_relative'].values,CPV['T_Amb (°C)'].values)
Intensidad=Curvas['i_sc']*Mi_CPV.get_uf(CPV['airmass_relative'].values,CPV['T_Amb (°C)'].values)


plt.figure(figsize=(30,15))
plt.plot(CPV['aoi'],Curvas_['i_sc'],'o',markersize=2,label='Sin IAM')
plt.plot(CPV['aoi'],Curvas['i_sc'],'o',markersize=2,label='IAM_tercer_grado')
plt.plot(CPV['aoi'],Intensidad,'o',markersize=2,label='conUF')
plt.plot(CPV['aoi'],CPV['ISC_measured_IIIV (A)'],'o',markersize=2,label='Datos medidos de ISC_IIIV')
plt.plot()
plt.xlabel('Voltaje (III-V) (V)')
plt.ylabel('Corriente (III-V) (A)')
plt.title('Curvas I-V para validar el proceso anterior')
plt.legend()


plt.figure(figsize=(30,15))
plt.plot(CPV['aoi'],CPV['PMP_estimated_IIIV (W)'],'o',markersize=2,label='Datos ')
plt.plot(CPV['aoi'],Curvas_['p_mp'],'o',markersize=2,label='Sin IAM')
plt.plot(CPV['aoi'],Curvas['p_mp'],'o',markersize=2,label='IAM_tercer_grado')
plt.plot(CPV['aoi'],Potencia,'o',markersize=2,label='UF')
plt.xlabel('Ángulo de incidencia (°)')
plt.ylabel('Puntos de máxima potencia (W)')
plt.title('Comparación de los resultados con los datos estimados de potencias en funcion del iam')
plt.legend()
--------------------------------------------------------------------------------------------------------------------'''

#%% COMPROBAMOS SI FUNCIONAN LOS MÉTODOS

Data_iam=pd.read_excel('C://Users/juanj/OneDrive/Escritorio/TFG/datos_para_calcular.xlsx',sheet_name='Cálculo_iam_CPV',encoding='utf-8')
Data_am=pd.read_excel('C://Users/juanj/OneDrive/Escritorio/TFG/datos_para_calcular.xlsx',sheet_name='Cálculo_uf_am_CPV',encoding='utf-8')
Data_temp=pd.read_excel('C://Users/juanj/OneDrive/Escritorio/TFG/datos_para_calcular.xlsx',sheet_name='Cálculo_uf_temp_CPV',encoding='utf-8')



Mi_CPV.generate_iam_parameters(Data_iam['aoi'].values, Data_iam['ISC_IIIV/DII (A m2/W)'].values)
CPV['DII_efectiva_tercer_grado (W/m2)']=CPV['DII (W/m2)']*Mi_CPV.get_iam(CPV['aoi'],iam_model='Tercer grado')

temp_cell=Mi_CPV.pvsyst_celltemp(poa_global=CPV['DII_efectiva_tercer_grado (W/m2)'], temp_air=CPV['T_Amb (°C)'], wind_speed=CPV['Wind Speed (m/s)']) 
temp_cell_=Mi_CPV.pvsyst_celltemp(poa_global=CPV['DII (W/m2)'], temp_air=CPV['T_Amb (°C)'], wind_speed=CPV['Wind Speed (m/s)'])

Five_parameters=Mi_CPV.calcparams_cpvsyst(CPV['DII_efectiva_tercer_grado (W/m2)'], temp_cell)
Five_parameters_=Mi_CPV.calcparams_cpvsyst(CPV['DII (W/m2)'], temp_cell_)

Curvas=Mi_CPV.singlediode(photocurrent=Five_parameters[0], saturation_current=Five_parameters[1],
                                  resistance_series=Five_parameters[2],resistance_shunt=Five_parameters[3], 
                                  nNsVth=Five_parameters[4],ivcurve_pnts=100, method='lambertw')
Curvas_=Mi_CPV.singlediode(photocurrent=Five_parameters_[0], saturation_current=Five_parameters_[1],
                                  resistance_series=Five_parameters_[2],resistance_shunt=Five_parameters_[3], 
                                  nNsVth=Five_parameters_[4],ivcurve_pnts=100, method='lambertw')

# Mi_CPV.generate_uf_temp_parameters(Data_temp['T_Amb (°C)'].values, Data_temp['ISC_IIIV/DII_efectiva (A m2/W)'].values)

# Mi_CPV.generate_uf_am_parameters(Data_am['airmass'].values, Data_am['ISC_IIIV/DII_efectiva (A m2/W)'].values)
#%%
# Mi_CPV.generate_uf_am_parameters2(Data_am['airmass'].values, Data_am['ISC_IIIV/DII_efectiva (A m2/W)'].values)


#%%


# Mi_CPV.uf_parameters['w_am']=0
# Mi_CPV.uf_parameters['w_temp']=0



# Mi_CPV.calculate_UF(CPV['airmass_relative'].values, CPV['T_Amb (°C)'].values, Curvas['p_mp'], CPV['PMP_estimated_IIIV (W)'].values)


#%% YA QUE HAY DOS METODOS PARA EL UF_AM HAY QUE COMPARARLOS NO SOLO CON EL RMSE



Mi_CPV.uf_parameters={'m1_am':0.172793, 'thld_am':1.285187 ,'m2_am':-0.408000,
                      'm_temp':-0.006439, 'thld_temp':15.18,
                      'w_am':0.422,'w_temp': 0.492}

Potencia_1=Curvas['p_mp']*Mi_CPV.get_uf(CPV['airmass_relative'].values,CPV['T_Amb (°C)'].values)
Diferencia_1=Potencia_1-CPV['PMP_estimated_IIIV (W)'].values
RMSE_1=E.RMSE(CPV['PMP_estimated_IIIV (W)'].values,Potencia_1)

Intensidad_1=Curvas['i_sc']*Mi_CPV.get_uf(CPV['airmass_relative'].values,CPV['T_Amb (°C)'].values)


Mi_CPV.uf_parameters={'m1_am': 0.18645008054738124,
                      'thld_am': 1.3081866727630114,
                      'm2_am': -0.32677187580032385,
                      'm_temp': -0.006439,
                      'thld_temp': 15.18,
                      'w_am': 0.161,
                      'w_temp': 0.765}

Potencia_2=Curvas['p_mp']*Mi_CPV.get_uf(CPV['airmass_relative'].values,CPV['T_Amb (°C)'].values)
Diferencia_2=Potencia_2-CPV['PMP_estimated_IIIV (W)'].values
RMSE_2=E.RMSE(CPV['PMP_estimated_IIIV (W)'].values,Potencia_2)
Intensidad_2=Curvas['i_sc']*Mi_CPV.get_uf(CPV['airmass_relative'].values,CPV['T_Amb (°C)'].values)

#%%

plt.figure(figsize=(30,15))
plt.plot(CPV['aoi'],Curvas['p_mp'],'o',markersize=2,label='sin UF')
plt.plot(CPV['aoi'],Potencia_1,'o',markersize=2,label='Con UF')
plt.plot(CPV['aoi'],CPV['PMP_estimated_IIIV (W)'],'o',markersize=2,label='Datos ')
plt.xlabel('Ángulo de incidencia (°)')
plt.ylabel('Potencia (III-V)(W)')
plt.title('Comparación de los resultados con los datos estimados de potencias en funcion del UF')
plt.legend()

plt.figure(figsize=(30,15))
plt.plot(CPV['aoi'],Diferencia_1,'o',markersize=4,label='Residuos de las potencias calculadas ')
plt.xlabel('Ángulo de incidencia (°)')
plt.ylabel('Potencia (III-V)(W)')
plt.title('Residuos de las potencias calculadas con los datos estimados')
plt.legend()


plt.figure(figsize=(30,15))
plt.plot(CPV['T_Amb (°C)'],Diferencia_1,'o',markersize=4,label='Residuos de las potencias calculadas ')
plt.xlabel('Temperatura ambiente (°C)')
plt.ylabel('Potencia (III-V)(W)')
plt.title('Residuos de las potencias calculadas con los datos estimados')
plt.legend()

plt.figure(figsize=(30,15))
plt.plot(CPV['airmass_relative'],Diferencia_1,'o',markersize=4,label='Residuos de las potencias calculadas ')
plt.xlabel('airmass (n.d.)')
plt.ylabel('Potencia (III-V)(W)')
plt.title('Residuos de las potencias calculadas con los datos estimados')
plt.legend()

plt.figure(figsize=(30,15))
plt.plot(CPV['aoi'],Curvas['p_mp'],'o',markersize=2,label='sin UF')
plt.plot(CPV['aoi'],Potencia_2,'o',markersize=2,label='Con UF')
plt.plot(CPV['aoi'],CPV['PMP_estimated_IIIV (W)'],'o',markersize=2,label='Datos ')
plt.xlabel('Ángulo de incidencia (°)')
plt.ylabel('Potencia (III-V)(W)')
plt.title('Comparación de los resultados con los datos estimados de potencias en funcion del UF')
plt.legend()

plt.figure(figsize=(30,15))
plt.plot(CPV['aoi'],Diferencia_2,'o',markersize=4,label='Residuos de las potencias calculadas ')
plt.xlabel('Ángulo de incidencia (°)')
plt.ylabel('Potencia (III-V)(W)')
plt.title('Residuos de las potencias calculadas con los datos estimados')
plt.legend()


plt.figure(figsize=(30,15))
plt.plot(CPV['T_Amb (°C)'],Diferencia_2,'o',markersize=4,label='Residuos de las potencias calculadas ')
plt.xlabel('Temperatura ambiente (°C)')
plt.ylabel('Potencia (III-V)(W)')
plt.title('Residuos de las potencias calculadas con los datos estimados')
plt.legend()

plt.figure(figsize=(30,15))
plt.plot(CPV['airmass_relative'],Diferencia_2,'o',markersize=4,label='Residuos de las potencias calculadas ')
plt.xlabel('airmass (n.d.)')
plt.ylabel('Potencia (III-V)(W)')
plt.title('Residuos de las potencias calculadas con los datos estimados')
plt.legend()




#%% LOCALIZED SYSTEM
# #Datos:
# #localización
# lat=40.453
# lon=-3.727
# alt=667
# tz='Europe/Berlin'

# CPV_location=Location(latitude=lat,longitude=lon,tz=tz,altitude=alt)



# localized_Mi_CPV=PVClass.LocalizedCVSystem(Mi_CPV,CPV_location)
# Hola=localized_Mi_CPV.get_iam(CPV['aoi'],iam_model='Tercer grado')

# Hola=localized_Mi_CPV.get_aoi(solar_zenith=Solar_position['zenith'], solar_azimuth=Solar_position['azimuth'])








