# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 15:56:55 2020

@author: juanjo
"""
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import host_subplot
AOI_LIMIT=55.0

df_Si=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/Datos_filtrados_Si.csv')
df_IIIV=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/Datos_filtrados_IIIV.csv')
#Se crea un dataframe con los datos de silicio y IIIV enun mismo data
#%%
df_juntos=pd.merge(df_IIIV, df_Si,how='outer')
df_juntos=df_juntos.set_index(pd.DatetimeIndex(df_juntos['Date Time']))
df_juntos=df_juntos.drop(['Date Time'],axis=1)
df_juntos=df_juntos.sort_values('Date Time')
df_juntos['ISC_IIIV/ISC_Si']=df_juntos['ISC_measured_IIIV (A)']/df_juntos['ISC_measured_Si (A)']
df_juntos['DII/GII']=df_juntos['DII (W/m2)']/df_juntos['GII (W/m2)']

fig=plt.figure(figsize=(30,15))
plt.plot(df_juntos.index.values,df_juntos['PMP_estimated_Si (W)'],'o',markersize=2, label='Potencia estimada Si')
plt.plot(df_juntos.index.values,df_juntos['PMP_estimated_IIIV (W)'],'o',markersize=2,label='Potencia estimada IIIV')
plt.xlabel('Ángulo de incidencia (º)', fontsize=30)
plt.ylabel('Potencia estimada (W)',fontsize=30)
plt.title("Comparativa de potencias estimadas del III-V con el Silicio en función del tiempo",fontsize=40)
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.legend(fontsize=30,markerscale=3)

fig=plt.figure(figsize=(30,15))
plt.plot(df_juntos.index.values,df_juntos['ISC_measured_Si (A)'],'o',markersize=2,label='Intensidad Silicio')
plt.plot(df_juntos.index.values,df_juntos['ISC_measured_IIIV (A)'],'o',markersize=2,label='Intensidad III-V')
plt.xlabel('Ángulo de incidencia (º)',fontsize=30)
plt.ylabel('Intensidad medida (A)',fontsize=30)
plt.title("Comparativa de intensidades del III-V con el Silicio en función del tiempo de todos los datos", fontsize=40)
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.legend(fontsize=30,markerscale=3)

fig=plt.figure(figsize=(30,15))
plt.plot(df_juntos['aoi'],df_juntos['PMP_estimated_Si (W)'],'o',markersize=2, label='Potencia Si')
plt.plot(df_juntos['aoi'],df_juntos['PMP_estimated_IIIV (W)'],'o',markersize=2,label='Potencia IIIV')
plt.xlabel('Ángulo de incidencia (º)',fontsize=30)
plt.ylabel('Potencia estimada (W)',fontsize=30)
plt.title("Comparativa de potencias del III-V con el Silicio en función del ángulo de incidencia",fontsize=40)
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.legend(fontsize=30,markerscale=3)

plt.figure(figsize=(30,15))
host = host_subplot(111)
par = host.twinx()
host.set_xlabel("Ángulo de incidencia (º)",fontsize=30)
host.set_ylabel("Eficiencia de captación del III-V (A m2/W)",fontsize=30)
par.set_ylabel("Eficiencia de captación del Silicio (A m2/W)",fontsize=30)
p1, = host.plot(df_juntos['aoi'],df_juntos['ISC_IIIV/DII (A m2/W)'],'o',markersize=2,color='b',label='IIIV')
p2, = par.plot(df_juntos['aoi'],df_juntos['ISC_Si/Irra_vista (A m2/W)'],'o',markersize=2,color='g',label='Si')
leg = plt.legend(fontsize=30,markerscale=3)
host.yaxis.get_label().set_color(p1.get_color())
leg.texts[0].set_color(p1.get_color())
par.yaxis.get_label().set_color(p2.get_color())
leg.texts[1].set_color(p2.get_color())
plt.title("Comparativa de eficiencia de captación de III-V con el Silicio en función del ángulo de incidencia", fontsize=40)
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
par.tick_params(labelsize=30)
plt.ylim(0,0.0015)
plt.show()






























