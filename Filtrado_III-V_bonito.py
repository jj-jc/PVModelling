# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 20:31:05 2020

@author: juanjo
"""
import pandas as pd
import matplotlib.pyplot as plt
import Error as E
import matplotlib.colors 
import matplotlib.cm
pd.plotting.register_matplotlib_converters()#ESTA SENTENCIA ES NECESARIA PARA DIBUJAR DATE.TIMES
df=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/Entradas.csv')
Fecha=pd.DatetimeIndex(df['Date Time'])
df=df.set_index(Fecha)
df=df.drop(['Date Time'],axis=1)
#------------------------------------criterios de filtrado
#Se elminan los datos NAN
df=df.where(df!='   NaN')
df=df.dropna()
filt_df=df[(df['PMP_estimated_IIIV (W)']>0.1)]
filt_df=df[(df['T_Amb (ºC)']>10.0)]
filt_df=filt_df[(filt_df['Wind Speed (m/s)']<2.5)]
filt_df=filt_df[(filt_df['SMR_Top_Mid (n.d.)'].astype(float)>0.7)]
filt_df=filt_df[(filt_df['SMR_Top_Mid (n.d.)'].astype(float)<1.1)]
filt_df=filt_df[filt_df['DII (W/m2)']>0] 
filt_df['ISC_IIIV/DII (A m2/W)']=filt_df['ISC_measured_IIIV (A)']/filt_df['DII (W/m2)']
filt_df_=filt_df
filt_df=E.mediana_filter(data=filt_df,colum_intervals='aoi',
                         columna_filter='ISC_IIIV/DII (A m2/W)',
                         n_intervalos=100,porcent_mediana=15)
'''  Comparativa del filtrado'''
fig=plt.figure(figsize=(30,15))
plt.ylim(0,0.0015 )
plt.plot(filt_df_['aoi'],filt_df_['ISC_IIIV/DII (A m2/W)'], 'o',markersize='4',label='Sin filtrado')    
plt.plot(filt_df['aoi'],filt_df['ISC_IIIV/DII (A m2/W)'],'o', markersize='2',label='Con filtrado')    
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.xlabel('Ángulo de incidencia (º)',fontsize=30)
plt.ylabel('ISC_IIIV/DII (A m2/W)',fontsize=30)
plt.legend(fontsize=30)
plt.title("Datos de eficiencia de captación en función del ángulo de incidencia",fontsize=40)

fig=plt.figure(figsize=(30,15))
plt.ylim(0,0.0015 )
plt.plot(filt_df_['T_Amb (ºC)'],filt_df_['ISC_IIIV/DII (A m2/W)'], 'o',markersize='4',label='Sin filtrado')    
plt.plot(filt_df['T_Amb (ºC)'],filt_df['ISC_IIIV/DII (A m2/W)'],'o', markersize='2',label='Con filtrado')    
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.xlabel('Temperatura ambiente (ºC)',fontsize=30)
plt.ylabel('ISC_IIIV/DII (A m2/W)',fontsize=30)
plt.legend(fontsize=30)
plt.title("Datos de eficiencia de intensidad en función de la temperatura",fontsize=40)

fig=plt.figure(figsize=(30,15))
plt.ylim(0,0.0015 )
plt.xlim(1,3)
plt.plot(filt_df_['airmass_relative'],filt_df_['ISC_IIIV/DII (A m2/W)'], 'o',markersize='4',label='Sin filtrado')    
plt.plot(filt_df['airmass_relative'],filt_df['ISC_IIIV/DII (A m2/W)'],'o', markersize='2',label='Con filtrado')    
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.xlabel('airmass (n.d.)',fontsize=30)
plt.ylabel('ISC_IIIV/DII (A m2/W)',fontsize=30)
plt.legend(fontsize=30)
plt.title("Datos de eficiencia de intensidad en función del ángulo del airmass",fontsize=40)

fig=plt.figure(figsize=(30,15))
plt.plot(filt_df_['aoi'],filt_df_['PMP_estimated_IIIV (W)'], 'o',markersize='4',label='Sin filtrado')    
plt.plot(filt_df['aoi'],filt_df['PMP_estimated_IIIV (W)'],'o', markersize='2',label='Con filtrado')    
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.xlabel('Ángulo de incidencia (º)',fontsize=30)
plt.ylabel('Potencia (W)',fontsize=30)
plt.legend(fontsize=30)
plt.title("Datos de potencia en función del ángulo de incidencia",fontsize=30)

''' Se estudian los datos por medio de dos variables de estudio por medio de un scalar mapeable'''
#Temp
norm=plt.Normalize(filt_df['T_Amb (ºC)'].min(),filt_df['T_Amb (ºC)'].max())
cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["blue","violet","red"])
Mappable_Temp=matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap)
#aoi
norm=plt.Normalize(filt_df['aoi'].min(),filt_df['aoi'].max())
cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["blue","violet","red"])
Mappable_aoi=matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap)
#airmass
norm=plt.Normalize(filt_df['airmass_relative'].min(),filt_df['airmass_relative'].max())
cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["blue","violet","red"])
Mappable_airmass=matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap)
#velocidad del viento
norm=plt.Normalize(filt_df['Wind Speed (m/s)'].min(),filt_df['Wind Speed (m/s)'].max())
cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["blue","violet","red"])
Mappable_viento=matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap)
#dirección del viento
norm=plt.Normalize(filt_df['Wind Dir. (m/s)'].min(),filt_df['Wind Dir. (m/s)'].max())
cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["blue","violet","red"])
Mappable_DirViento=matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap)


#representacion del aoi con el scalar mapeable
fig, ax = plt.subplots(1,1,figsize=(30,20))
ax.scatter(x=filt_df['aoi'],y=filt_df['ISC_IIIV/DII (A m2/W)'],c=filt_df['T_Amb (ºC)'],cmap=Mappable_Temp.cmap, norm=Mappable_Temp.norm,s=10)
plt.ylim(0,0.0012)
plt.xlim(10,60)
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
ax.set_xlabel('Ángulo de incidencia (º)',fontsize=30)
ax.set_ylabel('ISC_measured_IIIV/DII (A m2/W)',fontsize=30)
ax.set_title("Eficiencia de intensidad en función del ángulo de incidencia y la temperatura",fontsize=40)
color_=fig.colorbar(Mappable_Temp)
color_.set_label('Temperatura ambiente (ºC)',fontsize=30)
color_.ax.tick_params(labelsize=30) 
plt.show()
#representacion del airmass con el scalar mapeable
fig, ax = plt.subplots(1,1,figsize=(30,20))
ax.scatter(x=filt_df['airmass_relative'],y=filt_df['ISC_IIIV/DII (A m2/W)'],c=filt_df['T_Amb (ºC)'], cmap=Mappable_Temp.cmap, norm=Mappable_Temp.norm,s=10)
plt.ylim(0,0.0012)
plt.xlim(1,2)
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
ax.set_xlabel('airmass (n.d.)',fontsize=30)
ax.set_ylabel('ISC_measured_IIIV/DII (A m2/W)',fontsize=30)
ax.set_title("Eficiencia de intensidad en función de la masa de aire y la temperatura",fontsize=40)
color_=fig.colorbar(Mappable_Temp)
color_.set_label('Temperatura ambiente (ºC) ',fontsize=30)
color_.ax.tick_params(labelsize=30) 
plt.show()

#representacion del airmass con el scalar mapeable
fig, ax = plt.subplots(1,1,figsize=(30,20))
ax.scatter(x=filt_df['airmass_relative'],y=filt_df['ISC_IIIV/DII (A m2/W)'],c=filt_df['aoi'], cmap=Mappable_aoi.cmap, norm=Mappable_aoi.norm,s=10)
plt.ylim(0,0.0012)
plt.xlim(1,2)
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
ax.set_xlabel('airmass (n.d.)',fontsize=30)
ax.set_ylabel('ISC_measured_IIIV/DII (A m2/W)',fontsize=30)
ax.set_title("Eficiencia de captación en función de la masa de aire y la temperatura",fontsize=40)
color_=fig.colorbar(Mappable_aoi)
color_.set_label('Ángulo de incidencia (º)',fontsize=30)
color_.ax.tick_params(labelsize=30) 
plt.show()

#representamos de la temp con el scalar mapeable
fig, ax = plt.subplots(1,1,figsize=(30,20))
ax.scatter(x=filt_df['T_Amb (ºC)'],y=filt_df['ISC_IIIV/DII (A m2/W)'],c=filt_df['aoi'], cmap=Mappable_aoi.cmap, norm=Mappable_aoi.norm,s=10)
plt.ylim(0,0.0012)
#plt.xlim(1,2)
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
ax.set_xlabel('Temperatura ambiente (ºC)',fontsize=30)
ax.set_ylabel('ISC_measured_IIIV/DII (A m2/W)',fontsize=30)
ax.set_title("Eficiencia de captación en función de la temperatura y el ángulo de incidencia",fontsize=40)
color_=fig.colorbar(Mappable_aoi)
color_.set_label('Ángulo de incidencia (º)',fontsize=30)
color_.ax.tick_params(labelsize=30) 
plt.show()

fig, ax = plt.subplots(1,1,figsize=(30,20))
ax.scatter(x=filt_df['aoi'],y=filt_df['ISC_IIIV/DII (A m2/W)'],c=filt_df['Wind Speed (m/s)'], cmap=Mappable_viento.cmap, norm=Mappable_viento.norm,s=10)
plt.ylim(0,0.0012)
#plt.xlim(1,2)
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
ax.set_xlabel('Ángulo de incidencia (º)',fontsize=30)
ax.set_ylabel('ISC_measured_IIIV/DII (A m2/W)',fontsize=30)
ax.set_title("Eficiencia de captación en función del ángulo de incidencia y la velocidad del viento",fontsize=40)
color_=fig.colorbar(Mappable_viento)
color_.set_label('Velocidad del viento (m/s)',fontsize=30)
color_.ax.tick_params(labelsize=30) 
plt.show()

fig, ax = plt.subplots(1,1,figsize=(30,20))
ax.scatter(x=filt_df['aoi'],y=filt_df['ISC_IIIV/DII (A m2/W)'],c=filt_df['Wind Dir. (m/s)'], cmap=Mappable_DirViento.cmap, norm=Mappable_DirViento.norm,s=10)
plt.ylim(0,0.0012)
#plt.xlim(1,2)
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
ax.set_xlabel('Ángulo de incidencia (º)',fontsize=30)
ax.set_ylabel('ISC_measured_IIIV/DII (A m2/W)',fontsize=30)
ax.set_title("Eficiencia de captación en función del ángulo de incidencia y la dirección del viento",fontsize=40)
color_=fig.colorbar(Mappable_DirViento)
color_.set_label('Dirección del viento (ºN)',fontsize=30 )
color_.ax.tick_params(labelsize=30) 
plt.show()

''' Una vez satisfechos con el filtrado se guarda en un excel'''

filt_df.to_csv("C://Users/juanj/OneDrive/Escritorio/TFG/Datos_filtrados_IIIV.csv",encoding='utf-8')

