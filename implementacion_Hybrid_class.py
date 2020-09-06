# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 09:36:22 2020

@author: juanj
"""

import Error as E
from pvlib import atmosphere, irradiance
from pvlib.tools import _build_kwargs
from pvlib.location import Location
import numpy as np
from pvlib import pvsystem
import pandas as pd
import CPVClass

pd.plotting.register_matplotlib_converters()#ESTA SENTENCIA ES NECESARIA PARA DIBUJAR DATE.TIMES
tz='Europe/Berlin'
surface_tilt=30
surface_azimuth=180
#Se construye el sistema CPV
Mi_CPV=CPVClass.CPVSystem(surface_tilt=surface_tilt, surface_azimuth=surface_azimuth,
                 albedo=None, surface_type=None,
                 module=None, 
                 module_parameters=None,
                 temperature_model_parameters=None,
                 modules_per_string=1, strings_per_inverter=1,
                 inverter=None, inverter_parameters=None,
                 losses_parameters=None, name=None,
                 iam_parameters=None)
Mi_CPV.module_CPV_parameters={'gamma_ref': 5.524, 'mu_gamma': 0.003, 'I_L_ref':0.96,
                'I_o_ref': 0.00000000017,'R_sh_ref': 5226, 'R_sh_0':21000,
                'R_sh_exp': 5.50,'R_s': 0.01,'alpha_sc':0.00,'EgRef':3.91,
                'irrad_ref': 1000,'temp_ref':25, 'cells_in_series':12,
                'eta_m':0.32, 'alpha_absorption':0.9, 'pdc0': 25,'gamma_pdc':-0.005 }
Mi_CPV.temperature_model_CPV_parameters={'u_c': 4.5,'u_v':0}

Mi_CPV.module_CPV_parameters={'gamma_ref': 5.524, 'mu_gamma': 0.0004, 'I_L_ref':0.96,
                'I_o_ref': 0.00000000017,'R_sh_ref': 5226, 'R_sh_0':21000,
                'R_sh_exp': 5.50,'R_s': 0.01,'alpha_sc':0.00,'EgRef':3.91,
                'irrad_ref': 1000,'temp_ref':25, 'cells_in_series':12,
                'eta_m':0.32, 'alpha_absorption':0.9, 'pdc0': 25,'gamma_pdc':-0.005 }
Mi_CPV.temperature_model_CPV_parameters={'u_c': 9,'u_v':0}

#Se construye el sistema Flat
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

#LOCALIZED SYSTEM
#Datos:
#localización
lat=40.453
lon=-3.727
alt=667
tz='Europe/Berlin'
#AOILIMIT
AOILIMIT=55.0
# se construye el sistema híbrido
Mi_hybrid=CPVClass.HybridSystem(Mi_CPV,Mi_Si_CPV,AOILIMIT=AOILIMIT)

#ahora es necesario leer los datos fitrados:
df_iam_CPV=pd.read_excel('C://Users/juanj/OneDrive/Escritorio/TFG/datos_para_calcular.xlsx', sheet_name='Cálculo_iam_CPV')
df_uf_am_CPV=pd.read_excel('C://Users/juanj/OneDrive/Escritorio/TFG/datos_para_calcular.xlsx', sheet_name='Cálculo_uf_am_CPV')
df_uf_temp_CPV=pd.read_excel('C://Users/juanj/OneDrive/Escritorio/TFG/datos_para_calcular.xlsx', sheet_name='Cálculo_uf_temp_CPV')
df_iam_Si=pd.read_excel('C://Users/juanj/OneDrive/Escritorio/TFG/datos_para_calcular.xlsx', sheet_name='Cálculo_iam_Si_greater')


Mi_hybrid.generate_iam_parameters(df_iam_CPV['aoi'].values,df_iam_Si['aoi'].values,df_iam_CPV['ISC_IIIV/DII (A m2/W)'].values,df_iam_Si['ISC_Si/Irra_vista (A m2/W)'].values)
Mi_hybrid.generate_uf_parameters(df_uf_am_CPV['airmass'].values,df_uf_am_CPV['ISC_IIIV/DII_efectiva (A m2/W)'].values,df_uf_temp_CPV['T_Amb (ºC)'].values,df_uf_temp_CPV['ISC_IIIV/DII_efectiva (A m2/W)'].values)
df=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/Datos_filtrados_IIIV.csv',encoding='utf-8')
CPV=df[(df['aoi']<=AOILIMIT)]
Fecha=pd.DatetimeIndex(CPV['Date Time'])
CPV=CPV.set_index(Fecha)
CPV=CPV.drop(['Date Time'],axis=1) 
CPV=E.mediana_filter(CPV,'aoi','PMP_estimated_IIIV (W)',200,15)
CPV=E.mediana_filter(data=CPV,colum_intervals='aoi',columna_filter='DII (W/m2)',n_intervalos=20,porcent_mediana=10)

#Parte de CPV
IAM_CPV=Mi_hybrid.get_CPV_iam(CPV['aoi'],iam_model='third degree')
CPV['DII_efectiva (W/m2)']=CPV['DII (W/m2)']*IAM_CPV
temp_CPV=Mi_hybrid.CPV_temp(poa_global=CPV['DII_efectiva (W/m2)'], temp_air=CPV['T_Amb (ºC)'], wind_speed=CPV['Wind Speed (m/s)']) 
Five_parameters=Mi_hybrid.CPV_calcparams(CPV['DII_efectiva (W/m2)'], temp_CPV)
Curvas_CPV=Mi_hybrid.CPV_singlediode(photocurrent=Five_parameters[0], saturation_current=Five_parameters[1],
                                  resistance_series=Five_parameters[2],resistance_shunt=Five_parameters[3], 
                                  nNsVth=Five_parameters[4],ivcurve_pnts=100, method='lambertw')
UF=Mi_hybrid.calculate_uf(CPV['airmass_relative'].values,CPV['T_Amb (ºC)'].values,
                       Curvas_CPV['p_mp'],CPV['PMP_estimated_IIIV (W)'].values)
Potencia=Curvas_CPV['p_mp']*UF
RMSE_potencia=E.RMSE(CPV['PMP_estimated_IIIV (W)'],Potencia)


#%%
#Parte de Si
df=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/filt_df_Si.csv',encoding='utf-8')
Si=df[(df['aoi']>AOILIMIT)]
Fecha=pd.DatetimeIndex(Si['Date Time'])
Si=Si.set_index(Fecha)
Si=Si.drop(['Date Time'],axis=1)
Si=E.mediana_filter(Si,'aoi','PMP_estimated_Si (W)',100,20)

IAM_Flat=Mi_hybrid.get_Flat_iam(Si['aoi'],iam_model='Third degree')
Si['Irra_vista_efectiva (W/m2)']=((Si['Irra_vista (W/m2)'].values)*IAM_Flat)
Si['ISC_Si/Irra_vista_efectiva (A m2/W)']=((Si['ISC_measured_Si (A)'].values)/(Si['Irra_vista_efectiva (W/m2)'].values))
Irradianccia_afecta_temp=Si['Irra_vista_efectiva (W/m2)']+Si['Difusa']
temp_cell=Mi_hybrid.Flat_temp(poa_global=Irradianccia_afecta_temp, temp_air=Si['T_Amb (ºC)'], wind_speed=Si['Wind Speed (m/s)']) 

Five_parameters=Mi_hybrid.Flat_calcparams(Si['Irra_vista_efectiva (W/m2)'], temp_cell)

Curvas=Mi_hybrid.Flat_singlediode(photocurrent=Five_parameters[0], saturation_current=Five_parameters[1],
                                  resistance_series=Five_parameters[2],resistance_shunt=Five_parameters[3], 
                                  nNsVth=Five_parameters[4],ivcurve_pnts=100, method='lambertw')

RMS_potencia=E.RMSE(Si['PMP_estimated_Si (W)'],Curvas['p_mp'])

#El valor obtenido de los RMSE corresponde con el obtenido en el programa elaborado, lo que implica
#que la librería funciona correctamente
