import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pvlib 


df=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/InsolightMay2019.csv',encoding= 'unicode_escape')
#Datos del módulo CPV
#localización
lat=40.453
lon=-3.727
alt=667
tz='Europe/Berlin'
#orientación
surface_tilt=30
surface_azimuth=180
#definicion de pvsystem
#Sistema=pvlib.pvsystem.PVSystem(surface_tilt=surface_tilt, surface_azimuth=surface_azimuth)
#localiamos el sistema
CPV_location=pvlib.location.Location(latitude=lat,longitude=lon,tz=tz,altitude=alt)
#definicion del modulo, en principio no hace falta ya que no se va a usar el modelo SAPM
# Modulo=pvlib.modelchain.ModelChain(system=Sistema, location=CPV_location, dc_model='cec')
#Calculamos la posicion solar
Solar_position=CPV_location.get_solarposition(times=df['Date Time'], pressure=None, temperature=df['T_Amb (°C)'])
AOI=pd.DataFrame(pvlib.irradiance.aoi(surface_tilt=surface_tilt, surface_azimuth=surface_azimuth, 
                                      solar_zenith=Solar_position['zenith'], solar_azimuth=Solar_position['azimuth']))
AM=CPV_location.get_airmass(times=df['Date Time'], solar_position=Solar_position)
ISC_DII=pd.Series(df['ISC_measured_IIIV (A)']/df['DII (W/m2)'])
AM=AM.set_index([pd.Series(df.index)])
AOI=AOI.set_index([pd.Series(df.index)])





#ISC_DII=ISC_DII.set_index([pd.Series(df.index)])
df=pd.concat([df,AM,AOI,ISC_DII],axis=1)
df=df.rename(columns={0:'ISC/DII'})
#Criterios de filtrado para datos del III-V
#Potencia estimada <0.001 ( un valor tan bajo no aporta información, de hecho puede empeorar el estudio)
#angulo de incidencia >50 (Traking range)
#criterios de Marcos, SMR, DNI,AM,viento

filt_df=df[(df['PMP_estimated_IIIV (W)']>0.001)]
filt_df=filt_df[(filt_df['aoi']<90.00)]
#En la base de datos estaba con dos espacios"
filt_df=filt_df[(filt_df['SMR_Top_Mid (n.d.)']!='   NaN')]
filt_df[['SMR_Top_Mid (n.d.)']] = filt_df[['SMR_Top_Mid (n.d.)']].apply(pd.to_numeric)
filt_df=filt_df[(filt_df['SMR_Top_Mid (n.d.)']<1.10)]
filt_df=filt_df[(filt_df['SMR_Top_Mid (n.d.)']>0.7)]
filt_df=filt_df[(filt_df['DII (W/m2)']>600.00)]
filt_df=filt_df[(filt_df['Wind Speed (m/s)']<10.00)]
filt_df=filt_df[(filt_df['airmass_relative']<10.00)]
filt_df=filt_df.set_index(np.arange(0,len(filt_df)))

'''vemos los datos representados tras el primer filtrado'''


'''Este es el código para dibujar la nube de puntos con el filtrado'''
x=filt_df['aoi']
y1=filt_df['ISC/DII']
x_aoi=filt_df['aoi']
x_temp=filt_df['T_Amb (°C)']
x_AM=filt_df['airmass_relative']

#AOI
fig, ax=plt.subplots(figsize=(10,7))
ax.plot(x_aoi,y1,'o',markersize=2)
#plt.ylim(0,0.0015)
ax.set_xlabel('AOI (°)')
ax.set_ylabel('ISC_measured_IIIV/DII (A m2/W)')
ax.set_title("Datos")
plt.legend()
#T_Amb
fig, ax=plt.subplots(figsize=(10,7))
ax.plot(x_temp,y1,'o',markersize=2)
#ax.ylimit(0,0.0015)
ax.set_xlabel('T_Amb (°C)')
ax.set_ylabel('ISC_measured_IIIV/DII (A m2/W)')
ax.set_title("Datos")
plt.legend()
#airmass_relative
fig, ax=plt.subplots(figsize=(10,7))
ax.plot(x_AM,y1,'o',markersize=2)
#ax.ylimit(0,0.0015)
ax.set_xlabel('airmass_relative')
ax.set_ylabel('ISC_measured_IIIV/DII (A m2/W)')
ax.set_title("Datos")
plt.legend()

#
#'''Potencias'''
#
#y1=filt_df['PMP_estimated_IIIV (W)']
#y2=filt_df['PMP_estimated_Si (W)']
#x_aoi=filt_df['aoi']
#x_temp=filt_df['T_Amb (°C)']
#x_AM=filt_df['airmass_relative']
#
##Potencia en función del aoi
#fig, ax=plt.subplots(figsize=(10,7))
#ax.plot(x_aoi,y1,'o',markersize=2,label='PMP_estimated_IIIV (W)')
#ax.plot(x_aoi,y2,'o',markersize=2,label='PMP_estimated_Si (W)')
##ax.ylimit(0,0.0015)
#ax.set_xlabel('AOI (°)')
#ax.set_ylabel('Potencia (W)')
#ax.set_title("Potencias en función de AOI")
#plt.legend()
#
#
#
#fig, ax=plt.subplots(figsize=(10,7))
#ax.plot(x_temp,y1,'o',markersize=2,label='PMP_estimated_IIIV (W)')
#ax.plot(x_temp,y2,'o',markersize=2,label='PMP_estimated_Si (W)')
##ax.ylimit(0,0.0015)
#ax.set_xlabel('Temp (°C)')
#ax.set_ylabel('Potencia (W)')
#ax.set_title("Potencias en función de Temp")
#plt.legend()
#
#
#fig, ax=plt.subplots(figsize=(10,7))
#ax.plot(x_AM,y1,'o',markersize=2,label='PMP_estimated_IIIV (W)')
#ax.plot(x_AM,y2,'o',markersize=2,label='PMP_estimated_Si (W)')
##ax.ylimit(0,0.0015)
#ax.set_xlabel('Airmass')
#ax.set_ylabel('Potencia (W)')
#ax.set_title("Potencias en función de Airmass")
#plt.legend()




'''Hay que mejorar el filtrado'''


filt_df=filt_df[(filt_df['ISC/DII']<0.0012)]
filt_df=filt_df[(filt_df['ISC/DII']>0.0004)]
media_ISCDII=filt_df['ISC/DII'].mean()
limit_sup=media_ISCDII+0.0003
limit_inf=media_ISCDII-0.0003
filt_df=filt_df[filt_df['ISC/DII']>limit_inf]
filt_df=filt_df[filt_df['ISC/DII']<limit_sup]




'''Este es el código para dibujar la nube de puntos con el filtrado'''
x=filt_df['aoi']
y1=filt_df['ISC/DII']
x_aoi=filt_df['aoi']
x_temp=filt_df['T_Amb (°C)']
x_AM=filt_df['airmass_relative']


#AOI
fig, ax=plt.subplots(figsize=(10,7))
ax.plot(x_aoi,y1,'o',markersize=2)
ax.set_ylim(0,0.0015)
ax.set_xlabel('AOI (°)')
ax.set_ylabel('ISC_measured_IIIV/DII (A m2/W)')
ax.set_title("Datos")
plt.legend()
#T_Amb
fig, ax=plt.subplots(figsize=(10,7))
ax.plot(x_temp,y1,'o',markersize=2)
ax.set_ylim(0,0.0015)
ax.set_xlabel('T_Amb (°C)')
ax.set_ylabel('ISC_measured_IIIV/DII (A m2/W)')
ax.set_title("Datos")
plt.legend()
#airmass_relative
fig, ax=plt.subplots(figsize=(10,7))
ax.plot(x_AM,y1,'o',markersize=2)
ax.set_ylim(0,0.0015)
ax.set_xlabel('airmass_relative')
ax.set_ylabel('ISC_measured_IIIV/DII (A m2/W)')
ax.set_title("Datos")
plt.legend()

'''Potencias'''

y1=filt_df['PMP_estimated_IIIV (W)']
#y2=filt_df['PMP_estimated_Si (W)']
x_aoi=filt_df['aoi']
x_temp=filt_df['T_Amb (°C)']
x_AM=filt_df['airmass_relative']

#Potencia en función del aoi
fig, ax=plt.subplots(figsize=(10,7))
ax.plot(x_aoi,y1,'o',markersize=2,label='PMP_estimated_IIIV (W)')
#ax.plot(x_aoi,y2,'o',markersize=2,label='PMP_estimated_Si (W)')
#ax.ylimit(0,0.0015)
ax.set_xlabel('AOI (°)')
ax.set_ylabel('Potencia (W)')
ax.set_title("Potencias en función de AOI")
plt.legend()


#Potencia en función de la temp
fig, ax=plt.subplots(figsize=(10,7))
ax.plot(x_temp,y1,'o',markersize=2,label='PMP_estimated_IIIV (W)')
#ax.plot(x_temp,y2,'o',markersize=2,label='PMP_estimated_Si (W)')
#ax.ylimit(0,0.0015)
ax.set_xlabel('Temp (°C)')
ax.set_ylabel('Potencia (W)')
ax.set_title("Potencias en función de Temp")
plt.legend()

#Potencia en función del airmass
fig, ax=plt.subplots(figsize=(10,7))
ax.plot(x_AM,y1,'o',markersize=2,label='PMP_estimated_IIIV (W)')
#ax.plot(x_AM,y2,'o',markersize=2,label='PMP_estimated_Si (W)')
#ax.ylimit(0,0.0015)
ax.set_xlabel('Airmass')
ax.set_ylabel('Potencia (W)')
ax.set_title("Potencias en función de Airmass")
plt.legend()

'''decido crear otro excel con los datos ya filtrados, para mayor comodidad'''

filt_df.to_excel("C://Users/juanj/OneDrive/Escritorio/TFG/Datos_filtrados.xlsx")











