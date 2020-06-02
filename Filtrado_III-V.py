# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 20:46:37 2020

@author: juanj
"""

import numpy as np
import pandas as pd
import math 
import matplotlib.pyplot as plt
import pvlib
import Error 
import matplotlib.colors 
import matplotlib.cm
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default = "browser"
#Datos del módulo CPV
#localización
lat=40.453
lon=-3.727
alt=667
tz='Europe/Berlin'
#orientación
surface_tilt=30
surface_azimuth=180
#AOILIMIt
AOILIMIT=55.0
pd.plotting.register_matplotlib_converters()#ESTA SENTENCIA ES NECESARIA PARA DIBUJAR DATE.TIMES




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
filt_df=df[(df['T_Amb (°C)']>10.0)]
#filt_df=df[(df['DII (W/m2)']>100)]
#filt_df=df[(df['T_Amb (°C)']>10)]

Irradiancias=CPV_location.get_clearsky(times=Fecha, model='ineichen', solar_position=Solar_position, dni_extra=None)


# #-----------DNI 
# #de esta forma limpiamos los datos que no pertenezcan a los días claros
# Porcentaje=5
# for i in filt_df.index[:]:
#     Cambio= abs(filt_df.loc[i]['DNI (W/m2)']-Irradiancias.loc[i]['dni'])
#     if Cambio>=Porcentaje*:
#         filt_df=filt_df.drop(i,axis=0)
#----------velocidad del viento
filt_df=filt_df[(filt_df['Wind Speed (m/s)']<2.5)]
        
#----------SMR

filt_df=filt_df[(filt_df['SMR_Top_Mid (n.d.)'].astype(float)>0.7)]
filt_df=filt_df[(filt_df['SMR_Top_Mid (n.d.)'].astype(float)<1.1)]
        
        
    
filt_df=filt_df[filt_df['DII (W/m2)']>0] #evitamos problemas de infinitos en la siguiente ejecución

filt_df['ISC_IIIV/DII (A m2/W)']=filt_df['ISC_measured_IIIV (A)']/filt_df['DII (W/m2)']




#-----------------------------------------filtrado 

filt_df2=filt_df
limSup=filt_df['aoi'].max()
limInf=filt_df['aoi'].min()
Rango=limSup-limInf
n_intervalos=100
porcent_mediana=15
incremento=Rango/n_intervalos
for i in range(n_intervalos):
    AUX=filt_df[filt_df['aoi']>limInf+i*incremento]
    AUX=AUX[AUX['aoi']<=limInf+incremento*(1+i)]
    Mediana=Error.mediana(AUX['ISC_IIIV/DII (A m2/W)'].values)
    DEBAJO=AUX[AUX['ISC_IIIV/DII (A m2/W)']<(Mediana*(1-porcent_mediana/100))]   
    filt_df2=filt_df2.drop(DEBAJO.index[:],axis=0)
    ENCIMA=AUX[AUX['ISC_IIIV/DII (A m2/W)']>(Mediana*(1+porcent_mediana/100))]
    filt_df2=filt_df2.drop(ENCIMA.index[:],axis=0)


#
'''Este es el código para dibujar la nube de puntos con el filtrado'''
x=filt_df2['aoi']
y1=filt_df2['ISC_IIIV/DII (A m2/W)']
y2=filt_df2['PMP_estimated_IIIV (W)']
x_aoi=filt_df2['aoi']
x_temp=filt_df2['T_Amb (°C)']
x_AM=filt_df2['airmass_absolute']
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
    plt.plot(df[str(i)].index[:].time,df[str(i)]['DNI (W/m2)'], label='DNI')    
#    plt.plot(df[i].index[:].time,df[i]['GNI (W/m2)'],label='GHI')
    plt.plot(df[str(i)].index[:].time,df[str(i)]['DII (W/m2)'],label='DII')
    plt.plot(df[str(i)].index[:].time,df[str(i)]['GII (W/m2)'],label='GII')

    plt.xlabel('Hora')
    plt.ylabel('Irradiancia (W/m2)')
    plt.legend()
    plt.title("Datos de irradiancias "+ str(i))
    fig.add_subplot(122)
    plt.plot(filt_df2[str(i)].index[:].time,filt_df2[str(i)]['DNI (W/m2)'], label='DNI')    
#    plt.plot(filt_df[i].index[:].time,filt_df[i]['GNI (W/m2)'],label='GHI')
    plt.plot(filt_df2[str(i)].index[:].time,filt_df2[str(i)]['DII (W/m2)'],label='DII')
    plt.plot(filt_df2[str(i)].index[:].time,filt_df2[str(i)]['GII (W/m2)'],label='GII')
    plt.xlabel('Hora')
    plt.ylabel('Irradiancia (W/m2)')
    plt.legend()
    plt.title("Datos de irradiancias filtrados "+str(i))






#AOI
fig, ax=plt.subplots(figsize=(30,15))
#ax.plot(filt_df['aoi'],filt_df['ISC_IIIV/DII (A m2/W)'],'o',markersize=3)
ax.plot(x_aoi,y1,'o',markersize=2)
plt.ylim(0,0.0015)
ax.set_xlabel('AOI (°)')
ax.set_ylabel('ISC_measured_IIIV/DII (A m2/W)')
ax.set_title("ISC_IIIV/DII en función del ángulo de incidencia",fontsize=20)
plt.legend()
#T_Amb
fig, ax=plt.subplots(figsize=(30,15))
ax.plot(x_temp,y1,'o',markersize=2)
#plt.ylim(0,0.0015)
ax.set_xlabel('T_Amb (°C)')
ax.set_ylabel('ISC_measured_IIIV/DII (A m2/W)')
ax.set_title("ISC_IIIV/DII en función de la temperarua ambiente",fontsize=20)
plt.legend()
#airmass_absolute
fig, ax=plt.subplots(figsize=(30,15))
ax.plot(x_AM,y1,'o',markersize=2)
#plt.ylim(0,0.0015)
ax.set_xlabel('airmass_absolute')
ax.set_ylabel('ISC_measured_IIIV/DII (A m2/W)')
ax.set_title("ISC_IIIV/DII en función del airmass",fontsize=20)
plt.legend()

#Potencia IIIV
fig, ax=plt.subplots(figsize=(30,15))
ax.plot(x_aoi,y2,'o',markersize=2)
#plt.ylim(0,0.0015)
ax.set_xlabel('AOI (°)')
ax.set_ylabel('PMP_estimated_IIIV (W)')
ax.set_title("Potencia estimada en función del aoi",fontsize=20)
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
norm=plt.Normalize(filt_df2['airmass_absolute'].min(),filt_df2['airmass_absolute'].max())
cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["blue","violet","red"])
Mappable_airmass=matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap)
#velocidad del viento
norm=plt.Normalize(filt_df2['Wind Speed (m/s)'].min(),filt_df2['Wind Speed (m/s)'].max())
cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["blue","violet","red"])
Mappable_viento=matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap)
#dirección del viento
norm=plt.Normalize(filt_df2['Wind Dir. (m/s)'].min(),filt_df2['Wind Dir. (m/s)'].max())
cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["blue","violet","red"])
Mappable_DirViento=matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap)







#representacion del aoi con el scalar mapeable
fig, ax = plt.subplots(1,1,figsize=(30,20))
ax.scatter(x=filt_df2['aoi'],y=filt_df2['ISC_IIIV/DII (A m2/W)'],c=filt_df2['T_Amb (°C)'],cmap=Mappable_Temp.cmap, norm=Mappable_Temp.norm,s=10)
plt.ylim(0,0.0012)
plt.xlim(10,60)
ax.set_xlabel('aoi (°)')
ax.set_ylabel('ISC_measured_IIIV/DII (A m2/W)')
ax.set_title("ISC/DII en función del ángulo de incidencia y la temperatura",fontsize=20)
(fig.colorbar(Mappable_Temp)).set_label('Temperatura ambiente (°C)')
plt.show()
#representacion del airmass con el scalar mapeable
fig, ax = plt.subplots(1,1,figsize=(30,20))
ax.scatter(x=filt_df2['airmass_absolute'],y=filt_df2['ISC_IIIV/DII (A m2/W)'],c=filt_df2['T_Amb (°C)'], cmap=Mappable_Temp.cmap, norm=Mappable_Temp.norm,s=10)
plt.ylim(0,0.0012)
plt.xlim(1,2)
ax.set_xlabel('airmass')
ax.set_ylabel('ISC_measured_IIIV/DII (A m2/W)')
ax.set_title("ISC/DII en función de la masa de aire y la temperatura",fontsize=20)
(fig.colorbar(Mappable_Temp)).set_label('Temperatura ambiente (°C) ')
plt.show()

#representacion del airmass con el scalar mapeable
fig, ax = plt.subplots(1,1,figsize=(30,20))
ax.scatter(x=filt_df2['airmass_absolute'],y=filt_df2['ISC_IIIV/DII (A m2/W)'],c=filt_df2['aoi'], cmap=Mappable_aoi.cmap, norm=Mappable_aoi.norm,s=10)
plt.ylim(0,0.0012)
plt.xlim(1,2)
ax.set_xlabel('airmass')
ax.set_ylabel('ISC_measured_IIIV/DII (A m2/W)')
ax.set_title("ISC/DII en función de la masa de aire y la temperatura",fontsize=20)
(fig.colorbar(Mappable_aoi)).set_label('aoi ')
plt.show()



#representamos de la temp con el scalar mapeable
fig, ax = plt.subplots(1,1,figsize=(30,20))
ax.scatter(x=filt_df2['T_Amb (°C)'],y=filt_df2['ISC_IIIV/DII (A m2/W)'],c=filt_df2['aoi'], cmap=Mappable_aoi.cmap, norm=Mappable_aoi.norm,s=10)
plt.ylim(0,0.0012)
#plt.xlim(1,2)
ax.set_xlabel('Temperatura')
ax.set_ylabel('ISC_measured_IIIV/DII (A m2/W)')
ax.set_title("ISC/DII en función de la temperatura y el ángulo de incidencia",fontsize=20)
(fig.colorbar(Mappable_aoi)).set_label('Ángulo de incidencia (°)')
plt.show()

#%%AQUÍ SE OBSERVA LA DEPENDENCIA CON LA VELOCIDAD DEL VIENTO Y CON LA DIRECION DEL VIENTO


fig, ax = plt.subplots(1,1,figsize=(30,20))
ax.scatter(x=filt_df2['aoi'],y=filt_df2['ISC_IIIV/DII (A m2/W)'],c=filt_df2['Wind Speed (m/s)'], cmap=Mappable_viento.cmap, norm=Mappable_viento.norm,s=10)
plt.ylim(0,0.0012)
#plt.xlim(1,2)
ax.set_xlabel('Ángulo de incidencia (°)')
ax.set_ylabel('ISC_measured_IIIV/DII (A m2/W)')
ax.set_title("ISC/DII en función del ángulo de incidencia y la velocidad del viento",fontsize=20)
(fig.colorbar(Mappable_viento)).set_label('Velocidad del viento (m/s)')
plt.show()

fig, ax = plt.subplots(1,1,figsize=(30,20))
ax.scatter(x=filt_df2['aoi'],y=filt_df2['ISC_IIIV/DII (A m2/W)'],c=filt_df2['Wind Dir. (m/s)'], cmap=Mappable_DirViento.cmap, norm=Mappable_DirViento.norm,s=10)
plt.ylim(0,0.0012)
#plt.xlim(1,2)
ax.set_xlabel('Ángulo de incidencia (°)')
ax.set_ylabel('ISC_measured_IIIV/DII (A m2/W)')
ax.set_title("ISC/DII en función del ángulo de incidencia y la dirección del viento",fontsize=20)
(fig.colorbar(Mappable_DirViento)).set_label('Dirección del viento (°N)')
plt.show()





#%%

filt_df2.to_csv("C://Users/juanj/OneDrive/Escritorio/TFG/Datos_filtrados_IIIV.csv",encoding='utf-8')

#%%
 





filt_df2=filt_df2[filt_df2['aoi']<AOILIMIT]

temp_cell=pvlib.temperature.pvsyst_cell(poa_global=filt_df2['GII (W/m2)'], temp_air=filt_df2['T_Amb (°C)'], wind_speed=filt_df2['Wind Speed (m/s)'], u_c=29.0, u_v=0.0, eta_m=0.1, alpha_absorption=0.9)

fig, ax = plt.subplots(1,1,figsize=(30,20))
ax.scatter(x=temp_cell.values,y=filt_df2['ISC_IIIV/DII (A m2/W)'],c=filt_df2['Wind Speed (m/s)'], cmap=Mappable_viento.cmap, norm=Mappable_viento.norm,s=10)
plt.ylim(0,0.0012)
#plt.xlim(1,2)
ax.set_xlabel('Temperatura')
ax.set_ylabel('ISC_measured_IIIV/DII (A m2/W)')
ax.set_title("ISC/DII en función de la temperatura y el ángulo de incidencia",fontsize=20)
(fig.colorbar(Mappable_viento)).set_label('Ángulo de incidencia (°)')
plt.show()




fig=go.Figure(
data=go.Scatter(
    y=filt_df2['ISC_IIIV/DII (A m2/W)'],
    x=temp_cell.values,
    mode='markers',
    visible=True,
    showlegend=True,
    name='Temperatura '+ str(i)
    ))
fig.update_layout(
    title="Isc_IIIV/DII en función del ángulo de incidencia, divido por intervalos de velocidad de viento",
    xaxis_title="Ángulo de incidencia (°)",
    yaxis_title="ISC_IIIV/DII (A m2/W)",
)

fig.show()






















############################################################LIMPIAR DESDE AQUÍ###########################################################3



"""                                      Otro código de filtrado                           """

#----------------------------------------código que filtra con media y en cada iteración vuelve a calcular la media,


#-------------------------------------------------------
#ErrorPercent=20
##para limipar los valores de DII
#filt_df3=filt_df2
#for i in range(0,len(filt_df2.index[:])):
#    H=filt_df2.index[i].hour
#    Media_Hora=Media_DII.loc[H]['Medias']
#    Cambio=abs(filt_df2.iloc[i]['DII (W/m2)']-Media_Hora)
#    Margen=(ErrorPercent/100)*(Media_Hora)
#    if Cambio>Margen:
#        filt_df3=filt_df3.drop(filt_df2.index[i],axis=0)
#        AUX.loc[H]['Grupo']=AUX.loc[H]['Grupo'].drop(filt_df2.index[i],axis=0)
#        Media_DII.loc[H]['Medias']=AUX.loc[H]['Grupo']['DII (W/m2)'].mean()
#        
#        
#    
#
#
#for i in date:
#    fig=plt.figure(figsize=(20,15))
#    plt.plot(df[i].index[:].time,df[i]['DII (W/m2)'], label='Fecha:'+i)
#    plt.plot(filt_df3[i].index[:].time,filt_df3[i]['DII (W/m2)'], label='Fecha:'+i)
#    
#    plt.xlabel('Hora')
#    plt.ylabel('Irradiancia (W/m2)')
#    plt.legend()
#    plt.title("Irradiancia directa sobre plano inclinado")
#    
#fig=plt.figure(figsize=(20,15))
#plt.plot(Media_DII.index,Media_DII['Medias'])
#plt.xlabel('Hora')
#plt.ylabel('Irradiancia (W/m2)')
#plt.title("Media de irradiancia directa por horas")
#
#
#
#
#




