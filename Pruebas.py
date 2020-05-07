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

AOI_LIMIT=55.0


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




df=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/Entradas.csv')
Fecha=pd.DatetimeIndex(df['Date Time'])
df=df.set_index(Fecha)
df=df.drop(['Date Time'],axis=1)

CPV_location=pvlib.location.Location(latitude=lat,longitude=lon,tz=tz,altitude=alt)
Solar_position=CPV_location.get_solarposition(Fecha, pressure=None, temperature=df['T_Amb (°C)'])

#--------------------------------------------------------criterios de filtrado
#Se elminan los datos NAN
df=df.where(df!='   NaN')
df=df.dropna()
#----------Potencia
filt_df=df[(df['PMP_estimated_IIIV (W)']>0.1)]
#filt_df=df[(df['DII (W/m2)']>100)]
#filt_df=df[(df['T_Amb (°C)']>10)]

Irradiancias=CPV_location.get_clearsky(times=Fecha, model='ineichen', solar_position=Solar_position, dni_extra=None)


date=np.array(['2019-05-30'])
for i in range(0,len(filt_df.index[:])):
    if(i==0):
        date[0]=str(filt_df.index[0].date())
    elif(filt_df.index[i-1].date()!=filt_df.index[i].date()):
        date=np.append(date,str(filt_df.index[i].date()))




#-----------GNI
#de esta forma limpiamos los datos que no pertenezcan a los días claros
Porcentaje=10
for i in filt_df.index[:]:
    Cambio=filt_df.loc[i]['DNI (W/m2)']-Irradiancias.loc[i]['dni']
    if Cambio<=0:
        filt_df=filt_df.drop(i,axis=0)
#----------velocidad del viento
filt_df=filt_df[(filt_df['Wind Speed (m/s)']<10.0)]
        
#----------SMR

filt_df=filt_df[(filt_df['SMR_Top_Mid (n.d.)'].astype(float)>0.7)]
filt_df=filt_df[(filt_df['SMR_Top_Mid (n.d.)'].astype(float)<1.1)]
        
        
        
        
Solar_position=CPV_location.get_solarposition(filt_df.index[:], pressure=None, temperature=filt_df['T_Amb (°C)'])
POA=pvlib.irradiance.get_total_irradiance(surface_tilt=surface_tilt, surface_azimuth=surface_azimuth,
                                          solar_zenith=Solar_position['zenith'], solar_azimuth=Solar_position['azimuth'], 
                                          dni=filt_df['DNI (W/m2)'], ghi=filt_df['GHI (W/m2)'], dhi=filt_df['DHI (W/m2)'],
                                          dni_extra=None, airmass=None, albedo=0.25, surface_type=None, model='isotropic', 
                                          model_perez='allsitescomposite1990')

filt_df['DII (W/m2)']=POA['poa_direct']
filt_df['GII (W/m2)']=POA['poa_global']

filt_df=filt_df[filt_df['DII (W/m2)']>0] #Para evitar problemas de infinitos en la siguiente ejecución

filt_df['ISC_Si/GII (A m2/W)']=filt_df['ISC_measured_Si (A)']/filt_df['GII (W/m2)']
filt_df['Difusa']=filt_df['GII (W/m2)']-filt_df['DII (W/m2)']
filt_df['ISC_Si/(GII-DII) (A m2/W)']=filt_df['ISC_measured_Si (A)']/filt_df['Difusa']
filt_df['ISC_Si/Irra_vista (A m2/W)']=filt_df['ISC_Si/GII (A m2/W)']
for i in range(len(filt_df.index[:])):    
    if filt_df.iloc[i]['aoi']<AOI_LIMIT:
        filt_df['ISC_Si/Irra_vista (A m2/W)'][i]=filt_df['ISC_Si/(GII-DII) (A m2/W)'][i]
#
        
        
        
        
        
        
        
        
