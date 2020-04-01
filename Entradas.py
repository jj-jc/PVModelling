# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 17:44:03 2020

@author: juanj
"""


import pandas as pd
import matplotlib.pyplot as plt
import pvlib 
import numpy as np

df=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/InsolightMay2019.csv',encoding= 'unicode_escape')



'''--------------------------------------------------ENTRADAS------------------------------------'''


#----------------------------------------------------System config/Location---------
#Datos del módulo CPV
#localización
lat=40.453
lon=-3.727
alt=667
tz='Europe/Berlin'
#orientación
surface_tilt=30
surface_azimuth=180
#----------------------------------------------------------Module parameters--------------

#----------------------------------------------------------Time-------
Fecha=pd.DatetimeIndex(df['Date Time'],tz=tz)
#----------------------------------------------------------DNI-------
DNI=np.array(df['DNI (W/m2)'])
#----------------------------------------------------------T_Amb
T_amb=np.array(df['T_Amb (°C)'])
#----------------------------------------------------------AM
#localizamos el sistema
CPV_location=pvlib.location.Location(latitude=lat,longitude=lon,tz=tz,altitude=alt)
Solar_position=CPV_location.get_solarposition(Fecha, pressure=None, temperature=df['T_Amb (°C)'])
AM=np.array(CPV_location.get_airmass(times=Fecha, solar_position=Solar_position))
#----------------------------------------------------------GHI
GHI=np.array(df['GNI (W/m2)'])





#Clearsky=CPV_location.get_clearsky(times=Fecha, model='ineichen', solar_position=Solar_position, dni_extra=None)
