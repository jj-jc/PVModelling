# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 11:53:09 2020

@author: juanj
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import Error 
import pvlib
import plotly.graph_objects as go

from mpl_toolkits.axes_grid1 import host_subplot
#Codigo para poder expresar las gráfcas en plotly
import plotly.io as pio
pio.renderers.default='browser'


#AOILIMIT
AOILIMIT=55.0
# Valor_normalizar=0.00091802#Este valor es el valor que Marcos utiliza para normalizar 
# VALOR_NORMALIZAR=0.00096
VALOR_NORMALIZAR=0.006
df=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/Datos_filtrados_Si.csv',encoding='utf-8')



filt_df2=df

filt_df2=df[(df['aoi']>AOILIMIT)]
filt_x=filt_df2['aoi'].values
filt_y=filt_df2['ISC_Si/Irra_vista (A m2/W)'].values
filt_df3=filt_df2
plt.figure(figsize=(30,15))
plt.plot(filt_x,filt_y,'o',markersize=2,label='Previsión actual')

# plt.plot(CPV['aoi'],Potencias_estimadas['Potencias_estimadas (W)'],'o',markersize=2,label='Con UF')
plt.xlabel('Ángulo de incidencia (°)')
plt.ylabel('Eficiencia de intensidad (A m2/W)')
plt.title('Eficiencia de intensidad en función del ángulo de incidencia')
plt.legend()


plt.figure(figsize=(30,15))
plt.plot(filt_df2['airmass_relative'],filt_y,'o',markersize=2,label='Previsión actual')
# plt.plot(CPV['aoi'],Potencias_estimadas['Potencias_estimadas (W)'],'o',markersize=2,label='Con UF')
plt.xlabel('airmass (n.d.)')
plt.ylabel('Eficiencia de intensidad (A m2/W)')
plt.title('Eficiencia de intensidad en función del airmass')
plt.legend()



plt.figure(figsize=(30,15))
plt.plot(filt_df2['T_Amb (°C)'],filt_y,'o',markersize=2,label='Previsión actual')
# plt.plot(CPV['aoi'],Potencias_estimadas['Potencias_estimadas (W)'],'o',markersize=2,label='Con UF')
plt.xlabel('Ángulo de incidencia (°)')
plt.ylabel('Eficiencia de intensidad (A m2/W)')
plt.title('Eficiencia de intensidad en función de la temperatura')
plt.legend()

# iam=pvlib.iam.ashrae(filt_x, b=0.05)

# plt.figure(figsize=(30,15))
# plt.plot(filt_x,iam,'o',markersize=2,label='Previsión actual')
# # plt.plot(CPV['aoi'],Potencias_estimadas['Potencias_estimadas (W)'],'o',markersize=2,label='Con UF')
# plt.xlabel('Ángulo de incidencia (°)')
# plt.ylabel('Potencia (III-V)(W)')
# # plt.title('Comparación de los resultados con los datos estimados de potencias en funcion del UF')
# plt.legend()

#%%

#Se estudian las influencias de demás variables en la de estudio.


# Incremento=.1
# Max_temp=math.ceil(filt_df2['Wind Speed (m/s)'].max())
# Min_temp=math.floor(filt_df2['Wind Speed (m/s)'].min())
# fig=go.Figure()
# contador=np.arange(Min_temp,Max_temp,Incremento)
# for i in contador:
#     AUX=filt_df2[(filt_df2['Wind Speed (m/s)']>=float(i))]
#     AUX=AUX[((AUX['Wind Speed (m/s)'])<i+Incremento)]    

#     fig.add_trace(go.Scatter(
#     y=AUX['ISC_Si/Irra_vista (A m2/W)'],
#     x=AUX['aoi'],
#     mode='markers',
#     visible=True,
#     showlegend=True,
#     name='Temperatura '+ str(i)
#     ))
# fig.update_layout(
#     title="Isc_IIIV/DII en función del ángulo de incidencia, divido por intervalos de velocidad de viento",
#     xaxis_title="Ángulo de incidencia (°)",
#     yaxis_title="ISC_IIIV/DII (A m2/W)",
# )

# fig.show()



# Incremento=10
# Max_temp=math.ceil(filt_df2['Wind Dir. (m/s)'].max())
# Min_temp=math.floor(filt_df2['Wind Dir. (m/s)'].min())
# fig=go.Figure()
# contador=np.arange(Min_temp,Max_temp,Incremento)
# for i in contador:
#     AUX=filt_df2[(filt_df2['Wind Dir. (m/s)']>=float(i))]
#     AUX=AUX[((AUX['Wind Dir. (m/s)'])<i+Incremento)]    

#     fig.add_trace(go.Scatter(
#     y=AUX['ISC_Si/Irra_vista (A m2/W)'],
#     x=AUX['aoi'],
#     mode='markers',
#     visible=True,
#     showlegend=True,
#     name='Temperatura '+ str(i)
#     ))
# fig.update_layout(
#     title="Isc_IIIV/DII en función del ángulo de incidencia, divido por intervalos de velocidad de viento",
#     xaxis_title="Ángulo de incidencia (°)",
#     yaxis_title="ISC_IIIV/DII (A m2/W)",
# )

# fig.show()

# Incremento=1
# Max_temp=math.ceil(filt_df2['T_Amb (°C)'].max())
# Min_temp=math.floor(filt_df2['T_Amb (°C)'].min())
# fig=go.Figure()
# contador=np.arange(Min_temp,Max_temp,Incremento)
# for i in contador:
#     AUX=filt_df2[(filt_df2['T_Amb (°C)']>=float(i))]
#     AUX=AUX[((AUX['T_Amb (°C)'])<i+Incremento)]    

#     fig.add_trace(go.Scatter(
#     y=AUX['ISC_Si/Irra_vista (A m2/W)'],
#     x=AUX['aoi'],
#     mode='markers',
#     visible=True,
#     showlegend=True,
#     name='Temperatura '+ str(i)
#     ))
# fig.update_layout(
#     title="Isc_IIIV/DII en función del ángulo de incidencia, divido por intervalos de velocidad de viento",
#     xaxis_title="Ángulo de incidencia (°)",
#     yaxis_title="ISC_IIIV/DII (A m2/W)",
# )

# fig.show()

#%% Como se puede observar con el código anterior, existe una linea de tendencia muy clara dependiente de la temperatura
#En este caso se ha escogido una temperatura de 30 a 31 grados centígrados
filt_df2=df[(df['aoi']>AOILIMIT)]





filt_df2=filt_df2[filt_df2['T_Amb (°C)']>=30.0]
filt_df2=filt_df2[filt_df2['T_Amb (°C)']<32]

filt_x=filt_df2['aoi'].values
filt_y=filt_df2['ISC_Si/Irra_vista (A m2/W)'].values


plt.figure(figsize=(30,15))
plt.plot(filt_df3['aoi'].values,filt_df3['ISC_Si/Irra_vista (A m2/W)'].values,'o',markersize=2,label='Previsión actual')

plt.plot(filt_x,filt_y,'o',markersize=2,label='Previsión actual')
# plt.plot(CPV['aoi'],Potencias_estimadas['Potencias_estimadas (W)'],'o',markersize=2,label='Con UF')
plt.xlabel('Ángulo de incidencia (°)')
plt.ylabel('Potencia (III-V)(W)')
# plt.title('Comparación de los resultados con los datos estimados de potencias en funcion del UF')
plt.legend()


# plt.figure(figsize=(30,15))
# plt.plot(filt_df2['airmass_relative'],filt_y,'o',markersize=2,label='Previsión actual')
# # plt.plot(CPV['aoi'],Potencias_estimadas['Potencias_estimadas (W)'],'o',markersize=2,label='Con UF')
# plt.xlabel('Ángulo de incidencia (°)')
# plt.ylabel('Potencia (III-V)(W)')
# plt.legend()



plt.figure(figsize=(30,15))
plt.plot(filt_df2['T_Amb (°C)'],filt_y,'o',markersize=2,label='Previsión actual')
# plt.plot(CPV['aoi'],Potencias_estimadas['Potencias_estimadas (W)'],'o',markersize=2,label='Con UF')
plt.xlabel('Ángulo de incidencia (°)')
plt.ylabel('Potencia (III-V)(W)')
# plt.title('Comparación de los resultados con los datos estimados de potencias en funcion del UF')
plt.legend()


#REGRESION DE PRIMER GRADO
#ESTE PROGRAMA ES PARA AVERIGUAR CUAL ES EL MEJOR THLDS  PARA EL AOI 
aux=np.arange(filt_df2['aoi'].min(),filt_df2['aoi'].max(),1) 
thdl=30
RR_max=0.01
for i in aux:
    filt_df_low=filt_df2[filt_df2['aoi']<=i]
    filt_df_high=filt_df2[filt_df2['aoi']>i]

    x_low=filt_df_low['aoi'].values
    y_low=filt_df_low['ISC_Si/Irra_vista (A m2/W)'].values
    yr_low, RR_low, a_s_low, b_low=Error.regresion_polinomica(x_low, y_low, 1)
    
    x_high=filt_df_high['aoi'].values
    y_high=filt_df_high['ISC_Si/Irra_vista (A m2/W)'].values
    yr_high, RR_high, a_s_high, b_high=Error.regresion_polinomica(x_high, y_high, 1)
    

    # y_datos=filt_df['ISC_IIIV/DII (A m2/W)'].values
    y=np.concatenate((y_low,y_high))
    yr=np.concatenate((yr_low,yr_high))
    xr=np.concatenate((x_low,x_high))
    RR=Error.Determination_coefficient(y,yr)   
    if RR_max < RR:
        RR_max=RR
        thld=i



filt_df_low=filt_df2[filt_df2['aoi']<=thld]
filt_df_high=filt_df2[filt_df2['aoi']>thld]

x_low=filt_df_low['aoi'].values
y_low=filt_df_low['ISC_Si/Irra_vista (A m2/W)'].values
yr_low, RR_low, a_s_low, b_low=Error.regresion_polinomica(x_low, y_low, 1)

x_high=filt_df_high['aoi'].values
y_high=filt_df_high['ISC_Si/Irra_vista (A m2/W)'].values
yr_high, RR_high, a_s_high, b_high=Error.regresion_polinomica(x_high, y_high, 1)

a_s1=np.concatenate((a_s_low,a_s_high))
b1=[b_low,b_high]
y_total=np.concatenate((y_low,y_high))
x_total=np.concatenate((x_low,x_high))
yr_total=np.concatenate((yr_low,yr_high))
RR_poli1=Error.Determination_coefficient(y_total, yr_total)

#----poli2
y_poli2,RR_poli2,a_s2,b2=Error.regresion_polinomica(filt_df2['aoi'].values,filt_df2['ISC_Si/Irra_vista (A m2/W)'].values,2)
#-----poli3
y_poli3,RR_poli3,a_s3,b3=Error.regresion_polinomica(filt_df2['aoi'].values,filt_df2['ISC_Si/Irra_vista (A m2/W)'].values,3)


fig=plt.figure(figsize=(30,15))
plt.plot(filt_df2['aoi'].values,filt_df2['ISC_Si/Irra_vista (A m2/W)'].values,'o',markersize=4,label='Datos')
plt.plot(x_total,yr_total,'o',markersize=4,label='Datos')
plt.plot(filt_df2['aoi'].values,y_poli2,'o',markersize=4,label='Datos')
plt.plot(filt_df2['aoi'].values,y_poli3,'o',markersize=4,label='Datos')

plt.xlabel('Ángulo de incidencia (°)')
plt.ylabel('ISC_IIIV/DII (A m2/W)')
plt.title('Regresión polinómica para 26 °C' )
plt.legend() 
print('El coeficiente de determinación para la regresión de primer grado es: '+str(RR_poli1))
print('El coeficiente de determinación para la regresión de segundo grado es: '+str(RR_poli2))
print('El coeficiente de determinación para la regresión de tercer grado es: '+str(RR_poli3))


iam1_low=[a_s_low[1]/VALOR_NORMALIZAR,0,0,b_low/VALOR_NORMALIZAR,thld,RR_low]
iam1_high=[a_s_high[1]/VALOR_NORMALIZAR,0,0,b_high/VALOR_NORMALIZAR,0,RR_low]

iam2=[a_s2[1]/VALOR_NORMALIZAR,a_s2[2]/VALOR_NORMALIZAR,0,b2/VALOR_NORMALIZAR,0,RR_poli2]

iam3=[a_s3[1]/VALOR_NORMALIZAR,a_s3[2]/VALOR_NORMALIZAR,a_s3[3]/VALOR_NORMALIZAR,b3/VALOR_NORMALIZAR,0,RR_poli3]
IAM=pd.DataFrame(columns={'Primer grado low','Primer grado high','Segundo grado','Tercer grado','ashrae','physical','martin_ruiz'},index=['a1','a2','a3','b','thld','RR'])


IAM['Primer grado low']=iam1_low
IAM['Primer grado high']=iam1_high
IAM['Segundo grado']=iam2
IAM['Tercer grado']=iam3


IAM.to_csv("C://Users/juanj/OneDrive/Escritorio/TFG/IAM_Si.csv")


#%%Se procede al cálculo de las irradiancias efectiva para obtener los UF

# filt_df3=filt_df2
# filt_df3['Irra_vista_efectiva (W/m2)']=filt_df3['Irra_vista (W/m2)']*Error.calc_iam_Si(filt_df3['aoi'].values,'Tercer grado')
# filt_df3['ISC_Si/Irra_vista_efectiva (A m2/W)']=filt_df3['ISC_measured_Si (A)']/filt_df3['Irra_vista_efectiva (W/m2)']
# filt_x=filt_df3['T_Amb (°C)'].values
# filt_y=filt_df3['ISC_Si/Irra_vista_efectiva (A m2/W)'].values

# fig=plt.figure(figsize=(30,15))
# # plt.plot(filt_df3['aoi'],filt_df3['ISC_Si/Irra_vista (A m2/W)'],'o',markersize=4,label='Datos por debajo de thdl')
# plt.plot(filt_df3['aoi'],filt_df3['ISC_Si/Irra_vista (A m2/W)'],'o',markersize=4,label='Datos por debajo de thdl')
# plt.plot(filt_df3['aoi'],filt_y,'o',markersize=4,label='Irra_vista')
# plt.ylabel('Ángulo de incidencia (°)')
# plt.ylabel('ISC_IIIV/DII (A m2/W)')
# plt.title('Eficiencia de la parte de III-V una vez corregida la irradiancia con el IAM')
# plt.legend()



