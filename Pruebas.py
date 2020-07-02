# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 11:03:31 2020

@author: juanj
"""


# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 20:46:37 2020

@author: juanj
"""
import CPVClass
import pandas as pd
import numpy as np
import pvlib
# AOILIMIT=55.0
# df=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/Datos_filtrados_IIIV.csv',encoding='utf-8')

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

Mi_PV=pvlib.pvsystem.PVSystem(surface_tilt=surface_tilt, surface_azimuth=surface_azimuth,
                 AOILIMIT=AOILIMIT,albedo=None, surface_type=None,
                 module=None, module_type='glass_polymer',
                 module_parameters=None,
                 temperature_model_parameters=None,
                 modules_per_string=1, strings_per_inverter=1,
                 inverter=None, inverter_parameters=None,
                 racking_model='open_rack', losses_parameters=None, name=None,
                 iam_parameters=None)

location=pvlib.location.Location(latitude=lat,longitude=lon,tz=tz,altitude=alt)
Localized_Mi_PV=pvlib.pvsystem.LocalizedPVSystem(Mi_PV,location)


Mi_CPV=CPVClass.CPVSystem(surface_tilt=surface_tilt, surface_azimuth=surface_azimuth,
                 AOILIMIT=AOILIMIT,albedo=None, surface_type=None,
                 module=None, module_type='glass_polymer',
                 module_parameters=None,
                 temperature_model_parameters=None,
                 modules_per_string=1, strings_per_inverter=1,
                 inverter=None, inverter_parameters=None,
                 racking_model='open_rack', losses_parameters=None, name=None,
                 iam_parameters=None)


Localized_Mi_PV=CPVClass.LocalizedCVSystem(Mi_PV,location)


