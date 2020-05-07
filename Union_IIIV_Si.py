# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import host_subplot

df_Si=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/Datos_filtrados_Si.csv')
df_IIIV=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/Datos_filtrados_IIIV.csv')
#Se crea un dataframe con los datos de silicio y IIIV enun mismo data

df_juntos=pd.merge(df_IIIV, df_Si,how='outer')
df_juntos=df_juntos.set_index(pd.DatetimeIndex(df_juntos['Date Time']))
df_juntos=df_juntos.drop(['Date Time'],axis=1)
df_juntos=df_juntos.sort_values('Date Time')
df_juntos['ISC_IIIV/ISC_Si']=df_juntos['ISC_measured_IIIV (A)']/df_juntos['ISC_measured_Si (A)']
df_juntos['DII/GII']=df_juntos['DII (W/m2)']/df_juntos['GII (W/m2)']



fig=plt.figure(figsize=(30,15))
plt.plot(df_juntos.index,df_juntos['PMP_estimated_Si (W)'],'o',markersize=2, label='Potencia estimada Si')
plt.plot(df_juntos.index,df_juntos['PMP_estimated_IIIV (W)'],'o',markersize=2,label='Potencia estimada IIIV')
plt.xlabel('Tiempo')
plt.ylabel('Potencia estimada (W)')
plt.title("Comparativa de potencias estimadas del III-V con el Silicio en función del ángulo de incidencia")
plt.legend()


fig=plt.figure(figsize=(30,15))
plt.plot(df_juntos.index,df_juntos['ISC_measured_Si (A)'],'o',markersize=2,label='Intensidad Silicio')
plt.plot(df_juntos.index,df_juntos['ISC_measured_IIIV (A)'],'o',markersize=2,label='Intensidad III-V')
plt.xlabel('Tiempo')
plt.ylabel('Intensidad medida (A)')
plt.title("Comparativa de intensidades del III-V con el Silicio en función del tiempo de todos los datos")
plt.legend()


fig=plt.figure(figsize=(30,15))
plt.xlim(0.6,1)
plt.plot(df_juntos['DII/GII'],df_juntos['ISC_IIIV/ISC_Si'],'o',markersize=2)
plt.xlabel('Proporción de Irradiancia directa incidente sobre la Irradiancia general incidente')
plt.ylabel('Proporción de Intensidad de concentración sobre intensidad del silicio')
plt.title("Representación de proporción de intensidades en función de la proporción de irradiancias")


fig=plt.figure(figsize=(30,15))
plt.plot(df_juntos['aoi'],df_juntos['ISC_IIIV/DII (A m2/W)'],'o',markersize=2,label='Intensidad efectiva del III-V')
plt.plot(df_juntos['aoi'],df_juntos['ISC_Si/GII (A m2/W)'],'o',markersize=2,label='Intensidad efectiva del silicio')
plt.plot(df_juntos['aoi'],df_juntos['ISC_Si/Irra_vista (A m2/W)'],'o',markersize=2,label='Intensidad efectiva del silicio')
plt.xlabel('Ángulo de incidencia (°)')
plt.ylabel('Eficiencia de la captación de irradiancia (A m2/W)')
plt.title("Comparativa de intensidades efectivas del III-V con el Silicio en función del ángulo de incidencia")
plt.legend()


fig=plt.figure(figsize=(30,15))
plt.plot(df_juntos['aoi'],df_juntos['ISC_IIIV/DII (A m2/W)'],'o',markersize=2,label='Intensidad efectiva del III-V')
plt.plot(df_juntos['aoi'],df_juntos['ISC_Si/Irra_vista (A m2/W)'],'o',markersize=2,label='Intensidad efectiva del silicio')
plt.xlabel('Ángulo de incidencia (°)')
plt.ylabel('Eficiencia de la captación de irradiancia (A m2/W)')
plt.title("Comparativa de intensidades efectivas del III-V con el Silicio en función del ángulo de incidencia")
plt.legend()



fig,ax1=plt.subplots(figsize=(20,20))
ax1.set_xlabel('Ángulo de incidencia (°)')
ax1.set_ylabel('Eficiencia de la captación de irradiancia del IIIV(A m2/W)')
ax1.plot(df_juntos['aoi'],df_juntos['ISC_IIIV/DII (A m2/W)'],'o',markersize=2,color='b',label='IIIV')
ax2 = ax1.twinx() 
ax2.set_ylabel('Eficiencia de la captación de irradiancia del Silicio(A m2/W)')  # we already handled the x-label with ax1
ax2.plot(df_juntos['aoi'],df_juntos['ISC_Si/Irra_vista (A m2/W)'],'o',markersize=2,color='g',label='Si')
fig.tight_layout()  # otherwise the right y-label is slightly clipped
ax1.legend()
ax2.legend()
plt.show()

plt.figure(figsize=(30,20))
host = host_subplot(111)
par = host.twinx()
host.set_xlabel("Ángulo de incidencia (°)")
host.set_ylabel("Eficiencia de la captación de irradiancia del IIIV(A m2/W)")
par.set_ylabel("Eficiencia de la captación de irradiancia del Silicio(A m2/W)")
p1, = host.plot(df_juntos['aoi'],df_juntos['ISC_IIIV/DII (A m2/W)'],'o',markersize=2,color='b',label='IIIV')
p2, = par.plot(df_juntos['aoi'],df_juntos['ISC_Si/Irra_vista (A m2/W)'],'o',markersize=2,color='g',label='Si')
leg = plt.legend()
host.yaxis.get_label().set_color(p1.get_color())
leg.texts[0].set_color(p1.get_color())
par.yaxis.get_label().set_color(p2.get_color())
leg.texts[1].set_color(p2.get_color())
plt.show()































#------------------para ver los rultados del filtrado juntos, por dias
#date=np.array(['2019-05-30'])
#for i in range(0,len(df_juntos.index)):
#    if(i==0):
#        date[0]=str(df_juntos.index[0].date())
#    elif(df_juntos.index[i-1].date()!=df_juntos.index[i].date()):
#        date=np.append(date,str(df_juntos.index[i].date()))
#        
#for i in date:
#    fig=plt.figure(figsize=(30,15))
#    plt.plot(df_juntos[i].index[:].time,df_juntos[i]['PMP_estimated_Si (W)'],'o',markersize=2)
#    plt.plot(df_juntos[i].index[:].time,df_juntos[i]['PMP_estimated_IIIV (W)'],'o',markersize=2)
#    plt.xlabel('Horas')
#    plt.ylabel('PMP_estimated (W)')
#    plt.legend()
#    plt.title("Datos de potencias "+ str(i))
#    
#for i in date:
#    fig=plt.figure(figsize=(30,15))
#    plt.plot(df_juntos[i].index[:].time,df_juntos[i]['ISC_measured_Si (A)'],'o',markersize=2,label='Intensidad Silicio')
#    plt.plot(df_juntos[i].index[:].time,df_juntos[i]['ISC_measured_IIIV (A)'],'o',markersize=2,label='Intensidad III-V')
#    plt.xlabel('Horas')
#    plt.ylabel('ISC_measured (A)')
#    plt.legend()
#    plt.title("Datos de intensidades "+ str(i))
#







