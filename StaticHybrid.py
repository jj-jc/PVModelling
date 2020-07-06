# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 10:12:41 2020

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





#Se construye el objeto CPVSystem

Mi_CPV=CPVClass.CPVSystem(surface_tilt=surface_tilt, surface_azimuth=surface_azimuth,
                 AOILIMIT=AOILIMIT,albedo=None, surface_type=None,
                 module=None, module_type='glass_polymer',
                 module_CPV_parameters=None,
                 temperature_model_CPV_parameters=None,
                 modules_per_string=1, strings_per_inverter=1,
                 inverter=None, inverter_parameters=None,
                 racking_model='open_rack', losses_parameters=None, name=None,
                 iam_CPV_parameters=None)

Mi_CPV.module_CPV_parameters={'gamma_ref': 5.524, 'mu_gamma': 0.003, 'I_L_ref':0.96,
                'I_o_ref': 0.00000000017,'R_sh_ref': 5226, 'R_sh_0':21000,
                'R_sh_exp': 5.50,'R_s': 0.01,'alpha_sc':0.00,'EgRef':3.91,
                'irrad_ref': 1000,'temp_ref':25, 'cells_in_series':12,
                'eta_m':0.32, 'alpha_absorption':0.9, 'pdc0': 25,'gamma_pdc':-0.005 }

Mi_CPV.temperature_model_CPV_parameters={'u_c': 10.0,'u_v':0}

Mi_CPV.iam_CPV_parameters={'a3':-8.315977512579898e-06,'a2':0.00039212250547851236,
                        'a1':-0.006006260890940105,'valor_norm':0.0008938270669770386}



Mi_CPV.uf_parameters={'m1_am':0.172793, 'thld_am':1.285187 ,'m2_am':-0.408000,
                      'm_temp':-0.006439, 'thld_temp':15.18,
                      'w_am':0.41400000000000003,'w_temp': 0.464}

#'pdc0': 25,'gamma_pdc':-0.005 son para comprobar que fuuncionen las funcione, pero no esta correctamente seleccionado
Mi_CPV.inverter_parameters={'pdc0': 25, 'eta_inv_nom': 0.96 ,'eta_inv_ref':0.9637}

Mi_Si_CPV=CPVClass.Flat_CPVSystem(surface_tilt=surface_tilt, surface_azimuth=surface_azimuth,
                 AOILIMIT=AOILIMIT,albedo=None, surface_type=None,
                 module=None, module_type='glass_polymer',
                 module_Flat_parameters=None,
                 temperature_model_Flat_parameters=None,
                 modules_per_string=1, strings_per_inverter=1,
                 inverter=None, inverter_parameters=None,
                 racking_model='open_rack', losses_parameters=None, name=None,
                 iam_Flat_parameters=None)

Mi_Si_CPV.module_Flat_parameters={'gamma_ref': 2.13, 'mu_gamma': 0.002, 'I_L_ref':2.355,
                'I_o_ref': 0.0000147,'R_sh_ref': 3000, 'R_sh_0':8000,
                'R_sh_exp': 5.5,'R_s': 0.35,'alpha_sc':0.0,'EgRef':1.121,
                'irrad_ref': 400,'temp_ref':25, 'cells_in_series':4,
                'eta_m':0.16, 'alpha_absorption':0.9}

Mi_Si_CPV.temperature_model_Flat_parameters={'u_c': 29.0,'u_v':0}

Mi_Si_CPV.iam_Flat_parameters={'a3':0.000121,'a2':-0.023926,
                        'a1':1.539450,'b': 0.03,'valor_norm':0.0008938270669770386}




location=Location(latitude=lat,longitude=lon,tz=tz,altitude=alt)

Localized_Mi_Si_CPV=CPVClass.LocalizedFlat_CPVSystem(Mi_Si_CPV,location)
Localized_Mi_CPV=CPVClass.LocalizedCPVSystem(Mi_CPV,location)
Mi_Hybrid=CPVClass.HybridSystem(Mi_CPV,Mi_Si_CPV)
Localized_Mi_Hybrid=CPVClass.LocalizedHybridSystem(Mi_CPV,location)

