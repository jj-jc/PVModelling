
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

filt_df=filt_df[filt_df['DII (W/m2)']>0] #evitamos problemas de infinitos en la siguiente ejecución

filt_df['ISC_Si/GII (A m2/W)']=filt_df['ISC_measured_Si (A)']/filt_df['GII (W/m2)']

filt_df['Difusa']=filt_df['GII (W/m2)']-filt_df['DII (W/m2)']
filt_df['ISC_Si/(GII-DII) (A m2/W)']=filt_df['ISC_measured_Si (A)']/filt_df['Difusa']
filt_df['ISC_Si/Irra_vista (A m2/W)']=filt_df['ISC_Si/GII (A m2/W)']
for i in range(len(filt_df.index[:])):    
    if filt_df.iloc[i]['aoi']<AOI_LIMIT:
        print(i)
        filt_df['ISC_Si/Irra_vista (A m2/W)'][i]=filt_df['ISC_Si/(GII-DII) (A m2/W)'][i]
#

#-----------------------------------------filtrado 

#filtrar con una mediana de ISC_IIIV en pequeños intervaloes de aoi
filt_df2=filt_df
limSup=filt_df['aoi'].max()
limInf=filt_df['aoi'].min()
Rango=limSup-limInf
n_intervalos=100
porcent_mediana=10
incremento=Rango/n_intervalos
for i in range(n_intervalos):
    AUX=filt_df[filt_df['aoi']>limInf+i*incremento]
    AUX=AUX[AUX['aoi']<=limInf+incremento*(1+i)]
    Mediana=Error.mediana(AUX['ISC_measured_Si (A)'])
    DEBAJO=AUX[AUX['ISC_measured_Si (A)']<Mediana*(1-porcent_mediana/100)]   
    filt_df2=filt_df2.drop(DEBAJO.index[:],axis=0)
    ENCIMA=AUX[AUX['ISC_measured_Si (A)']>Mediana*(1+porcent_mediana/100)]
    filt_df2=filt_df2.drop(ENCIMA.index[:],axis=0)




#
'''Este es el código para dibujar la nube de puntos con el filtrado'''
x=filt_df2['aoi']
y1=filt_df2['ISC_Si/GII (A m2/W)']
x_aoi=filt_df2['aoi']
x_temp=filt_df2['T_Amb (°C)']
x_AM=filt_df2['airmass_relative']
#
#Para ver las irradiancias tras el filtrado

date=np.array(['2019-05-30'])
for i in range(0,len(filt_df.index[:])):
    if(i==0):
        date[0]=str(filt_df.index[0].date())
    elif(filt_df.index[i-1].date()!=filt_df.index[i].date()):
        date=np.append(date,str(filt_df.index[i].date()))
for i in date:
    fig=plt.figure(figsize=(30,15))
    fig.add_subplot(121)
    plt.plot(df[i].index[:].time,df[i]['DNI (W/m2)'], label='DNI')    
#    plt.plot(df[i].index[:].time,df[i]['GNI (W/m2)'],label='GHI')
    plt.plot(df[i].index[:].time,df[i]['DII (W/m2)'],label='DII')
    plt.plot(df[i].index[:].time,df[i]['GII (W/m2)'],label='GII')

    plt.xlabel('Hora')
    plt.ylabel('Irradiancia (W/m2)')
    plt.legend()
    plt.title("Datos de irradiancias "+ str(i))
    fig.add_subplot(122)
    plt.plot(filt_df2[i].index[:].time,filt_df2[i]['DNI (W/m2)'], label='DNI')    
#    plt.plot(filt_df[i].index[:].time,filt_df[i]['GNI (W/m2)'],label='GHI')
    plt.plot(filt_df2[i].index[:].time,filt_df2[i]['DII (W/m2)'],label='DII')
    plt.plot(filt_df2[i].index[:].time,filt_df2[i]['GII (W/m2)'],label='GII')
    plt.xlabel('Hora')
    plt.ylabel('Irradiancia (W/m2)')
    plt.legend()
    plt.title("Datos de irradiancias filtrados "+str(i))






#AOI
fig, ax=plt.subplots(figsize=(30,15))
#ax.plot(filt_df['aoi'],filt_df['ISC_IIIV/DII (A m2/W)'],'o',markersize=3)
ax.plot(x_aoi,y1,'o',markersize=2)
#plt.ylim(0,0.0015)
ax.set_xlabel('AOI (°)')
ax.set_ylabel('ISC_Si/GII (A m2/W)')
ax.set_title("ISC_Si/DII en función del ángulo de incidencia",fontsize=20)
plt.legend()
#T_Amb
fig, ax=plt.subplots(figsize=(30,15))
ax.plot(x_temp,y1,'o',markersize=2)
#plt.ylim(0,0.0015)
ax.set_xlabel('T_Amb (°C)')
ax.set_ylabel('ISC_Si/GII (A m2/W)')
ax.set_title("ISC_Si/GII en función de la temperarua ambiente",fontsize=20)
plt.legend()
#airmass_relative
fig, ax=plt.subplots(figsize=(30,15))
ax.plot(x_AM,y1,'o',markersize=2)
#plt.ylim(0,0.0015)
ax.set_xlabel('airmass_relative')
ax.set_ylabel('ISC_Si/GII (A m2/W)')
ax.set_title("ISC_Si/GII en función del airmass",fontsize=20)
plt.legend()




#creamos un scalar mapeable por cada tercera variable a estudiar.
#Temp
norm=plt.Normalize(filt_df2['T_Amb (°C)'].min(),filt_df2['T_Amb (°C)'].max())
cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["blue","violet","red"])
Mappable_Temp=matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap)
#aoi
norm=plt.Normalize(filt_df2['aoi'].min(),filt_df2['aoi'].max())
cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["blue","violet","red"])
Mappable_aoi=matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap)
#airmass
norm=plt.Normalize(filt_df2['airmass_relative'].min(),filt_df2['airmass_relative'].max())
cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["blue","violet","red"])
Mappable_airmass=matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap)








#representacion del aoi con el scalar mapeable
fig, ax = plt.subplots(1,1,figsize=(30,20))
ax.scatter(x=filt_df2['aoi'],y=filt_df2['ISC_Si/GII (A m2/W)'],c=filt_df2['T_Amb (°C)'],cmap=Mappable_Temp.cmap, norm=Mappable_Temp.norm,s=10)
#plt.ylim(0,0.0012)
#plt.xlim(10,60)
ax.set_xlabel('aoi (°)')
ax.set_ylabel('ISC_Si/GII (A m2/W)')
ax.set_title("ISC_si/GII en función del ángulo de incidencia y la temperatura")
(fig.colorbar(Mappable_Temp)).set_label('Temperatura ambiente (°C)')
plt.show()
#representacion del airmass con el scalar mapeable
fig, ax = plt.subplots(1,1,figsize=(30,20))
ax.scatter(x=filt_df2['airmass_relative'],y=filt_df2['ISC_Si/GII (A m2/W)'],c=filt_df2['T_Amb (°C)'], cmap=Mappable_Temp.cmap, norm=Mappable_Temp.norm,s=10)
#plt.ylim(0,0.0012)
#plt.xlim(1,2)
ax.set_xlabel('airmass')
ax.set_ylabel('ISC_Si/GII (A m2/W)')
ax.set_title("ISC_Si/GII en función de la masa de aire y la temperatura")
(fig.colorbar(Mappable_Temp)).set_label('Temperatura ambiente (°C) ')
plt.show()

#representacion del airmass con el scalar mapeable
fig, ax = plt.subplots(1,1,figsize=(30,20))
ax.scatter(x=filt_df2['airmass_relative'],y=filt_df2['ISC_Si/GII (A m2/W)'],c=filt_df2['aoi'], cmap=Mappable_aoi.cmap, norm=Mappable_aoi.norm,s=10)
#plt.ylim(0,0.0012)
#plt.xlim(1,2)
ax.set_xlabel('airmass')
ax.set_ylabel('ISC_Si/GII (A m2/W)')
ax.set_title("ISC_Si/GII en función de la masa de aire y la temperatura")
(fig.colorbar(Mappable_aoi)).set_label('aoi ')
plt.show()



#representamos de la temp con el scalar mapeable
fig, ax = plt.subplots(1,1,figsize=(30,20))
ax.scatter(x=filt_df2['T_Amb (°C)'],y=filt_df2['ISC_Si/GII (A m2/W)'],c=filt_df2['aoi'], cmap=Mappable_aoi.cmap, norm=Mappable_aoi.norm,s=10)
#plt.ylim(0,0.0012)
#plt.xlim(1,2)
ax.set_xlabel('Temperatura')
ax.set_ylabel('ISC_Si/GII (A m2/W)')
ax.set_title("ISC_Si/GII en función de la temperatura y el ángulo de incidencia")
(fig.colorbar(Mappable_aoi)).set_label('Ángulo de incidencia (°)')
plt.show()


#representacion del aoi con el scalar mapeable
fig, ax = plt.subplots(1,1,figsize=(30,20))
ax.scatter(x=filt_df2['aoi'],y=filt_df2['ISC_Si/Irra_vista (A m2/W)'],c=filt_df2['T_Amb (°C)'],cmap=Mappable_Temp.cmap, norm=Mappable_Temp.norm,s=10)
#plt.ylim(0,0.0012)filt_df['ISC_Si/Irra_vista (A m2/W)'][i]
#plt.xlim(10,60)
ax.set_xlabel('aoi (°)')
ax.set_ylabel('ISC_Si/Irradiancia vista por la célula (A m2/W)')
ax.set_title("ISC_Si/Irradiancia vista por la célula en función del ángulo de incidencia y la temperatura")
(fig.colorbar(Mappable_Temp)).set_label('Temperatura ambiente (°C)')
plt.show()






#
filt_df2.to_csv("C://Users/juanj/OneDrive/Escritorio/TFG/Datos_filtrados_Si.csv",encoding='utf-8')
#
#
#



