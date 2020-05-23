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
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pvlib
import Error 
import matplotlib.colors 
import matplotlib.cm

pd.plotting.register_matplotlib_converters()#ESTA SENTENCIA ES NECESARIA PARA DIBUJAR DATE.TIMES
df=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/InsolightMay2019.csv',encoding= 'unicode_escape')


#df=df.loc[:, ['Date Time','DNI (W/m2)','T_Amb (°C)']]
#Datos del módulo CPV
#localización
lat=40.453
lon=-3.727
alt=667
tz='Europe/Berlin'
#orientación
surface_tilt=30
surface_azimuth=180
#localizamos el sistema
CPV_location=pvlib.location.Location(latitude=lat,longitude=lon,tz=tz,altitude=alt)
#Calculamos la posicion solar
Fecha=pd.DatetimeIndex(df['Date Time'],tz=tz)
Solar_position=CPV_location.get_solarposition(Fecha, pressure=None, temperature=df['T_Amb (°C)'])
AOI=pd.DataFrame(pvlib.irradiance.aoi(surface_tilt=surface_tilt, surface_azimuth=surface_azimuth, 
                                      solar_zenith=Solar_position['zenith'], solar_azimuth=Solar_position['azimuth']))
AM=CPV_location.get_airmass(times=Fecha, solar_position=Solar_position)
Irradiancias=CPV_location.get_clearsky(times=Fecha, model='ineichen', solar_position=None, dni_extra=None)

AM=AM.set_index([pd.Series(df.index)])
AOI=AOI.set_index([pd.Series(df.index)])
df=pd.concat([df,AM['airmass_relative'],AOI],axis=1)
df=df.set_index(Fecha)
df=df.drop(['Date Time'],axis=1)
df['GHI (W/m2)']=Irradiancias['ghi']
df['DHI (W/m2)']=Irradiancias['dhi']
#código para identificar los dia
POA=pvlib.irradiance.get_total_irradiance(surface_tilt=surface_tilt, surface_azimuth=surface_azimuth,
                                          solar_zenith=Solar_position['zenith'], solar_azimuth=Solar_position['azimuth'], 
                                          dni=df['DNI (W/m2)'], ghi=df['GHI (W/m2)'], dhi=df['DHI (W/m2)'],
                                          dni_extra=None, airmass=None, albedo=0.25, surface_type=None, model='isotropic', 
                                          model_perez='allsitescomposite1990')

df['DII_mio']=POA['poa_direct']
df['GII_mio']=POA['poa_global']


fig=plt.figure(figsize=(30,15))
plt.plot(df['2019-05-30'].index[:].time,df['2019-05-30']['GII_mio'],label='mio')   
plt.plot(df['2019-05-30'].index[:].time,df['2019-05-30']['GII (W/m2)'],label='datos')
plt.legend()



        
        
        
        
        
        
        
