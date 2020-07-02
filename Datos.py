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
# Solar_position2=pvlib.solarposition.get_solarposition(Fecha, latitude=lat,
#                                                       longitude=lon, altitude=alt, 
#                                                       pressure=None, method='nrel_numpy', 
#                                                       temperature=df['T_Amb (°C)'])
AOI=pd.DataFrame(pvlib.irradiance.aoi(surface_tilt=surface_tilt, surface_azimuth=surface_azimuth, 
                                      solar_zenith=Solar_position['zenith'], solar_azimuth=Solar_position['azimuth']))
AM=CPV_location.get_airmass(times=Fecha, solar_position=Solar_position,model='simple')
'''PARA COMPARAR LOS DIFEERNTES MODELOS 
AM1=CPV_location.get_airmass(times=Fecha, solar_position=Solar_position,model='simple')
AM2=CPV_location.get_airmass(times=Fecha, solar_position=Solar_position,model='youngirvine1967')

AM3=CPV_location.get_airmass(times=Fecha, solar_position=Solar_position,model='kastenyoung1989')
AM4=CPV_location.get_airmass(times=Fecha, solar_position=Solar_position,model='gueymard1993')
AM5=CPV_location.get_airmass(times=Fecha, solar_position=Solar_position,model='young1994')
AM6=CPV_location.get_airmass(times=Fecha, solar_position=Solar_position,model='pickering2002')


print(AM['airmass_absolute'].min())
print(AM1['airmass_absolute'].min())
print(AM2['airmass_absolute'].min())

print(AM3['airmass_absolute'].min())

print(AM4['airmass_absolute'].min())

print(AM5['airmass_absolute'].min())
print(AM6['airmass_absolute'].min())

print('airmass_relative')
print(AM['airmass_relative'].min())
print(AM1['airmass_relative'].min())
print(AM2['airmass_relative'].min())

print(AM3['airmass_relative'].min())

print(AM4['airmass_relative'].min())

print(AM5['airmass_relative'].min())
print(AM6['airmass_relative'].min())


'''


#%%
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

fig=plt.figure(figsize=(30,20))

plt.plot(df['aoi'],df['DII_mio'],'o',markersize='4',label='dii')   
plt.plot(df['aoi'],df['DII (W/m2)'],'o',markersize='2',label='dii')   


plt.xlabel('Hora')
plt.ylabel('Irradiancia (W/m2)')
plt.legend()

#%%

fig=plt.figure(figsize=(30,20))

plt.plot(df['aoi'],df['PMP_estimated_Si (W)'],'o',label='dni')   


plt.xlabel('Hora')
plt.ylabel('Irradiancia (W/m2)')
plt.legend()


#%%


date=np.array(['2019-05-30'])
for i in range(0,len(df.index.values)):
    if(i==0):
        date[0]=str(df.index[0].date())
    elif(df.index[i-1].date()!=df.index[i].date()):
        date=np.append(date,str(df.index[i].date()))
     
#Para visualizar los datos
pd.plotting.register_matplotlib_converters()#ESTA SENTENCIA ES NECESARIA PARA DIBUJAR DATE.TIMES
for i in date:
    fig=plt.figure(figsize=(30,15))
    fig.add_subplot(121)
    plt.plot(df[str(i)].index[:].time,Irradiancias[str(i)]['dni'],label='dni')   
    plt.plot(df[str(i)].index[:].time,Irradiancias[str(i)]['ghi'],label='ghi')

    plt.xlabel('Hora')
    plt.ylabel('Irradiancia (W/m2)')
    plt.legend()
    plt.title("Irradiancias calculadas "+ str(i))
    fig.add_subplot(122)
    plt.plot(df[str(i)].index[:].time,df[str(i)]['DNI (W/m2)'], label='DNI')    
    plt.plot(df[str(i)].index[:].time,df[str(i)]['GNI (W/m2)'],label='GHI')
    plt.plot(df[str(i)].index[:].time,df[str(i)]['DII (W/m2)'],label='DII')
    plt.plot(df[str(i)].index[:].time,df[str(i)]['GII (W/m2)'],label='GII')
    plt.xlabel('Hora')
    plt.ylabel('Irradiancia (W/m2)')
    plt.legend()
    plt.title("Datos de irradiancias "+str(i))


#df['ISC_IIIV/DII (A m2/W)']=df['ISC_measured_IIIV (A)']/df['DII (W/m2)']
#fig=plt.figure(figsize=(30,15))
#plt.plot(df['airmass_relative'],df['ISC_IIIV/DII (A m2/W)'],'o')  
#plt.ylim(0,0.01) 



df.to_csv("C://Users/juanj/OneDrive/Escritorio/TFG/Entradas.csv")









