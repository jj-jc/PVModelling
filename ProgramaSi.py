# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 12:06:32 2020

@author: juanj
"""

from pvlib.location import Location
import CPVClass
import pandas as pd
import numpy as np
import Error as E
import matplotlib.pyplot as plt

'''
DATOS DE ENTRADA:
    -DNI
    -Air temperature
    -Time 
    -Location 
    -Module config:
'''

# ----------------------------------------DNI, air temperature, time--------------------------------------------
# df=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/Datos_filtrados_IIIV.csv',encoding='utf-8')

df=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/InsolightMay2019.csv',encoding= 'unicode_escape')


df=df.where(df!='   NaN')


# -------------------------------------------Location-----------------------------------------------
lat=40.453
lon=-3.727
alt=667
tz='Europe/Berlin'

location=Location(name= 'IES_location',latitude=lat,longitude=lon,tz=tz,altitude=alt)



#------------------------------------------- Module config----------------------------------------------

surface_tilt=30
surface_azimuth=180

My_Si=CPVClass.Flat_CPVSystem(surface_tilt=surface_tilt, surface_azimuth=surface_azimuth, 
                 AOILIMIT=55.0,
                 albedo=None, surface_type=None,
                 module=None, module_type='glass_polymer',
                 module_Flat_parameters=None,
                 temperature_model_Flat_parameters=None,
                 modules_per_string=1, strings_per_inverter=1,
                 inverter=None, inverter_parameters=None, 
                 losses_parameters=None, name=None,
                 iam_Flat_parameters=None)

My_Si.module_Flat_parameters={'gamma_ref': 2.13, 'mu_gamma': 0.002, 'I_L_ref':2.355,
                'I_o_ref': 0.0000147,'R_sh_ref': 3000, 'R_sh_0':8000,
                'R_sh_exp': 5.5,'R_s': 0.35,'alpha_sc':0.0,'EgRef':1.121,
                'irrad_ref': 400,'temp_ref':25, 'cells_in_series':4,
                'eta_m':0.16, 'alpha_absorption':0.9}

My_Si.temperature_model_Flat_parameters={'u_c': 29.0,'u_v':0}

My_Si.iam_Flat_parameters={'a3': 4.415712058608902e-05,'a2':-0.00870855968202769,
                        'a1':0.5604598483238424,'b':-11.538903897556816,'valor_norm':0.017250317962638585}




#'pdc0': 25,'gamma_pdc':-0.005 son para comprobar que fuuncionen las funcione, pero no esta correctamente seleccionado
My_Si.inverter_parameters={'pdc0': 25, 'eta_inv_nom': 0.96 ,'eta_inv_ref':0.9637}



My_Si_local=CPVClass.LocalizedFlat_CPVSystem(My_Si,location)

#%%

Fecha=pd.DatetimeIndex(df['Date Time'],tz=tz)

Solar_position=location.get_solarposition(Fecha, pressure=None, temperature=df['T_Amb (ºC)'])



AOI=pd.DataFrame(My_Si_local.get_aoi(solar_zenith=Solar_position['zenith'],solar_azimuth=Solar_position['azimuth']))


AM=My_Si_local.get_airmass(times=df['Date Time'].values,solar_position=Solar_position,model='simple')





AM=AM.set_index([pd.Series(df.index)])
AOI=AOI.set_index([pd.Series(df.index)])
df=pd.concat([df,AM['airmass_relative'],AOI],axis=1)






#%%
# estudiamos la parte del silicio >AOILIMIT

greater_AOILIMIT=df[df['aoi']>My_Si_local.AOILIMIT]



#Filtrado de condiciones normales
greater_AOILIMIT=greater_AOILIMIT[(greater_AOILIMIT['PMP_estimated_IIIV (W)']>0.1)]
greater_AOILIMIT=greater_AOILIMIT[(greater_AOILIMIT['T_Amb (ºC)']>10.0)]
#----------velocidad del viento
greater_AOILIMIT=greater_AOILIMIT[(greater_AOILIMIT['Wind Speed (m/s)']<2.5)]
#----------SMR
greater_AOILIMIT=greater_AOILIMIT[(greater_AOILIMIT['SMR_Top_Mid (n.d.)'].astype(float)>0.7)]
greater_AOILIMIT=greater_AOILIMIT[(greater_AOILIMIT['SMR_Top_Mid (n.d.)'].astype(float)<1.1)]
greater_AOILIMIT=greater_AOILIMIT[greater_AOILIMIT['DII (W/m2)']>0] #evitamos problemas de infinitos en la siguiente ejecución

# greater_AOILIMIT['ISC_IIIV/DII (A m2/W)']=greater_AOILIMIT['ISC_measured_IIIV (A)']/greater_AOILIMIT['DII (W/m2)']

#se limpia la gráfica de potencia por medio de la mediana.

greater_AOILIMIT=E.mediana_filter(data=greater_AOILIMIT,colum_intervals='aoi',columna_filter='PMP_estimated_Si (W)',n_intervalos=100,porcent_mediana=15)

greater_AOILIMIT['Difusa']=greater_AOILIMIT['GII (W/m2)']-greater_AOILIMIT['DII (W/m2)']
greater_AOILIMIT=greater_AOILIMIT[greater_AOILIMIT['Difusa']>0]

#Me cargo bastantes valores en este filtrado de mediana, pero la difusa cuanto más pequeña, más claro es el día.
greater_AOILIMIT=E.mediana_filter(data=greater_AOILIMIT,colum_intervals='aoi',columna_filter='Difusa',n_intervalos=5,porcent_mediana=20)



# plt.figure(figsize=(30,15))
# plt.plot(greater_AOILIMIT['aoi'],greater_AOILIMIT['Difusa'],'o',markersize=2,label='Datos ')
# plt.plot(greater_AOILIMIT_['aoi'],greater_AOILIMIT_['Difusa'],'o',markersize=2,label='Datos ')
# plt.xlabel('Ángulo de incidencia (º)')
# plt.ylabel('Potencia (III-V)(W)')
# plt.title('Comparación de los resultados con los datos estimados de potencias en funcion del UF')
# plt.legend()





# greater_AOILIMIT=E.mediana_filter(data=greater_AOILIMIT,colum_intervals='aoi',columna_filter='DII (W/m2)',n_intervalos=20,porcent_mediana=10)




# #%%


#SE CALCULA EL IAM CON LOS PARAMETROS OBTENIDOS
IAM=np.array(My_Si_local.get_iam(greater_AOILIMIT['aoi'].values))
greater_AOILIMIT['DII_efective']=greater_AOILIMIT['DII (W/m2)']*IAM
greater_AOILIMIT['GII_efective']=greater_AOILIMIT['GII (W/m2)']*IAM





greater_AOILIMIT['DII_efective_Difusa']=greater_AOILIMIT['DII_efective']+greater_AOILIMIT['Difusa']
greater_AOILIMIT['GII_efective_Difusa']=greater_AOILIMIT['GII_efective']-greater_AOILIMIT['Difusa']

temp_cell=My_Si_local.pvsyst_celltemp(poa_global=greater_AOILIMIT['DII_efective_Difusa'], temp_air=greater_AOILIMIT['T_Amb (ºC)'], wind_speed=greater_AOILIMIT['Wind Speed (m/s)']) 
temp_cell_=My_Si_local.pvsyst_celltemp(poa_global=greater_AOILIMIT['DII (W/m2)'], temp_air=greater_AOILIMIT['T_Amb (ºC)'], wind_speed=greater_AOILIMIT['Wind Speed (m/s)'])

Five_parameters=My_Si_local.calcparams_pvsyst(greater_AOILIMIT['DII_efective'], temp_cell)
Five_parameters_=My_Si_local.calcparams_pvsyst(greater_AOILIMIT['DII (W/m2)'], temp_cell_)
Five_parameters_gii=My_Si_local.calcparams_pvsyst(greater_AOILIMIT['GII_efective'], temp_cell)
Five_parameters_gii=My_Si_local.calcparams_pvsyst(greater_AOILIMIT['GII_efective'], temp_cell)


Curvas=My_Si_local.singlediode(photocurrent=Five_parameters[0], saturation_current=Five_parameters[1],
                                  resistance_series=Five_parameters[2],resistance_shunt=Five_parameters[3], 
                                  nNsVth=Five_parameters[4],ivcurve_pnts=100, method='lambertw')
Curvas_=My_Si_local.singlediode(photocurrent=Five_parameters_[0], saturation_current=Five_parameters_[1],
                                  resistance_series=Five_parameters_[2],resistance_shunt=Five_parameters_[3], 
                                  nNsVth=Five_parameters_[4],ivcurve_pnts=100, method='lambertw')

Curvas_prueba=My_Si_local.singlediode(photocurrent=Five_parameters_prueba[0], saturation_current=Five_parameters_prueba[1],
                                  resistance_series=Five_parameters_prueba[2],resistance_shunt=Five_parameters_prueba[3], 
                                  nNsVth=Five_parameters_prueba[4],ivcurve_pnts=100, method='lambertw')

#%%
Potencia=Curvas['p_mp']
RMSE=E.RMSE(greater_AOILIMIT['PMP_estimated_IIIV (W)'].values,Potencia)
Potencia_prueba=Curvas_prueba['p_mp']

plt.figure(figsize=(30,15))
plt.plot(greater_AOILIMIT['aoi'],Potencia,'o',markersize=2,label='Calculado')
plt.plot(greater_AOILIMIT['aoi'],greater_AOILIMIT['PMP_estimated_IIIV (W)'],'o',markersize=2,label='Datos ')
plt.plot(greater_AOILIMIT['aoi'],Potencia_prueba,'o',markersize=2,label='Prueba ')
plt.xlabel('Ángulo de incidencia (º)')
plt.ylabel('Potencia (III-V)(W)')
plt.title('Comparación de los resultados con los datos estimados de potencias')
plt.legend()

# Intensidad_1=Curvas['i_sc']*My_CPV_local.get_uf(CPV['airmass_relative'].values,CPV['T_Amb (ºC)'].values)


#%% SE COMPRUEBA LA INTENSIDAD

Intensidad=Curvas['i_sc']
Intensidad_prueba=Curvas_prueba['i_sc']
Diferencia=Intensidad-greater_AOILIMIT['ISC_measured_Si (A)'].values
RMSE=E.RMSE(greater_AOILIMIT['ISC_measured_Si (A)'].values,Intensidad)



plt.figure(figsize=(30,15))
plt.plot(greater_AOILIMIT['aoi'],Intensidad,'o',markersize=2,label='Calculado')
plt.plot(greater_AOILIMIT['aoi'],greater_AOILIMIT['ISC_measured_Si (A)'],'o',markersize=2,label='Datos')
plt.plot(greater_AOILIMIT['aoi'],Intensidad_prueba,'o',markersize=2,label='Prueba')
plt.xlabel('Ángulo de incidencia (º)')
plt.ylabel('Intensidad (A)')
plt.title('Comparación de los resultados con los datos estimados de intensidad')
plt.legend()



#%% TAL CUAL SALE EN EL DIAGRAMA



My_Si.iam_Flat_parameters={'a3':-8.315977512579898e-06,'a2':0.00039212250547851236,
                        'a1':-0.006006260890940105,'b':1,'valor_norm':0.0008938270669770386}

IAM=np.array(My_Si_local.get_iam(greater_AOILIMIT['aoi'].values))


greater_AOILIMIT['DII_efective']=greater_AOILIMIT['DII (W/m2)']*IAM



