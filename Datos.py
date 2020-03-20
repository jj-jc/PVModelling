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
Difusa=df['GII (W/m2)']-df['DII (W/m2)']
#la sentencia anterior puede generar valores infinitos, no provocan errores. Se filtrarán más adelante.
AM=AM.set_index([pd.Series(df.index)])
AOI=AOI.set_index([pd.Series(df.index)])
ISC_Dif=pd.Series(df['ISC_measured_Si (A)'].divide(Difusa))
df=pd.concat([df,AM,AOI,ISC_DII,Difusa,ISC_Dif],axis=1)
df=df.rename(columns={0:'ISC_IIIV/DII (A m2/W)',1:'DifusaI (W/m2)',2:'ISC_Si/Difusa (A m2/W)'})
df=df.set_index(Fecha)
df=df.drop(['Date Time'],axis=1)


#código para identificar los dia
date=np.array(['2019-05-30'])
for i in range(0,len(df.index[:])):
    if(i==0):
        date[0]=str(df.index[0].date())
    elif(df.index[i-1].date()!=df.index[i].date()):
        date=np.append(date,str(df.index[i].date()))


fig=plt.figure(figsize=(20,15))    
for i in date:
    plt.plot(df[i].index[:].time,df[i]['aoi'], label='Fecha:'+i)
plt.xlabel('Hora')
plt.ylabel('aoi (°)')
plt.legend()
plt.title("Ángulo de incidencia")

fig=plt.figure(figsize=(20,15))    
for i in date:
    plt.plot(df[i].index[:].time,df[i]['airmass_relative'], label='Fecha:'+i)
plt.xlabel('Hora')
plt.ylabel('')
plt.legend()
plt.title("Masa de aire relativa")

fig=plt.figure(figsize=(20,15))    
for i in date:
    plt.plot(df[i].index[:].time,df[i]['T_Amb (°C)'], label='Fecha:'+i)
plt.xlabel('Hora')
plt.ylabel('Temperatura (°C)')
plt.legend()
plt.title("Temperatura ambiente")

fig=plt.figure(figsize=(20,15))    
for i in date:
    plt.plot(df[i].index[:].time,df[i]['DII (W/m2)'], label='Fecha:'+i)
plt.xlabel('Hora')
plt.ylabel('Irradiancia (W/m2)')
plt.legend()
plt.title("Irradiancia directa sobre plano inclinado")

#fig=plt.figure(figsize=(20,15))    
#for i in date:
#    plt.plot(df[i].index[:].time,df[i]['T_Amb (°C)'], label='Fecha:'+i)
#plt.xlabel('Hora')
#plt.ylabel('Temperatura (°C)')
#plt.legend()
#plt.title("Temperatura ambiente")

fig=plt.figure(figsize=(20,15))    
for i in date:
    plt.plot(df[i].index[:].time,df[i]['PMP_estimated_IIIV (W)'], label='Fecha:'+i)
plt.xlabel('Hora')
plt.ylabel('Potencia (W)')
plt.legend()
plt.title("Potencia estimada generada por el III-V")

fig=plt.figure(figsize=(20,15))    
for i in date:
    plt.plot(df[i].index[:].time,df[i]['PMP_estimated_Si (W)'], label='Fecha:'+i)
plt.xlabel('Hora')
plt.ylabel('Potencia (W)')
plt.legend()
plt.title("Potencia estimada generada por el Si")

fig=plt.figure(figsize=(20,15))    
for i in date:
    plt.plot(df[i].index[:].time,df[i]['ISC_measured_IIIV (A)'], label='Fecha:'+i)
plt.xlabel('Hora')
plt.ylabel('Intensidad (A)')
plt.legend()
plt.title("Intensidad de cortocircuito generada por III-V")

fig=plt.figure(figsize=(20,15))    
for i in date:
    plt.plot(df[i].index[:].time,df[i]['ISC_IIIV/DII (A m2/W)'], label='Fecha:'+i)
plt.xlabel('Hora')
plt.ylabel('Intensidad/Irradiancia (A m2/W)')
plt.legend()
plt.title("Intensidad/Irradiancia directa sobre plano inclinado")

fig=plt.figure(figsize=(20,15))    
for i in date:
    plt.plot(df[i].index[:].time,df[i]['ISC_measured_Si (A)'], label='Fecha:'+i)
plt.xlabel('Hora')
plt.ylabel('Intensidad (A)')
plt.legend()
plt.title("Intensidad de cortocircuito generada por Si")

fig=plt.figure(figsize=(20,15))    
for i in date:
    plt.plot(df[i].index[:].time,df[i]['ISC_Si/Difusa (A m2/W)'], label='Fecha:'+i)
plt.xlabel('Hora')
plt.ylabel('Intensidad/Irradiancia (A m2/W)')
plt.legend()
plt.title("Intensidad/Irradiancia difusa sobre plano inclinado")






'''ver una a una la intensidad'''
for i in date:
    fig=plt.figure(figsize=(20,15))
    plt.plot(df[i].index[:].time,df[i]['ISC_measured_IIIV (A)'], label='Fecha:'+i)
    plt.xlabel('Hora')
    plt.ylabel('Intensidad (A)')
    plt.legend()
    plt.title("Intensidad de cortocircuito generada por III-V")

'''ver una a una la intensidad'''
for i in date:
    fig=plt.figure(figsize=(20,15))
    plt.plot(df[i].index[:].time,df[i]['DII (W/m2)'], label='Fecha:'+i)
    plt.xlabel('Hora')
    plt.ylabel('Intensidad (A)')
    plt.legend()
    plt.title("Intensidad de cortocircuito generada por Si")





























'''genera una figura por cada dia'''
#for i in date:
#    fig=plt.figure(figsize=(20,15))
#    plt.plot(df[i].index[:].time,df[i]['PMP_estimated_IIIV (W)'], label='Fecha:'+i)
#    plt.xlabel('Hora')
#    plt.ylabel('A m2/W')
#    plt.legend()
#    plt.title("PMP_estimated_IIIV (W)")


'''todas las gráficas escogiendo el dia'''
##'''Comprobamos los datos y calculos de las variables a usar'''
##Se ha escogido un día al azar
#plt.figure(figsize=(10,7))
#plt.plot(df["2019-06-01"].index[:].time,df["2019-06-01"]['aoi'])
#plt.xlabel('Hora')
#plt.ylabel('°')
#plt.title("aoi")
#
#plt.figure(figsize=(10,7))
#plt.plot(df["2019-06-01"].index[:].time,df["2019-06-01"]['airmass_relative'])
#plt.xlabel('Hora')
#plt.ylabel('°')
#plt.title("airmass relative")
#
#plt.figure(figsize=(10,7))
#plt.plot(df["2019-06-01"].index[:].time,df["2019-06-01"]['T_Amb (°C)'])
#plt.xlabel('Hora')
#plt.ylabel('°C')
#plt.title("Temperatura")
#
#plt.figure(figsize=(10,7))
#plt.plot(df["2019-06-01"].index[:].time,df["2019-06-01"]['PMP_estimated_IIIV (W)'])
#plt.xlabel('Hora')
#plt.ylabel('W')
#plt.title("Potencia estimada de la parte de IIIV")
#plt.figure(figsize=(10,7))
#plt.plot(df["2019-06-01"].index[:].time,df["2019-06-01"]['PMP_estimated_Si (W)'])
#plt.xlabel('Hora')
#plt.ylabel('W')
#plt.title("Potencia de la parte de silicio")
#
#plt.figure(figsize=(10,7))
#plt.plot(df["2019-06-01"].index[:].time,df["2019-06-01"]['ISC_measured_IIIV (A)'])
#plt.xlabel('Hora')
#plt.ylabel('A')
#plt.title("ISC_IIIV")
#
#plt.figure(figsize=(10,7))
#plt.plot(df["2019-06-01"].index[:].time,df["2019-06-01"]['ISC_IIIV/DII (A m2/W)'])
#plt.xlabel('Hora')
#plt.ylabel('A m2/W')
#plt.title("ISC/DII")
#plt.ylim([0,0.0015])
#
#plt.figure(figsize=(10,7))
#plt.plot(df["2019-06-01"].index[:].time,df["2019-06-01"]['ISC_measured_Si (A)'])
#plt.xlabel('Hora')
#plt.ylabel('A')
#plt.title("ISC_Si")
#
#plt.figure(figsize=(10,7))
#plt.plot(df["2019-06-01"].index[:].time,df["2019-06-01"]['ISC_Si/Difusa (A m2/W)'])
#plt.xlabel('Hora')
#plt.ylabel('A m2/W')
#plt.title("ISC_Si/Difusa")
#
#plt.show()









#'''decido crear otro excel con los datos ya filtrados, para mayor comodidad'''
#
#df.to_excel("C://Users/juanj/OneDrive/Escritorio/TFG/Datos.xlsx",options={'remove_timezone':True})
##
#
df.to_csv("C://Users/juanj/OneDrive/Escritorio/TFG/Datos.csv")









