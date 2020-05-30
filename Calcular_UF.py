# -*- coding: utf-8 -*-



import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import Error as E
from cpvtopvlib import uf_preprocessing
import plotly.graph_objects as go
import plotly.io as pio
import math
pio.renderers.default='browser'
AOILIMIT=55.0
# VALOR_NORMALIZAR=0.0009180248205304829
VALOR_NORMALIZAR=0.001
df=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/Datos_filtrados_IIIV.csv')
df_iam=pd.read_csv("C://Users/juanj/OneDrive/Escritorio/TFG/IAM.csv")
df_iam=df_iam.set_index(df_iam['Unnamed: 0'].values)
df_iam=df_iam.drop('Unnamed: 0',axis=1)



filt_df=df[df['aoi']<=AOILIMIT]
filt_df['DII_efectiva (W/m2)']=filt_df['DII (W/m2)']*E.obtencion_dii_efectiva(filt_df['aoi'].values)
filt_df['ISC_IIIV/DII_efectiva (A m2/W)']=filt_df['ISC_measured_IIIV (A)']/filt_df['DII_efectiva (W/m2)']
filt_x=filt_df['T_Amb (°C)'].values
filt_y=filt_df['ISC_IIIV/DII_efectiva (A m2/W)'].values

fig=plt.figure(figsize=(30,15))
plt.plot(filt_df['aoi'],filt_df['ISC_IIIV/DII (A m2/W)'],'o',markersize=4,label='Datos por debajo de thdl')
plt.plot(filt_df['aoi'],filt_y,'o',markersize=4,label='Datos por debajo de thdl')
plt.ylabel('Ángulo de incidencia (°)')
plt.ylabel('ISC_IIIV/DII (A m2/W)')
plt.title('Ificiencia de la parte de III-V una vez corregida la irradiancia con el IAM')
plt.legend()





UF=pd.DataFrame(columns=['temp','UF_temp','UF_am','UF_am_2'])



#%%AHORA SE ESTUDIAN LAS TENDENCIAS PAR EVITAR LA INFLUENCIA DEL AIRMASS


# Incremento=1
# Max_temp=math.ceil(filt_df['airmass_absolute'].max())*10
# Min_temp=math.floor(filt_df['airmass_absolute'].min())*10
# fig=go.Figure()
# for i in range(Min_temp,Max_temp,Incremento):
#     AUX=filt_df[(filt_df['airmass_absolute']>=float(i/10))]
#     AUX=AUX[((AUX['airmass_absolute'])<(i+Incremento)/10)]    

#     fig.add_trace(go.Scatter(
#     y=AUX['ISC_IIIV/DII_efectiva (A m2/W)'],
#     x=AUX['T_Amb (°C)'],
#     mode='markers',
#     visible=True,
#     showlegend=True,
#     name='airmass '+ str(i/10)
#     ))
# fig.update_layout(
#     title="Isc_IIIV/DII en función del ángulo de incidencia, divido por intervalos de temperatura",
#     xaxis_title="Ángulo de incidencia (°)",
#     yaxis_title="ISC_IIIV/DII (A m2/W)",
# )


# fig.show()

#%%Cálculo del UF_temp

filt_df_temp=filt_df
# filt_df_temp=filt_df_temp[filt_df_temp['Wind Dir. (m/s)']>=133.0]
# filt_df_temp=filt_df_temp[filt_df_temp['Wind Dir. (m/s)']<143]
# filt_df_temp=filt_df_temp[filt_df_temp['Wind Speed (m/s)']>=1.4]
# filt_df_temp=filt_df_temp[filt_df_temp['Wind Speed (m/s)']<2.5]

temp_cell=pvlib.temperature.pvsyst_cell(poa_global=filt_df_temp['DII_efectiva (W/m2)'], 
                                        temp_air=filt_df_temp['T_Amb (°C)'],
                                        wind_speed=filt_df_temp['Wind Speed (m/s)'], 
                                        u_c=29.0, u_v=0.0, 
                                        eta_m=0.1, alpha_absorption=0.9)
fig=plt.figure(figsize=(30,15))
plt.plot(temp_cell,filt_df_temp['ISC_IIIV/DII_efectiva (A m2/W)'].values,'o',markersize=4,label='Datos por debajo de AOILIMIT')
plt.plot(filt_df_temp['T_Amb (°C)'].values,filt_df_temp['ISC_IIIV/DII_efectiva (A m2/W)'].values,'o',markersize=4,label='Datos por debajo de AOILIMIT')
# plt.ylim(0,0.002)
plt.xlabel('Temperatura ambiente (°C) ')
plt.ylabel('ISC_IIIV/DII (A m2/W)')
plt.title('Cálculo del UF para la temperatura')
plt.legend()
# print('El coeficiente de determinación para los datos por debajo de AOILIMIT es de: '+str(RR1))


Incremento=0.1
Max_temp=math.ceil(filt_df_temp['airmass_absolute'].max())
Min_temp=math.floor(filt_df_temp['airmass_absolute'].min())
contador=np.arange(Min_temp,Max_temp,Incremento)
fig=go.Figure()
for i in contador:
    AUX=filt_df_temp[(filt_df_temp['airmass_absolute']>=float(i))]
    AUX=AUX[((AUX['airmass_absolute'])<i+Incremento)]    

    fig.add_trace(go.Scatter(
    y=AUX['ISC_IIIV/DII_efectiva (A m2/W)'],
    x=AUX['T_Amb (°C)'],
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

#se aprecia claramente la influencia del airmass, para poder modelar la temperatura es necesario escoger un intervalo fijo
#de am para poder estudiar la influencia de la temperatura.
#%%
#He decidido observar llo que pasa con las condiciones estandart

filt_df_temp=filt_df


# filt_df_temp=filt_df_temp[(filt_df_temp['airmass_absolute']<1.1)]
# # filt_df_temp=filt_df_temp[(filt_df_temp['airmass_absolute']>1.0)]
# filt_x=filt_df_temp['T_Amb (°C)'].values
# filt_y=filt_df_temp['ISC_IIIV/DII_efectiva (A m2/W)'].values





y1_regre,RR1,a_s1,b1=E.regresion_polinomica(filt_x,filt_y,1)
fig=plt.figure(figsize=(30,15))
plt.plot(filt_x,filt_y,'o',markersize=4,label='Datos por debajo de AOILIMIT')
plt.plot(filt_x,y1_regre,'o',markersize=4,label='Línea de regresión')
# plt.ylim(0,0.002)
plt.xlabel('Temperatura ambiente (°C) ')
plt.ylabel('ISC_IIIV/DII (A m2/W)')
plt.title('Cálculo del UF para la temperatura')
plt.legend()
print('El coeficiente de determinación para los datos por debajo de AOILIMIT es de: '+str(RR1))



thld=filt_x[np.where(y1_regre==y1_regre.max())]
simple_uf= 1 + (filt_x - thld) * (a_s1[1])/VALOR_NORMALIZAR
fig=plt.figure(figsize=(30,15))
plt.plot(filt_x,simple_uf,'o',markersize=4,label='Datos primera parte')
UF_temp=simple_uf


#dando como resultado tras el normalizado
#  1+(Temp-thld)*(m/Normalizar)
# thld=14.67
# m=-3.35258382e-06
# valor_normalizar=0.00096

#%%Cálculo del UF_am 

filt_df_am=filt_df


# filt_df_am=filt_df_am[filt_df_am['Wind Dir. (m/s)']>=133.0]
# filt_df_am=filt_df_am[filt_df_am['Wind Dir. (m/s)']<143]
# filt_df_am=filt_df_am[filt_df_am['Wind Speed (m/s)']>=1.4]
# filt_df_am=filt_df_am[filt_df_am['Wind Speed (m/s)']<2.5]





# Incremento=1
# Max_temp=math.ceil(filt_df_am['T_Amb (°C)'].max())
# Min_temp=math.floor(filt_df_am['T_Amb (°C)'].min())
# contador=np.arange(Min_temp,Max_temp,Incremento)
# fig=go.Figure()
# for i in contador:
#     AUX=filt_df_am[(filt_df_am['T_Amb (°C)']>=float(i))]
#     AUX=AUX[((AUX['T_Amb (°C)'])<i+Incremento)]    

#     fig.add_trace(go.Scatter(
#     y=AUX['ISC_IIIV/DII (A m2/W)'],
#     x=AUX['airmass_absolute'],
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



# filt_df_am=filt_df_am[filt_df_am['T_Amb (°C)']>=26.0]
# filt_df_am=filt_df_am[filt_df_am['T_Amb (°C)']<28.0]

filt_x=filt_df_am['airmass_absolute'].values
filt_y=filt_df_am['ISC_IIIV/DII_efectiva (A m2/W)'].values

fig=plt.figure(figsize=(30,15))
plt.plot(filt_x,filt_y,'o',markersize=4,label='Datos ISC_IIIV/DII_efectiva')
plt.ylabel('ISC_IIIV/DII (A m2/W)')
plt.title('Cáculo del UF para airmass')
plt.legend()





#%%CÓDIGO PARA OBSERVAR LAS TENDENDICAS CON DIFERENTES TEMPERATURAS

Incremento=1
Max_temp=math.ceil(filt_df_am['T_Amb (°C)'].max())
Min_temp=math.floor(filt_df_am['T_Amb (°C)'].min())
fig=go.Figure()
for i in range(Min_temp,Max_temp,Incremento):
    AUX=filt_df_am[(filt_df_am['T_Amb (°C)']>=float(i))]
    AUX=AUX[((AUX['T_Amb (°C)'])<i+Incremento)]    

    fig.add_trace(go.Scatter(
    y=AUX['ISC_IIIV/DII_efectiva (A m2/W)'],
    x=AUX['airmass_absolute'],
    mode='markers',
    visible=True,
    showlegend=True,
    name='Temperatura '+ str(i)
    ))
fig.update_layout(
    title="Isc_IIIV/DII en función del ángulo de incidencia, divido por intervalos de temperatura",
    xaxis_title="Ángulo de incidencia (°)",
    yaxis_title="ISC_IIIV/DII (A m2/W)",
)


fig.show()

Incremento=0.1
Max_temp=math.ceil(filt_df_am['Wind Speed (m/s)'].max())
Min_temp=math.floor(filt_df_am['Wind Speed (m/s)'].min())
aux_vector=np.arange(Min_temp,Max_temp,Incremento)
fig=go.Figure()
for i in aux_vector:
    AUX=filt_df_am[(filt_df_am['Wind Speed (m/s)']>=float(i))]
    AUX=AUX[((AUX['Wind Speed (m/s)'])<i+Incremento)]    

    fig.add_trace(go.Scatter(
    y=AUX['ISC_IIIV/DII_efectiva (A m2/W)'],
    x=AUX['airmass_absolute'],
    mode='markers',
    visible=True,
    showlegend=True,
    name='Temperatura '+ str(i)
    ))
fig.update_layout(
    title="Isc_IIIV/DII en función del ángulo de incidencia, divido por intervalos de temperatura",
    xaxis_title="Ángulo de incidencia (°)",
    yaxis_title="ISC_IIIV/DII (A m2/W)",
)


fig.show()
#al observar el scatter, se observan como dos líneas de tendencias, pero no parecen que se la tempera amb 
# la causa de tales tendencias. Puede ser perfectamente la temperatura de trabajo de la célula, que debido 
# al viento en unas disipa mejor el calor que en las otras. Aunque es cierto que se filtraron los datos
# para velocidades menores que 2.5

fig=plt.figure(figsize=(30,15))
plt.plot(filt_df['Wind Speed (m/s)'],filt_df['ISC_IIIV/DII_efectiva (A m2/W)'],'o',markersize=4,label='Datos ISC_IIIV/DII_efectiva')
plt.ylabel('ISC_IIIV/DII (A m2/W)')
plt.title('Cáculo del UF para airmass')
plt.legend()

fig=plt.figure(figsize=(30,15))
plt.plot(filt_df['Wind Dir. (m/s)'],filt_df['ISC_IIIV/DII_efectiva (A m2/W)'],'o',markersize=4,label='Datos ISC_IIIV/DII_efectiva')
plt.ylabel('ISC_IIIV/DII (A m2/W)')
plt.title('Cáculo del UF para airmass')
plt.legend()

# Si dibujamos la ISC_IIIV/DII_efectiva (A m2/W) en función de la dirección del viento, observamos
# que existe una mayor densidad de datos, lo que puede indicar mejora de rendimiento en esa situación


#%%
filt_df_am=filt_df_am[filt_df_am['Wind Speed (m/s)']>=0.9]
filt_df_am=filt_df_am[filt_df_am['Wind Speed (m/s)']<1.1]



#%%

#ESTE PROGRAMA ES PARA AVERIGUAR CUAL ES EL MEJOR THLDS
# Se obtiene un RR=0.8540025403043598 y un thld=1.2467475563652137

aux=np.arange(filt_df_am['airmass_absolute'].min(),filt_df_am['airmass_absolute'].max(),0.001) 
thld=30
RR_max=0.01
for i in aux:
    filt_df_low=filt_df_am[filt_df_am['airmass_absolute']<=i]
    filt_df_high=filt_df_am[filt_df_am['airmass_absolute']>i]

    x_low=filt_df_low['airmass_absolute'].values
    y_low=filt_df_low['ISC_IIIV/DII_efectiva (A m2/W)'].values
    yr_low, RR_low, a_s_low, b_low=E.regresion_polinomica(x_low, y_low, 1)
    
    x_high=filt_df_high['airmass_absolute'].values
    y_high=filt_df_high['ISC_IIIV/DII_efectiva (A m2/W)'].values
    yr_high, RR_high, a_s_high, b_high=E.regresion_polinomica(x_high, y_high, 1)
    

    y_datos=filt_df_am['ISC_IIIV/DII_efectiva (A m2/W)'].values
    y=np.concatenate((y_low,y_high))
    yr=np.concatenate((yr_low,yr_high))
    xr=np.concatenate((x_low,x_high))
    RR=E.Determination_coefficient(y,yr)   
    if RR_max < RR:
        RR_max=RR
        thld=i
        
        
        
        
        
#%%
filt_df_low=filt_df_am[filt_df_am['airmass_absolute']<=thld]
filt_df_high=filt_df_am[filt_df_am['airmass_absolute']>thld]

x_low=filt_df_low['airmass_absolute'].values
y_low=filt_df_low['ISC_IIIV/DII_efectiva (A m2/W)'].values
yr_low, RR_low, a_s_low, b_low=E.regresion_polinomica(x_low, y_low, 1)

x_high=filt_df_high['airmass_absolute'].values
y_high=filt_df_high['ISC_IIIV/DII_efectiva (A m2/W)'].values
yr_high, RR_high, a_s_high, b_high=E.regresion_polinomica(x_high, y_high, 1)


y_total=np.concatenate((y_low,y_high))
yr_total=np.concatenate((yr_low,yr_high))
RR=E.Determination_coefficient(y_total, yr_total)
#asi vemos de un color los datos y de otro las regresiones
# fig=plt.figure(figsize=(30,15))
# plt.plot(x,y_datos,'o',markersize=4,label='Datos primera parte')
# plt.plot(xr,yr,'o',markersize=4,label='Datos primera parte')
# plt.title('Regresión polinómica')
# plt.legend()

#asi vemos de cada color cada regresion
fig=plt.figure(figsize=(30,15))
plt.plot(x_low,y_low,'o',markersize=4,label='Datos por debajo de thdl')
plt.plot(x_low,yr_low,'o',markersize=4,label='Regresión por debajo de thdl')
plt.plot(x_high,y_high,'o',markersize=4,label='Datos por encima de thdl')
plt.plot(x_high,yr_high,'o',markersize=4,label='Regresion por encima de thdl')
plt.xlabel('Airmass (n.d.)')
plt.ylabel('ISC_IIIV/DII (A m2/W)')
plt.title('Cáculo del UF para airmass')
plt.legend()
print('El coeficiente de determinación por debajo de thdl : ', str(RR_low))
print('El coeficiente de determinación por encima de thdl : ', str(RR_high))
print('El coeficiente de determinación total : ', str(RR))

#HAY QUE BUSCAR UN VALOR PARA NORMALIZAR LOS RESULTADOS, ESOCOJO LA INTERSECCION CON EL EJE DE ORDENADAS
# Valor_normalizar=0.00096
# thld=1.2485999999999837

thld_low=filt_x.min()

y_low_min=float(1 + (x_low[np.where(yr_low==yr_low.min())] - thld_low) * (a_s_low[1])/VALOR_NORMALIZAR)


simple_uf=[]
for i in filt_df_am['airmass_absolute'].values:
    if i < thld:
        simple_uf.append(float(1 + (i - thld_low) * (a_s_low[1])/VALOR_NORMALIZAR))


    else:
        simple_uf.append(float(y_low_min + ((i - thld) * a_s_high[1])/VALOR_NORMALIZAR))
        

fig=plt.figure(figsize=(30,15))
plt.plot(filt_df_am['airmass_absolute'],simple_uf,'o',markersize=4,label='Datos primera parte')



UF_am=simple_uf
# fig=plt.figure(figsize=(30,15))
# plt.plot(x_low,simple_uf_low,'o',markersize=4,label='Datos primera parte')
# plt.plot(x_high,simple_uf_high,'o',markersize=4,label='Datos primera parte')


# UF_am=np.concatenate((simple_uf_low,simple_uf_high))
# x_am=np.concatenate((x_low,x_high))






#%%Compruebo con un segundo grado
x=filt_df['airmass_absolute'].values
y=filt_df['ISC_IIIV/DII (A m2/W)'].values
yr, RR, a_s, b=E.regresion_polinomica(x, y, 2)

fig=plt.figure(figsize=(30,15))
plt.plot(x,y,'o',markersize=4,label='Datos primera parte')
plt.plot(x,yr,'o',markersize=4,label='Datos primera parte')
plt.xlabel('airmass (n.d.)')
plt.ylabel('ISC_IIIV/DII (A m2/W)')
plt.title('Regresión polinómica de grado 2')
plt.legend()
print('El coeficiente de determinación es de: ', str(RR))





#SE OBTIENE UN RR=0.8549227924488301 Y SIN LA NECESIDAD DE THLD NI DE SEGUNDAS REGRESIONES

#HAY QUE BUSCAR UN VALOR PARA NORMALIZAR LOS RESULTADOS, 
#escojo el mayor obtenido tras la regresion

UF_am_2=yr/VALOR_NORMALIZAR
UF_am_2_retocado=(1-UF_am_2.max())+UF_am_2
fig=plt.figure(figsize=(30,15))
# plt.plot(x,simple_uf,'o',markersize=4,label='Datos primera parte')
plt.plot(x,UF_am_2,'o',markersize=4,label='De forma polinómica de grado 2')
plt.plot(x,UF_am_2_retocado,'o',markersize=4,label='De forma polinómica de grado 2 desplazado')
plt.plot(x, UF_am, 'o', markersize=4, label='De forma lineal')
plt.xlabel('airmass (n.d.)')
plt.ylabel('ISC_IIIV/DII (A m2/W)')
plt.title('Comparación de las dos modelos de UF para el airmass')
plt.legend()



#

#%%Recojo los UF obtenidos y los guardo en un archivo csv



UF['UF_temp']=UF_temp
UF['temp']=filt_df['T_Amb (°C)'].values
UF['UF_am']=UF_am
UF['UF_am_2']=UF_am_2_retocado
UF.to_csv('C://Users/juanj/OneDrive/Escritorio/TFG/UF.csv', index=False)







