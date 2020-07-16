# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 11:59:44 2020

@author: juanjo
"""
import pandas as pd
import matplotlib.pyplot as plt
import Error as E
import matplotlib.colors 
import matplotlib.cm
pd.plotting.register_matplotlib_converters()#ESTA SENTENCIA ES NECESARIA PARA DIBUJAR DATE.TIMES
AOILIMIT=55.0
df=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/Entradas.csv')
Fecha=pd.DatetimeIndex(df['Date Time'])
df=df.set_index(Fecha)
df=df.drop(['Date Time'],axis=1)
#--------------------------------------------------------criterios de filtrado
#Se elminan los datos NAN
df=df.where(df!='   NaN')
df=df.dropna()
filt_df=df[(df['PMP_estimated_Si (W)']>0.1)]
filt_df=filt_df[(filt_df['Wind Speed (m/s)']<2.5)]
filt_df=filt_df[(filt_df['T_Amb (ºC)']>10.0)]
filt_df=filt_df[filt_df['GII (W/m2)']>0] 
filt_df=filt_df[filt_df['DII (W/m2)']>0] 
filt_df['Difusa']=filt_df['GII (W/m2)']-filt_df['DII (W/m2)']
filt_df=filt_df[filt_df['Difusa']>0]
filt_df['Irra_vista (W/m2)']=filt_df['GII (W/m2)']
for i in range(len(filt_df.index[:])):    
    if filt_df.iloc[i]['aoi']<AOILIMIT:
        filt_df['Irra_vista (W/m2)'][i]=filt_df['Difusa'][i]
filt_df['ISC_Si/Irra_vista (A m2/W)']=filt_df['ISC_measured_Si (A)']/filt_df['Irra_vista (W/m2)']
filt_df_=filt_df
filt_df=E.mediana_filter(data=filt_df,colum_intervals='aoi',
                         columna_filter='Irra_vista (W/m2)',
                         n_intervalos=50,porcent_mediana=50)
filt_df=E.mediana_filter(data=filt_df,colum_intervals='aoi',
                         columna_filter='ISC_measured_Si (A)',
                         n_intervalos=50,porcent_mediana=10)
'''Debido a que quiero cambair los límites de los intervalos es necesario desarrollar la función'''
Datos_filtrados=filt_df
limSup=AOILIMIT
limInf=filt_df['aoi'].min()
Rango=limSup-limInf
n_intervalos=2
porcent_mediana=20
incremento=Rango/n_intervalos
for i in range(n_intervalos):
    AUX=filt_df[filt_df['aoi']>limInf+i*incremento]
    AUX=AUX[AUX['aoi']<=limInf+incremento*(1+i)]
    Mediana=E.mediana(AUX['ISC_Si/Irra_vista (A m2/W)'])
    DEBAJO=AUX[AUX['ISC_Si/Irra_vista (A m2/W)']<Mediana*(1-porcent_mediana/100)]   
    Datos_filtrados=Datos_filtrados.drop(DEBAJO.index[:],axis=0)
    ENCIMA=AUX[AUX['ISC_Si/Irra_vista (A m2/W)']>Mediana*(1+porcent_mediana/100)]
    Datos_filtrados=Datos_filtrados.drop(ENCIMA.index[:],axis=0)
smaller_AOI=filt_df[filt_df['aoi']<AOILIMIT]
filt_smaller_AOI=Datos_filtrados[Datos_filtrados['aoi']<AOILIMIT]

limSup=Datos_filtrados['aoi'].max()
limInf=AOILIMIT
Rango=limSup-limInf
n_intervalos=10
porcent_mediana=10
incremento=Rango/n_intervalos
for i in range(n_intervalos):
    AUX=filt_df[filt_df['aoi']>limInf+i*incremento]
    AUX=AUX[AUX['aoi']<=limInf+incremento*(1+i)]
    Mediana=E.mediana(AUX['ISC_Si/Irra_vista (A m2/W)'])
    DEBAJO=AUX[AUX['ISC_Si/Irra_vista (A m2/W)']<Mediana*(1-porcent_mediana/100)]   
    Datos_filtrados=Datos_filtrados.drop(DEBAJO.index[:],axis=0)
    ENCIMA=AUX[AUX['ISC_Si/Irra_vista (A m2/W)']>Mediana*(1+porcent_mediana/100)]
    Datos_filtrados=Datos_filtrados.drop(ENCIMA.index[:],axis=0)
filt_df=Datos_filtrados
'''  Comparativa del filtrado'''

fig=plt.figure(figsize=(30,15))
plt.ylim(0,0.04)
plt.plot(filt_df_['aoi'],filt_df_['ISC_Si/Irra_vista (A m2/W)'], 'o',markersize='4',label='Sin filtrado')    
plt.plot(filt_df['aoi'],filt_df['ISC_Si/Irra_vista (A m2/W)'],'o', markersize='2',label='Con filtrado')    
plt.xlabel('Ángulo de incidencia (º)',fontsize=20)
plt.ylabel('ISC_Si/Irra_vista (A m2/W)',fontsize=20)
plt.legend()
plt.title("Datos de eficiencia de intensidad en función del ángulo de incidencia",fontsize=30)

fig=plt.figure(figsize=(30,15))
plt.ylim(0,0.04)
plt.plot(filt_df_['T_Amb (ºC)'],filt_df_['ISC_Si/Irra_vista (A m2/W)'], 'o',markersize='4',label='Sin filtrado')    
plt.plot(filt_df['T_Amb (ºC)'],filt_df['ISC_Si/Irra_vista (A m2/W)'],'o', markersize='2',label='Con filtrado')    
plt.xlabel('Temperatura ambiente (ºC)',fontsize=20)
plt.ylabel('ISC_Si/Irra_vista (A m2/W)',fontsize=20)
plt.legend()
plt.title("Datos de eficiencia de intensidad en función de la temperatura",fontsize=30)

fig=plt.figure(figsize=(30,15))
plt.ylim(0,0.04)
plt.xlim(1,3)
plt.plot(filt_df_['airmass_relative'],filt_df_['ISC_Si/Irra_vista (A m2/W)'], 'o',markersize='4',label='Sin filtrado')    
plt.plot(filt_df['airmass_relative'],filt_df['ISC_Si/Irra_vista (A m2/W)'],'o', markersize='2',label='Con filtrado')    
plt.xlabel('airmass (n.d.)',fontsize=20)
plt.ylabel('ISC_Si/Irra_vista (A m2/W)',fontsize=20)
plt.legend()
plt.title("Datos de eficiencia de intensidad en función del ángulo del airmass",fontsize=30)

fig=plt.figure(figsize=(30,15))
plt.plot(filt_df_['aoi'],filt_df_['PMP_estimated_Si (W)'], 'o',markersize='4',label='Sin filtrado')    
plt.plot(filt_df['aoi'],filt_df['PMP_estimated_Si (W)'],'o', markersize='2',label='Con filtrado')    
plt.xlabel('Ángulo de incidencia (º)',fontsize=20)
plt.ylabel('Potencia Si (W)',fontsize=20)
plt.legend()
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

x=filt_df['aoi']
y1=filt_df['ISC_Si/Irra_vista (A m2/W)']
x_aoi=filt_df['aoi']
x_temp=filt_df['T_Amb (ºC)']
x_AM=filt_df['airmass_relative']
#representacion del aoi con el scalar mapeable
fig, ax = plt.subplots(1,1,figsize=(30,20))
ax.scatter(x=x_aoi,y=y1,c=x_temp,cmap=Mappable_Temp.cmap, norm=Mappable_Temp.norm,s=10)
#plt.ylim(0,0.0012)
#plt.xlim(10,60)
ax.set_xlabel('Ángulo de incidencia (º)',fontsize=20)
ax.set_ylabel('ISC_Si/Irradiancia vista por el silicio (A m2/W)',fontsize=20)
ax.set_title("Eficiencia de instensidad del silicio en función del ángulo de incidencia y la temperatura",fontsize=30)
(fig.colorbar(Mappable_Temp)).set_label('Temperatura ambiente (ºC)')
plt.show()
#representacion del airmass con el scalar mapeable
fig, ax = plt.subplots(1,1,figsize=(30,20))
ax.scatter(x=x_AM,y=y1,c=x_temp, cmap=Mappable_Temp.cmap, norm=Mappable_Temp.norm,s=10)
#plt.ylim(0,0.0012)
#plt.xlim(1,2)
ax.set_xlabel('airmass (n.d)',fontsize=20)
ax.set_ylabel('ISC_Si/Irradiancia vista por el silicio (A m2/W)',fontsize=20)
ax.set_title("Eficiencia de instensidad del silicio en función de la masa de aire y la temperatura",fontsize=30)
(fig.colorbar(Mappable_Temp)).set_label('Temperatura ambiente (ºC) ',fontsize=20)
plt.show()
#representacion del airmass con el scalar mapeable
fig, ax = plt.subplots(1,1,figsize=(30,20))
ax.scatter(x=x_AM,y=y1,c=x_aoi, cmap=Mappable_aoi.cmap, norm=Mappable_aoi.norm,s=10)
#plt.ylim(0,0.0012)
#plt.xlim(1,2)
ax.set_xlabel('airmass(n.d.)',fontsize=20)
ax.set_ylabel('ISC_Si/Irradiancia vista por el silicio (A m2/W)',fontsize=20)
ax.set_title("Eficiencia de instensidad del silicio en función de la masa de aire y la temperatura",fontsize=30)
(fig.colorbar(Mappable_aoi)).set_label('Ángulo de incidencia (º)',fontsize=20)
plt.show()
#representamos de la temp con el scalar mapeable
fig, ax = plt.subplots(1,1,figsize=(30,20))
ax.scatter(x=x_temp,y=y1,c=x_aoi, cmap=Mappable_aoi.cmap, norm=Mappable_aoi.norm,s=10)
#plt.ylim(0,0.0012)
#plt.xlim(1,2)
ax.set_xlabel('Temperatura',fontsize=20)
ax.set_ylabel('ISC_Si/Irradiancia vista por el silicio (A m2/W)',fontsize=20)
ax.set_title("Eficiencia de instensidad del silicio en función de la temperatura y el ángulo de incidencia",fontsize=30)
(fig.colorbar(Mappable_aoi)).set_label('Ángulo de incidencia (º)',fontsize=20)
plt.show()
#representacion del aoi con el scalar mapeable
fig, ax = plt.subplots(1,1,figsize=(30,20))
ax.scatter(x=x_aoi,y=y1,c=x_temp,cmap=Mappable_Temp.cmap, norm=Mappable_Temp.norm,s=10)
#plt.ylim(0,0.0012)filt_df['ISC_Si/Irra_vista (A m2/W)'][i]
#plt.xlim(10,60)
ax.set_xlabel('Ángulo de incidencia (º)',fontsize=20)
ax.set_ylabel('ISC_Si/Irradiancia vista por la célula (A m2/W)',fontsize=20)
ax.set_title("Eficiencia de instensidad del silicio en función del ángulo de incidencia y la temperatura",fontsize=30)
(fig.colorbar(Mappable_Temp)).set_label('Temperatura ambiente (ºC)',fontsize=20)
plt.show()
filt_df.to_csv("C://Users/juanj/OneDrive/Escritorio/TFG/filt_df_Si.csv",encoding='utf-8')





