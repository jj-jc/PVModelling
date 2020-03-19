import pandas as pd
import matplotlib.pyplot as plt
import pvlib 
import numpy as np

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
#localizamos el sistema
CPV_location=pvlib.location.Location(latitude=lat,longitude=lon,tz=tz,altitude=alt)
#Calculamos la posicion solar
Fecha=pd.DatetimeIndex(df['Date Time'],tz=tz)

Solar_position=CPV_location.get_solarposition(Fecha, pressure=None, temperature=df['T_Amb (°C)'])
AOI=pd.DataFrame(pvlib.irradiance.aoi(surface_tilt=surface_tilt, surface_azimuth=surface_azimuth, 
                                      solar_zenith=Solar_position['zenith'], solar_azimuth=Solar_position['azimuth']))
AM=CPV_location.get_airmass(times=Fecha, solar_position=Solar_position)
ISC_DII=pd.Series(df['ISC_measured_IIIV (A)']/df['DII (W/m2)'])
#la sentencia anterior puede generar valores infinitos, no provocan errores. Se filtrarán más adelante.
AM=AM.set_index([pd.Series(df.index)])
AOI=AOI.set_index([pd.Series(df.index)])
ISC_Dif=pd.Series(df['ISC_measured_Si (A)'].divide((df['GII (W/m2)']-df['DII (W/m2)'])))
df=pd.concat([df,AM,AOI,ISC_DII,ISC_Dif],axis=1)
df=df.rename(columns={0:'ISC_IIIV/DII (A m2/W)',1:'ISC_Si/Difusa (A m2/W)'})
df=df.set_index(Fecha)
df=df.drop(['Date Time'],axis=1)


#'''Comprobamos los datos y calculos de las variables a usar'''
#Se ha escogido un día al azar
plt.figure(figsize=(10,7))
plt.plot(df["2019-06-01"].index[:].time,df["2019-06-01"]['aoi'])
plt.xlabel('Hora')
plt.ylabel('°')
plt.title("aoi")

plt.figure(figsize=(10,7))
plt.plot(df["2019-06-01"].index[:].time,df["2019-06-01"]['airmass_relative'])
plt.xlabel('Hora')
plt.ylabel('°')
plt.title("airmass relative")

plt.figure(figsize=(10,7))
plt.plot(df["2019-06-01"].index[:].time,df["2019-06-01"]['T_Amb (°C)'])
plt.xlabel('Hora')
plt.ylabel('°C')
plt.title("Temperatura")

plt.figure(figsize=(10,7))
plt.plot(df["2019-06-01"].index[:].time,df["2019-06-01"]['PMP_estimated_IIIV (W)'])
plt.xlabel('Hora')
plt.ylabel('W')
plt.title("Potencia estimada de la parte de IIIV")
plt.figure(figsize=(10,7))
plt.plot(df["2019-06-01"].index[:].time,df["2019-06-01"]['PMP_estimated_Si (W)'])
plt.xlabel('Hora')
plt.ylabel('W')
plt.title("Potencia de la parte de silicio")

plt.figure(figsize=(10,7))
plt.plot(df["2019-06-01"].index[:].time,df["2019-06-01"]['ISC_measured_IIIV (A)'])
plt.xlabel('Hora')
plt.ylabel('A')
plt.title("ISC_IIIV")

plt.figure(figsize=(10,7))
plt.plot(df["2019-06-01"].index[:].time,df["2019-06-01"]['ISC_IIIV/DII (A m2/W)'])
plt.xlabel('Hora')
plt.ylabel('A m2/W')
plt.title("ISC/DII")
plt.ylim([0,0.0015])

plt.figure(figsize=(10,7))
plt.plot(df["2019-06-01"].index[:].time,df["2019-06-01"]['ISC_measured_Si (A)'])
plt.xlabel('Hora')
plt.ylabel('A')
plt.title("ISC_Si")

plt.figure(figsize=(10,7))
plt.plot(df["2019-06-01"].index[:].time,df["2019-06-01"]['ISC_Si/Difusa (A m2/W)'])
plt.xlabel('Hora')
plt.ylabel('A m2/W')
plt.title("ISC_Si/Difusa")

plt.show()


#código para identificar los dia
date=np.array(['2019-05-30'])
for i in range(0,len(df.index[:])):
    if(i==0):
        date[0]=str(df.index[0].date())
    elif(df.index[i-1].date()!=df.index[i].date()):
        date=np.append(date,str(df.index[i].date()))


'''genera solo una figura y representa todos los dias'''
fig=plt.figure(figsize=(20,15))    


for i in date:
    plt.plot(df[i].index[:].time,df[i]['T_Amb (°C)'], label='Fecha:'+i)

plt.xlabel('Hora')
plt.ylabel('A m2/W')
plt.legend()
plt.title("PMP_estimated_IIIV (W)")

 
    

'''genera una figura por cada dia'''
#for i in date:
#    fig=plt.figure(figsize=(20,15))
#    plt.plot(df[i].index[:].time,df[i]['PMP_estimated_IIIV (W)'], label='Fecha:'+i)
#    plt.xlabel('Hora')
#    plt.ylabel('A m2/W')
#    plt.legend()
#    plt.title("PMP_estimated_IIIV (W)")





#
#for i in range
#plt.figure(figsize=(10,7))
#plt.plot(df["2019-06-01"].index[:].time,df["2019-06-01"]['PMP_estimated_IIIV (W)'])
#plt.xlabel('Hora')
#plt.ylabel('A m2/W')
#plt.title("ISC_Si/Difusa")






#'''decido crear otro excel con los datos ya filtrados, para mayor comodidad'''
#
#df.to_excel("C://Users/juanj/OneDrive/Escritorio/TFG/Datos.xlsx",options={'remove_timezone':True})
##
#
df.to_csv("C://Users/juanj/OneDrive/Escritorio/TFG/Datos.csv")









