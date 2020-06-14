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

# pd.plotting.register_matplotlib_converters()#ESTA SENTENCIA ES NECESARIA PARA DIBUJAR DATE.TIMES
# # df=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/InsolightMay2019.csv',encoding= 'unicode_escape')


# #df=df.loc[:, ['Date Time','DNI (W/m2)','T_Amb (°C)']]
# #Datos del módulo CPV
# #localización
# lat=40.453
# lon=-3.727
# alt=667
# tz='Europe/Berlin'
# #orientación
# surface_tilt=30
# surface_azimuth=180
# #localizamos el sistema
# CPV_location=pvlib.location.Location(latitude=lat,longitude=lon,tz=tz,altitude=alt)
# #Calculamos la posicion solar


# temperatura=np.arange(20,25,1)

# fecha=pd.Series(['27-Nov-2018 14:24:05','23-Nov-2018 14:24:05'])
# Fecha=pd.DatetimeIndex(fecha,tz=tz)



# Solar_position=CPV_location.get_solarposition(Fecha, pressure=None, temperature=20)



# Irradiancias=CPV_location.get_clearsky(times=Fecha, model='ineichen', solar_position=Solar_position, dni_extra=None)


# AM=CPV_location.get_airmass(times=fecha, solar_position=Solar_position)


# POA=pvlib.irradiance.get_total_irradiance(surface_tilt=surface_tilt, surface_azimuth=surface_azimuth,
#                                           solar_zenith=Solar_position['zenith'], solar_azimuth=Solar_position['azimuth'], 
#                                           dni=Irradiancias['dni'], ghi=Irradiancias['ghi'], dhi=Irradiancias['dhi'],
#                                           dni_extra=None, airmass=AM['airmass_absolute'], albedo=0.25, surface_type=None, model='isotropic', 
#                                           model_perez='allsitescomposite1990')

# Irradiancias['dni']=[892,644]
# Irradiancias['ghi']=[1081,950]


# POA2=pvlib.irradiance.get_total_irradiance(surface_tilt=surface_tilt, surface_azimuth=surface_azimuth,
#                                           solar_zenith=Solar_position['zenith'], solar_azimuth=Solar_position['azimuth'], 
#                                           dni=Irradiancias['dni'], ghi=Irradiancias['ghi'], dhi=Irradiancias['dhi'],
#                                           dni_extra=None, airmass=AM['airmass_absolute'], albedo=0.25, surface_type=None, model='isotropic', 
#                                           model_perez='allsitescomposite1990')

# print(POA2['poa_diffuse'])
        
# print(POA['poa_diffuse'])        
        
#%% 
    
x=filt_cuadro2['aoi'].values
y1=filt_cuadro2['ISC_IIIV/DII (A m2/W)'].values/VALOR_NORMALIZAR
LON=10
incremento=.2
#tenemos que poner el valor inicial
n_val=0.7
k_val=5.0
l_val=0.1

Combinaciones=pd.DataFrame(data=np.zeros(((LON**3)+1,4)), dtype='float32', columns=['n','k','l','RR'])
Combinaciones.iloc[0][0]=n_val
Combinaciones.iloc[0][1]=k_val
Combinaciones.iloc[0][2]=l_val
i=0
j=0
p=0
for i in range(LON):#se ocupará de las centenas, en la base que se ponga de LON
    print(i)
    for j in range(LON):#se ocupará de las decenas
        for p in range(LON):#se ocupará de las unidades
            Combinaciones.iloc[p+LON*j+LON**2*i][3]=Error.Determination_coefficient(y1,np.array(pvlib.iam.physical(aoi=x, n=Combinaciones.iloc[p+LON*j+LON**2*i][0],K=Combinaciones.iloc[p+LON*j+LON**2*i][1], L=Combinaciones.iloc[p+LON*j+LON**2*i][2])))
            Combinaciones.iloc[p+LON*j+LON**2*i+1]=Combinaciones.iloc[p+LON*j+LON**2*i]
            Combinaciones.iloc[p+LON*j+LON**2*i+1][0]=Combinaciones.iloc[p+LON*j+LON**2*i][0]+incremento
        Combinaciones.iloc[p+LON*j+LON**2*i+1][0]=n_val
        Combinaciones.iloc[p+LON*j+LON**2*i+1][1]=Combinaciones.iloc[p+LON*j+LON**2*i][1]+incremento
    Combinaciones.iloc[p+LON*j+LON**2*i+1][0]=n_val
    Combinaciones.iloc[p+LON*j+LON**2*i+1][1]=k_val
    Combinaciones.iloc[p+LON*j+LON**2*i+1][2]=Combinaciones.iloc[p+LON*j+LON**2*i][2]+incremento
Valores=Combinaciones[Combinaciones['RR']==Combinaciones['RR'].max()]
IAM_physical=pvlib.iam.physical(aoi=x, n=float(Valores['n']),K=float(Valores['k']), L=float(Valores['l']))

        
