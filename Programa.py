# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 11:33:08 2020

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
My_CPV=CPVClass.CPVSystem(surface_tilt=30, surface_azimuth=180,
                 AOILIMIT=55.0,albedo=None, surface_type=None,
                 module=None, module_type='glass_polymer',
                 module_parameters=None,
                 temperature_model_parameters=None,
                 modules_per_string=1, strings_per_inverter=1,
                 inverter=None, inverter_parameters=None,
                 racking_model='open_rack', losses_parameters=None, name=None,
                 iam_parameters=None)

My_CPV.module_CPV_parameters={'gamma_ref': 5.524, 'mu_gamma': 0.003, 'I_L_ref':0.96,
                'I_o_ref': 0.00000000017,'R_sh_ref': 5226, 'R_sh_0':21000,
                'R_sh_exp': 5.50,'R_s': 0.01,'alpha_sc':0.00,'EgRef':3.91,
                'irrad_ref': 1000,'temp_ref':25, 'cells_in_series':12,
                'eta_m':0.32, 'alpha_absorption':0.9, 'pdc0': 25,'gamma_pdc':-0.005 }

My_CPV.temperature_model_parameters={'u_c': 10.0,'u_v':0}

My_CPV.iam_CPV_parameters={'a3':-8.315977512579898e-06,'a2':0.00039212250547851236,
                        'a1':-0.006006260890940105,'valor_norm':0.0008938270669770386}



My_CPV.uf_parameters={'m1_am':0.172793, 'thld_am':1.285187 ,'m2_am':-0.408000,
                      'm_temp':-0.006439, 'thld_temp':15.18,
                      'w_am':0.41400000000000003,'w_temp': 0.464}

#'pdc0': 25,'gamma_pdc':-0.005 son para comprobar que fuuncionen las funcione, pero no esta correctamente seleccionado
My_CPV.inverter_parameters={'pdc0': 25, 'eta_inv_nom': 0.96 ,'eta_inv_ref':0.9637}



My_CPV_local=CPVClass.LocalizedCPVSystem(My_CPV,location)

#%%

Fecha=pd.DatetimeIndex(df['Date Time'],tz=tz)

Solar_position=location.get_solarposition(Fecha, pressure=None, temperature=df['T_Amb (°C)'])



AOI=pd.DataFrame(My_CPV_local.get_aoi(solar_zenith=Solar_position['zenith'],solar_azimuth=Solar_position['azimuth']))


AM=My_CPV_local.get_airmass(times=df['Date Time'].values,solar_position=Solar_position,model='simple')





AM=AM.set_index([pd.Series(df.index)])
AOI=AOI.set_index([pd.Series(df.index)])
df=pd.concat([df,AM['airmass_relative'],AOI],axis=1)






#%%
# estudiamos la parte del silicio <AOILIMIT

smaller_AOILIMIT=df[df['aoi']<My_CPV_local.AOILIMIT]


#Filtrado de condiciones normales
smaller_AOILIMIT=smaller_AOILIMIT[(smaller_AOILIMIT['PMP_estimated_IIIV (W)']>0.1)]
smaller_AOILIMIT=smaller_AOILIMIT[(smaller_AOILIMIT['T_Amb (°C)']>10.0)]
#----------velocidad del viento
smaller_AOILIMIT=smaller_AOILIMIT[(smaller_AOILIMIT['Wind Speed (m/s)']<2.5)]
#----------SMR
smaller_AOILIMIT=smaller_AOILIMIT[(smaller_AOILIMIT['SMR_Top_Mid (n.d.)'].astype(float)>0.7)]
smaller_AOILIMIT=smaller_AOILIMIT[(smaller_AOILIMIT['SMR_Top_Mid (n.d.)'].astype(float)<1.1)]
smaller_AOILIMIT=smaller_AOILIMIT[smaller_AOILIMIT['DII (W/m2)']>0] #evitamos problemas de infinitos en la siguiente ejecución

smaller_AOILIMIT['ISC_IIIV/DII (A m2/W)']=smaller_AOILIMIT['ISC_measured_IIIV (A)']/smaller_AOILIMIT['DII (W/m2)']

#se limpia la gráfica de potencia por medio de la mediana.

smaller_AOILIMIT=E.mediana_filter(data=smaller_AOILIMIT,colum_intervals='aoi',columna_filter='PMP_estimated_IIIV (W)',n_intervalos=50,porcent_mediana=15)

smaller_AOILIMIT=E.mediana_filter(data=smaller_AOILIMIT,colum_intervals='aoi',columna_filter='DII (W/m2)',n_intervalos=20,porcent_mediana=10)




#%%


#SE CALCULA EL IAM CON LOS PARAMETROS OBTENIDOS
IAM=np.array(My_CPV_local.get_iam(smaller_AOILIMIT['aoi'].values))
smaller_AOILIMIT['DII_efective']=smaller_AOILIMIT['DII (W/m2)']*IAM

temp_cell=My_CPV_local.pvsyst_celltemp(poa_global=smaller_AOILIMIT['DII_efective'], temp_air=smaller_AOILIMIT['T_Amb (°C)'], wind_speed=smaller_AOILIMIT['Wind Speed (m/s)']) 
temp_cell_=My_CPV_local.pvsyst_celltemp(poa_global=smaller_AOILIMIT['DII (W/m2)'], temp_air=smaller_AOILIMIT['T_Amb (°C)'], wind_speed=smaller_AOILIMIT['Wind Speed (m/s)'])

Five_parameters=My_CPV_local.calcparams_cpvsyst(smaller_AOILIMIT['DII_efective'], temp_cell)
Five_parameters_=My_CPV_local.calcparams_cpvsyst(smaller_AOILIMIT['DII (W/m2)'], temp_cell_)

Curvas=My_CPV_local.singlediode(photocurrent=Five_parameters[0], saturation_current=Five_parameters[1],
                                  resistance_series=Five_parameters[2],resistance_shunt=Five_parameters[3], 
                                  nNsVth=Five_parameters[4],ivcurve_pnts=100, method='lambertw')
Curvas_=My_CPV_local.singlediode(photocurrent=Five_parameters_[0], saturation_current=Five_parameters_[1],
                                  resistance_series=Five_parameters_[2],resistance_shunt=Five_parameters_[3], 
                                  nNsVth=Five_parameters_[4],ivcurve_pnts=100, method='lambertw')


#%%
Potencia=Curvas['p_mp']*My_CPV_local.get_uf(smaller_AOILIMIT['airmass_relative'].values,smaller_AOILIMIT['T_Amb (°C)'].values)
Diferencia=Potencia-smaller_AOILIMIT['PMP_estimated_IIIV (W)'].values
RMSE=E.RMSE(smaller_AOILIMIT['PMP_estimated_IIIV (W)'].values,Potencia)

plt.figure(figsize=(30,15))
plt.plot(smaller_AOILIMIT['aoi'],Curvas['p_mp'],'o',markersize=2,label='sin UF')
plt.plot(smaller_AOILIMIT['aoi'],Potencia,'o',markersize=2,label='Con UF')
plt.plot(smaller_AOILIMIT['aoi'],smaller_AOILIMIT['PMP_estimated_IIIV (W)'],'o',markersize=2,label='Datos ')
plt.plot(smaller_AOILIMIT['aoi'],smaller_AOILIMIT['PMP_estimated_IIIV (W)'],'o',markersize=2,label='Datos ')
plt.xlabel('Ángulo de incidencia (°)')
plt.ylabel('Potencia (III-V)(W)')
plt.title('Comparación de los resultados con los datos estimados de potencias en funcion del UF')
plt.legend()

# Intensidad_1=Curvas['i_sc']*My_CPV_local.get_uf(CPV['airmass_relative'].values,CPV['T_Amb (°C)'].values)


#%% SE COMPRUEBA LA INTENSIDAD

Intensidad=Curvas['i_mp']
Diferencia=Intensidad-smaller_AOILIMIT['ISC_measured_IIIV (A)'].values
RMSE=E.RMSE(smaller_AOILIMIT['ISC_measured_IIIV (A)'].values,Intensidad)



plt.figure(figsize=(30,15))
plt.plot(smaller_AOILIMIT['aoi'],Intensidad,'o',markersize=2,label='Calculado')
plt.plot(smaller_AOILIMIT['aoi'],smaller_AOILIMIT['ISC_measured_IIIV (A)'],'o',markersize=2,label='Datos')
plt.xlabel('Ángulo de incidencia (°)')
plt.ylabel('Potencia (III-V)(W)')
plt.title('Comparación de los resultados con los datos estimados de potencias en funcion del UF')
plt.legend()
















