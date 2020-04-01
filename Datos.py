import pandas as pd
import matplotlib.pyplot as plt
import pvlib 
import numpy as np

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

df['DII (W/m2)']=POA['poa_direct']
df['GII (W/m2)']=POA['poa_global']







date=np.array(['2019-05-30'])
for i in range(0,len(df.index[:])):
    if(i==0):
        date[0]=str(df.index[0].date())
    elif(df.index[i-1].date()!=df.index[i].date()):
        date=np.append(date,str(df.index[i].date()))
     
#Para visualizar los datos
for i in date:
    fig=plt.figure(figsize=(30,15))
    fig.add_subplot(121)
    plt.plot(df[i].index[:].time,Irradiancias[i]['dni'],label='dni')   
    plt.plot(df[i].index[:].time,Irradiancias[i]['ghi'],label='ghi')

    plt.xlabel('Hora')
    plt.ylabel('Irradiancia (W/m2)')
    plt.legend()
    plt.title("Irradiancias calculadas "+ str(i))
    fig.add_subplot(122)
    plt.plot(df[i].index[:].time,df[i]['DNI (W/m2)'], label='dni')    
    plt.plot(df[i].index[:].time,df[i]['GNI (W/m2)'],label='gni')
    plt.plot(df[i].index[:].time,df[i]['DII (W/m2)'],label='dii')
    plt.plot(df[i].index[:].time,df[i]['GII (W/m2)'],label='gii')
    plt.xlabel('Hora')
    plt.ylabel('Irradiancia (W/m2)')
    plt.legend()
    plt.title("Datos de irradiancias "+str(i))









#'''decido crear otro excel con los datos ya filtrados, para mayor comodidad'''
##
#df.to_excel("C://Users/juanj/OneDrive/Escritorio/TFG/Datos.xlsx",options={'remove_timezone':True})
##

df.to_csv("C://Users/juanj/OneDrive/Escritorio/TFG/Entradas.csv")









