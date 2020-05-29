# -*- coding: utf-8 -*-


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import Error 
import plotly.graph_objects as go

from mpl_toolkits.axes_grid1 import host_subplot
#Codigo para poder expresar las gráfcas en plotly
import plotly.io as pio
pio.renderers.default='browser'


#AOILIMIT
AOILIMIT=55.0
# Valor_normalizar=0.00091802#Este valor es el valor que Marcos utiliza para normalizar 


df=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/Datos_filtrados_IIIV.csv',encoding='utf-8')


#%%Este es el código para calcular iam cuando AOI<AOILIMIT
#Se recogen en numpy los vectores que se van a usar
# x=df['aoi']
# y=df['ISC_IIIV/DII (A m2/W)'].values


filt_df2=df[(df['aoi']<AOILIMIT)]
filt_x=filt_df2['aoi']
filt_y=filt_df2['ISC_IIIV/DII (A m2/W)'].values


#%%
Incremento=1
Max_temp=math.ceil(filt_df2['T_Amb (°C)'].max())
Min_temp=math.floor(filt_df2['T_Amb (°C)'].min())
Temperaturas=[]
rep=[]
for i in range(Min_temp,Max_temp,Incremento):
    AUX=filt_df2[(filt_df2['T_Amb (°C)']>i)]
    AUX=AUX[((AUX['T_Amb (°C)'])<i+Incremento)]
    rep.append(AUX['T_Amb (°C)'].count())
    Temperaturas.append(i)


rep=np.array(rep)
prob=rep/rep.sum()

fig = go.Figure(
    data=[go.Bar(
            x=Temperaturas,
            y=prob)],
    layout_title_text="Histograma con la probabilidad de cada temperatura"
    
)
fig.update_xaxes(title="Temperaturas (°C)")
fig.update_yaxes(title="Repeticiones (n.d.)")
fig.show()


#COn el siguiente código representamos los datos en fiferentes temperaturas, el incremento es de 1º
#el intervalo es desde el valor más pequeño aumentado en uno, es decir tempera 14 signififca desde el 14 al 15 sin incluir

Incremento=1
Max_temp=math.ceil(filt_df2['T_Amb (°C)'].max())
Min_temp=math.floor(filt_df2['T_Amb (°C)'].min())
fig=go.Figure()
for i in range(Min_temp,Max_temp,Incremento):
    AUX=filt_df2[(filt_df2['T_Amb (°C)']>=float(i))]
    AUX=AUX[((AUX['T_Amb (°C)'])<i+Incremento)]    

    fig.add_trace(go.Scatter(
    y=AUX['ISC_IIIV/DII (A m2/W)'],
    x=AUX['aoi'],
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

####################################CODIGO PARA LA SUPERFCIE#################################
fig = go.Figure(data=[go.Scatter3d(
    x=filt_df2['aoi'],
    y=filt_df2['T_Amb (°C)'],
    z=filt_df2['ISC_IIIV/DII (A m2/W)'],
    mode='markers',
    marker=dict(
        size=1,
        color=df['ISC_IIIV/DII (A m2/W)'],                # set color to an array/list of desired values
        colorscale='Viridis',   # choose a colorscale
        opacity=0.8
    )
)])
fig.update_layout(
    title="Isc_IIIV/DII en función del ángulo de incidencia y temperatura ambiente",
    xaxis_title="Ángulo de incidencia (°)",
    yaxis_title="ISC_IIIV/DII (A m2/W)",
    scene = dict(
                    xaxis_title='Ángulo de incidencia (°)',
                    yaxis_title='Temperatura ambiente (°C)',
                    zaxis_title='ISC_IIIV/DII (A m2/W)'),
                    )
fig.show()




#%%  ##REPRESENTACION DE LA REGRESION DE TODAS LAS TEMPERAURAS
y_poli,RR_poli,a_s,b=Error.regresion_polinomica(filt_x,filt_y,2)
fig=plt.figure(figsize=(30,15))
plt.plot(filt_x,filt_y,'o',markersize=4,label='Datos')
plt.plot(filt_x,y_poli,'o',markersize=4,label='Regresion')
plt.xlabel('Ángulo de incidencia (°)')
plt.ylabel('ISC_IIIV/DII (A m2/W)')
plt.title('Regresión polinómica de grado 2 para todas las temperaturas')
plt.legend()
print('Con el total de los datos')
print(RR_poli)
print('Temperaturas entre '+ str(Min_temp) +' y '+str(Max_temp)+' °C')

#%%
#Hay que tomar una decision, para ver qué tempetura o temperaturas escoger
#sumamos las probabilidades del intervalo escogido (de 19 a 27)
sumatorio=0
for i in range(6,15):
    sumatorio=sumatorio+prob[i]

Max_temp=27.0
Min_temp=19.0

df_filt_temp=filt_df2[(filt_df2['T_Amb (°C)']>=Min_temp)]
df_filt_temp=df_filt_temp[((df_filt_temp['T_Amb (°C)'])<=Max_temp)] 


I_DII=np.array(df_filt_temp['ISC_IIIV/DII (A m2/W)'])
aoi=np.array(df_filt_temp['aoi'])
fig=plt.figure(figsize=(30,15))
y_poli,RR_poli,a_s,b=Error.regresion_polinomica(aoi,I_DII,2)
plt.plot(aoi,I_DII,'o',markersize=4,label='Datos')
plt.plot(aoi,y_poli,'o',markersize=4,label='Regresion')
plt.xlabel('Ángulo de incidencia (°)')
plt.ylabel('ISC_IIIV/DII (A m2/W)')
plt.title('Regresión polinómica de grado 2 para temperaturas entre 19°C y 27°C ')
plt.legend()  
print('Con el '+str(sumatorio)+ 'de los datos')
print(RR_poli)
print('Temperaturas entre '+ str(Min_temp) +' y '+str(Max_temp)+' °C')
    

#%%
#Hay que tomar una decision, para ver qué tempetura o temperaturas escoger
#sumamos las probabilidades del intervalo escogido (26 y 27)
# sumatorio=0
# for i in range(6):
#     sumatorio=sumatorio+prob[i]

Max_temp=28.0
Min_temp=26.0

df_filt_26=filt_df2[(filt_df2['T_Amb (°C)']>=Min_temp)]
df_filt_26=df_filt_26[((df_filt_26['T_Amb (°C)'])<=Max_temp)] 

#%%
# Ahora pasamos al filtrado de los datos entre 26 y 28
for i in df_filt_26.index[:]:
    if (df_filt_26.loc[i]['aoi']<33.0) & (df_filt_26.loc[i]['ISC_IIIV/DII (A m2/W)']<0.000810):
        df_filt_26=df_filt_26.drop(i,axis=0)
    elif (df_filt_26.loc[i]['aoi']<36.5) & (df_filt_26.loc[i]['ISC_IIIV/DII (A m2/W)']<0.000760):
        df_filt_26=df_filt_26.drop(i,axis=0)
#%%
limSup=df_filt_26['aoi'].max()
limInf=df_filt_26['aoi'].min()
Rango=limSup-limInf
n_intervalos=100
porcent_mediana=3
incremento=Rango/n_intervalos
for i in range(n_intervalos):
    AUX=df_filt_26[df_filt_26['aoi']>limInf+i*incremento]
    AUX=AUX[AUX['aoi']<=limInf+incremento*(1+i)]
    Mediana=Error.mediana(AUX['ISC_IIIV/DII (A m2/W)'])
    DEBAJO=AUX[AUX['ISC_IIIV/DII (A m2/W)']<Mediana*(1-porcent_mediana/100)]   
    df_filt_26=df_filt_26.drop(DEBAJO.index[:],axis=0)
    ENCIMA=AUX[AUX['ISC_IIIV/DII (A m2/W)']>Mediana*(1+porcent_mediana/100)]
    df_filt_26=df_filt_26.drop(ENCIMA.index[:],axis=0)


#%%
I_DII=np.array(df_filt_26['ISC_IIIV/DII (A m2/W)'])
aoi=np.array(df_filt_26['aoi'])
fig=plt.figure(figsize=(30,15))
y_poli,RR_poli,a_s,b=Error.regresion_polinomica(aoi,I_DII,2)
plt.plot(aoi,I_DII,'o',markersize=4,label='Datos')
plt.plot(aoi,y_poli,'o',markersize=4,label='Regresion')
plt.xlabel('Ángulo de incidencia (°)')
plt.ylabel('ISC_IIIV/DII (A m2/W)')
plt.title('Regresión polinómica para 26 °C' )
plt.legend()  
print('Con el '+str(prob[13])+ ' de los datos')
print('Coeficiente de determinacion del ' +str(RR_poli))
print('Temperaturas entre '+ str(Min_temp) +' y '+str(Max_temp)+' °C')
# print('El valor de los coeficientes de la regresion son: a_1=' + str(a_s[1])+ ' a_2=' +str(a_s[2]+ ' b='+str(b)))



Incremento=.2
Max_temp=math.ceil(df_filt_26['T_Amb (°C)'].max())
Min_temp=math.floor(df_filt_26['T_Amb (°C)'].min())
contador=np.arange(Min_temp,Max_temp,Incremento)
fig=go.Figure()
for i in contador:
    AUX=df_filt_26[(df_filt_26['T_Amb (°C)']>=float(i))]
    AUX=AUX[((AUX['T_Amb (°C)'])<(i+Incremento))]    

    fig.add_trace(go.Scatter(
    y=AUX['ISC_IIIV/DII (A m2/W)'],
    x=AUX['aoi'],
    mode='markers',
    visible=True,
    showlegend=True,
    name='Temperatura '+ str(i)
    ))
    
fig.update_layout(
    title="Isc_IIIV/DII en función del ángulo de incidencia para la temperatura de 26°C",
    xaxis_title="Ángulo de incidencia (°)",
    yaxis_title="ISC_IIIV/DII (A m2/W)",
)
fig.show()



IAM=y_poli/Valor_normalizar
#%%

Valor_normalizar=0.00096
a1=1.45965860e-05
a2=-3.50234258e-07
b=0.0007236846839700705

datos=np.arange(10,55,0.1)
IAM=(datos*a1+datos**2*a2+b)/Valor_normalizar
IAM2=Error.obtención_dii_efectiva(datos)
fig=plt.figure(figsize=(30,15))
plt.plot(datos,IAM,'o',markersize=4,label='Datos')
plt.plot(datos,IAM2,'o',markersize=4,label='Datos')
plt.xlabel('Ángulo de incidencia (°)')
plt.ylabel('ISC_IIIV/DII (A m2/W)')
plt.title('Regresión polinómica para 26 °C' )
plt.legend()  
 
 
#%%
df_filt_26.to_csv("C://Users/juanj/OneDrive/Escritorio/TFG/IIIV.csv",encoding='utf-8')




#%% Estudiamos el iam añadiendo importancia a la velocidad del viento, ya que se observa que la eficiencia
# depende de esta variable.
Incremento=.1
Max_temp=math.ceil(filt_df2['Wind Speed (m/s)'].max())
Min_temp=math.floor(filt_df2['Wind Speed (m/s)'].min())
fig=go.Figure()
contador=np.arange(Min_temp,Max_temp,Incremento)
for i in contador:
    AUX=filt_df2[(filt_df2['Wind Speed (m/s)']>=float(i))]
    AUX=AUX[((AUX['Wind Speed (m/s)'])<i+Incremento)]    

    fig.add_trace(go.Scatter(
    y=AUX['ISC_IIIV/DII (A m2/W)'],
    x=AUX['aoi'],
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
#%%
#REGRESION FILTRANDO SOLO LA VELOCIDAD DEL VIENTO
filt_df3=filt_df2
filt_df3=filt_df3[filt_df3['Wind Speed (m/s)']<=1.1]
filt_df3=filt_df3[filt_df3['Wind Speed (m/s)']>=.9]

filt_df4=filt_df3
limSup=filt_df3['aoi'].max()
limInf=filt_df3['aoi'].min()
Rango=limSup-limInf
n_intervalos=50
porcent_mediana=5
incremento=Rango/n_intervalos
for i in range(n_intervalos):
    AUX=filt_df4[filt_df4['aoi']>limInf+i*incremento]
    AUX=AUX[AUX['aoi']<=limInf+incremento*(1+i)]
    Mediana=Error.mediana(AUX['ISC_IIIV/DII (A m2/W)'])
    DEBAJO=AUX[AUX['ISC_IIIV/DII (A m2/W)']<Mediana*(1-porcent_mediana/100)]   
    filt_df4=filt_df4.drop(DEBAJO.index[:],axis=0)
    ENCIMA=AUX[AUX['ISC_IIIV/DII (A m2/W)']>Mediana*(1+porcent_mediana/100)]
    filt_df4=filt_df4.drop(ENCIMA.index[:],axis=0)


y_poli,RR_poli,a_s,b=Error.regresion_polinomica(filt_df3['aoi'].values,filt_df3['ISC_IIIV/DII (A m2/W)'].values,2)
y_poli2,RR_poli2,a_s2,b2=Error.regresion_polinomica(filt_df4['aoi'].values,filt_df4['ISC_IIIV/DII (A m2/W)'].values,2)

fig=plt.figure(figsize=(30,15))
plt.plot(filt_df3['aoi'].values,filt_df3['ISC_IIIV/DII (A m2/W)'].values,'o',markersize=4,label='Datos')
plt.plot(filt_df3['aoi'].values,y_poli,'o',markersize=4,label='Datos')
plt.plot(filt_df4['aoi'].values,filt_df4['ISC_IIIV/DII (A m2/W)'].values,'o',markersize=4,label='Datos')
plt.plot(filt_df4['aoi'].values,y_poli2,'o',markersize=4,label='Datos')
plt.xlabel('Ángulo de incidencia (°)')
plt.ylabel('ISC_IIIV/DII (A m2/W)')
plt.title('Regresión polinómica para 26 °C' )
plt.legend()  

#%% 
#CON EL FILTRADO ANTERIOR OBSERVAMOS LA INFLUENCIA DE LA TEMPERATURA
Incremento=1
Max_temp=math.ceil(filt_df3['T_Amb (°C)'].max())
Min_temp=math.floor(filt_df3['T_Amb (°C)'].min())
contador=np.arange(Min_temp,Max_temp,Incremento)
fig=go.Figure()
for i in contador:
    AUX=filt_df3[(filt_df3['T_Amb (°C)']>=float(i))]
    AUX=AUX[((AUX['T_Amb (°C)'])<(i+Incremento))]    

    fig.add_trace(go.Scatter(
    y=AUX['ISC_IIIV/DII (A m2/W)'],
    x=AUX['aoi'],
    mode='markers',
    visible=True,
    showlegend=True,
    name='Temperatura '+ str(i)
    ))
    
fig.update_layout(
    title="Isc_IIIV/DII en función del ángulo de incidencia para la temperatura de 26°C",
    xaxis_title="Ángulo de incidencia (°)",
    yaxis_title="ISC_IIIV/DII (A m2/W)",
)
fig.show()


#%%

fig=plt.figure(figsize=(30,15))
plt.plot(filt_df2['T_Amb (°C)'].values,filt_df2['Wind Speed (m/s)'].values,'o',markersize=4,label='Datos')
plt.xlabel('Ángulo de incidencia (°)')
plt.ylabel('ISC_IIIV/DII (A m2/W)')
plt.title('Regresión polinómica para 26 °C' )
plt.legend()  


filt_cuadro=filt_df2
filt_cuadro=filt_cuadro[filt_cuadro['T_Amb (°C)']>23.0]
filt_cuadro=filt_cuadro[filt_cuadro['T_Amb (°C)']<29]
filt_cuadro=filt_cuadro[filt_cuadro['Wind Speed (m/s)']>=1.0]
filt_cuadro=filt_cuadro[filt_cuadro['Wind Speed (m/s)']<2.5]

fig=plt.figure(figsize=(30,15))
plt.plot(filt_cuadro['aoi'].values,filt_cuadro['ISC_IIIV/DII (A m2/W)'].values,'o',markersize=4,label='Datos')
plt.xlabel('Ángulo de incidencia (°)')
plt.ylabel('ISC_IIIV/DII (A m2/W)')
plt.title('Regresión polinómica para 26 °C' )
plt.legend()  

Incremento=.1
Max_temp=math.ceil(filt_cuadro['Wind Speed (m/s)'].max())
Min_temp=math.floor(filt_cuadro['Wind Speed (m/s)'].min())
fig=go.Figure()
contador=np.arange(Min_temp,Max_temp,Incremento)
for i in contador:
    AUX=filt_cuadro[(filt_cuadro['Wind Speed (m/s)']>=float(i))]
    AUX=AUX[((AUX['Wind Speed (m/s)'])<i+Incremento)]    

    fig.add_trace(go.Scatter(
    y=AUX['ISC_IIIV/DII (A m2/W)'],
    x=AUX['aoi'],
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
Incremento=1
Max_temp=math.ceil(filt_cuadro['T_Amb (°C)'].max())
Min_temp=math.floor(filt_cuadro['T_Amb (°C)'].min())
fig=go.Figure()
contador=np.arange(Min_temp,Max_temp,Incremento)
for i in contador:
    AUX=filt_cuadro[(filt_cuadro['T_Amb (°C)']>=float(i))]
    AUX=AUX[((AUX['T_Amb (°C)'])<i+Incremento)]    

    fig.add_trace(go.Scatter(
    y=AUX['ISC_IIIV/DII (A m2/W)'],
    x=AUX['aoi'],
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


#%%

filt_cuadro2=filt_cuadro
# filt_cuadro2=filt_cuadro2[filt_cuadro2['T_Amb (°C)']>=26.0]
# filt_cuadro2=filt_cuadro2[filt_cuadro2['T_Amb (°C)']<28]
filt_cuadro2=filt_cuadro2[filt_cuadro2['Wind Speed (m/s)']>=2]
filt_cuadro2=filt_cuadro2[filt_cuadro2['Wind Speed (m/s)']<2.5]

fig.show()
Incremento=1
Max_temp=math.ceil(filt_cuadro['T_Amb (°C)'].max())
Min_temp=math.floor(filt_cuadro['T_Amb (°C)'].min())
fig=go.Figure()
contador=np.arange(Min_temp,Max_temp,Incremento)
for i in contador:
    AUX=filt_cuadro[(filt_cuadro['T_Amb (°C)']>=float(i))]
    AUX=AUX[((AUX['T_Amb (°C)'])<i+Incremento)]    

    fig.add_trace(go.Scatter(
    y=AUX['ISC_IIIV/DII (A m2/W)'],
    x=AUX['aoi'],
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
#%%
filt_cuadro2=filt_df2
# filt_cuadro2=filt_cuadro2[filt_cuadro2['T_Amb (°C)']>=26.0]
# filt_cuadro2=filt_cuadro2[filt_cuadro2['T_Amb (°C)']<28]


Incremento=10
Max_temp=153
Min_temp=103
contador=np.arange(Min_temp,Max_temp,Incremento)
fig=go.Figure()
for i in contador:
    AUX=filt_cuadro2[(filt_cuadro2['Wind Dir. (m/s)']>=float(i))]
    AUX=AUX[((AUX['Wind Dir. (m/s)'])<i+Incremento)]    

    fig.add_trace(go.Scatter(
    y=AUX['ISC_IIIV/DII (A m2/W)'],
    x=AUX['aoi'],
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


#%%
#Tras el estudio de las variables anteriormente se determina el siguiente código para la obtencion de IAM

filt_cuadro2=filt_df2
filt_cuadro2=filt_cuadro2[filt_cuadro2['Wind Dir. (m/s)']>=133.0]
filt_cuadro2=filt_cuadro2[filt_cuadro2['Wind Dir. (m/s)']<143]
filt_cuadro2=filt_cuadro2[filt_cuadro2['Wind Speed (m/s)']>=1.4]
filt_cuadro2=filt_cuadro2[filt_cuadro2['Wind Speed (m/s)']<2.5]

filt_prueba=filt_cuadro2
filt_cuadro2=filt_cuadro2[filt_cuadro2['T_Amb (°C)']>=26.0]
filt_cuadro2=filt_cuadro2[filt_cuadro2['T_Amb (°C)']<28]


#ahora buscamos las mejores regresiones
#----poli2
y_poli2,RR_poli2,a_s2,b2=Error.regresion_polinomica(filt_cuadro2['aoi'].values,filt_cuadro2['ISC_IIIV/DII (A m2/W)'].values,2)
#-----poli3
y_poli3,RR_poli3,a_s3,b3=Error.regresion_polinomica(filt_cuadro2['aoi'].values,filt_cuadro2['ISC_IIIV/DII (A m2/W)'].values,3)
#-----poli1
filt_df_low=filt_cuadro2[filt_cuadro2['aoi']<=36.98077777852555]
filt_df_high=filt_cuadro2[filt_cuadro2['aoi']>36.98077777852555]

x_low=filt_df_low['aoi'].values
y_low=filt_df_low['ISC_IIIV/DII (A m2/W)'].values
yr_low, RR_low, a_s_low, b_low=Error.regresion_polinomica(x_low, y_low, 1)

x_high=filt_df_high['aoi'].values
y_high=filt_df_high['ISC_IIIV/DII (A m2/W)'].values
yr_high, RR_high, a_s_high, b_high=Error.regresion_polinomica(x_high, y_high, 1)

a_s1=np.concatenate((a_s_low,a_s_high))
b1=[b_low,b_high]
y_total=np.concatenate((y_low,y_high))
x_total=np.concatenate((x_low,x_high))
y_poli1=np.concatenate((yr_low,yr_high))
RR_poli1=Error.Determination_coefficient(y_total, yr_total)

#-------ashrae

#-------physical

#-------Martin Ruiz


#ESTE PROGRAMA ES PARA AVERIGUAR CUAL ES EL MEJOR THLDS  PARA EL AOI 


# aux=np.arange(filt_cuadro2['aoi'].min(),filt_cuadro2['aoi'].max(),1) 
# thdl=30
# RR_max=0.01
# for i in aux:
#     filt_df_low=filt_cuadro2[filt_cuadro2['aoi']<=i]
#     filt_df_high=filt_cuadro2[filt_cuadro2['aoi']>i]

#     x_low=filt_df_low['aoi'].values
#     y_low=filt_df_low['ISC_IIIV/DII (A m2/W)'].values
#     yr_low, RR_low, a_s_low, b_low=Error.regresion_polinomica(x_low, y_low, 1)
    
#     x_high=filt_df_high['aoi'].values
#     y_high=filt_df_high['ISC_IIIV/DII (A m2/W)'].values
#     yr_high, RR_high, a_s_high, b_high=Error.regresion_polinomica(x_high, y_high, 1)
    

#     # y_datos=filt_df['ISC_IIIV/DII (A m2/W)'].values
#     y=np.concatenate((y_low,y_high))
#     yr=np.concatenate((yr_low,yr_high))
#     xr=np.concatenate((x_low,x_high))
#     RR=Error.Determination_coefficient(y,yr)   
#     if RR_max < RR:
#         RR_max=RR
#         thld=i


fig=plt.figure(figsize=(30,15))
plt.plot(filt_cuadro2['aoi'].values,filt_cuadro2['ISC_IIIV/DII (A m2/W)'].values,'o',markersize=4,label='Datos')
plt.plot(x_total,y_poli1,'o',markersize=4,label='Datos')
plt.plot(filt_cuadro2['aoi'].values,y_poli2,'o',markersize=4,label='Datos')
plt.plot(filt_cuadro2['aoi'].values,y_poli3,'o',markersize=4,label='Datos')
plt.xlabel('Ángulo de incidencia (°)')
plt.ylabel('ISC_IIIV/DII (A m2/W)')
plt.title('Regresión polinómica para 26 °C' )
plt.legend() 
print('El coeficiente de determinación para la regresión de primer grado es: '+str(RR_poli1))
print('El coeficiente de determinación para la regresión de segundo grado es: '+str(RR_poli2))
print('El coeficiente de determinación para la regresión de tercer grado es: '+str(RR_poli3))

fig=plt.figure(figsize=(30,15))
plt.plot(filt_prueba['aoi'].values,filt_prueba['ISC_IIIV/DII (A m2/W)'].values,'o',markersize=4,label='Datos')

plt.xlabel('Ángulo de incidencia (°)')
plt.ylabel('ISC_IIIV/DII (A m2/W)')
plt.title('Regresión polinómica para 26 °C' )
plt.legend() 




#%% PARA CALCULAR EL NUEVO VALOR PARA NORMALIZAR
Valor_normalizar=b3


x=np.arange(0,55,1)
y3=(a_s3[3]*x**3+a_s3[2]*x**2+a_s3[1]*x+b3)/Valor_normalizar
y1=(a_s_low[1]*x+b_low)/Valor_normalizar
y2=(a_s2[2]*x**2+a_s2[1]*x+b2)/Valor_normalizar


fig=plt.figure(figsize=(30,15))
plt.plot(x,y3,'o',markersize=4,label='Datos')
plt.plot(x,y2,'o',markersize=4,label='Datos')
plt.plot(x,y1,'o',markersize=4,label='Datos')

plt.xlabel('Ángulo de incidencia (°)')
plt.ylabel('ISC_IIIV/DII (A m2/W)')
plt.title('Regresión polinómica para 26 °C' )
plt.legend() 
print('El coeficiente de determinación para la regresión de primer grado es: '+str(RR_poli1))
print('El coeficiente de determinación para la regresión de segundo grado es: '+str(RR_poli2))
print('El coeficiente de determinación para la regresión de tercer grado es: '+str(RR_poli3))






a_s=[0,0,0]
b=[0,0,0]
param=[0,0,0]
RR=[0,0,0]


#NORMALIZAMOS



a_s[0]=a_s1/Valor_normalizar
b[0]=b1/Valor_normalizar
param[0]=0
RR[0]=RR_poli1

a_s[1]=a_s2/Valor_normalizar
b[1]=b2/Valor_normalizar
param[1]=0
RR[1]=RR_poli2

a_s[2]=a_s3/Valor_normalizar
b[2]=b3/Valor_normalizar
param[2]=0
RR[2]=RR_poli2


#%%
IAM=pd.DataFrame(columns={'Primer grado','Segundo grado','Tercer grado'},index=['a_s','b','parámetros','RR'])


IAM.loc['a_s']=a_s
IAM.loc['b']=b
IAM.loc['parámetros']=param
IAM.loc['RR']=RR



IAM.to_excel("C://Users/juanj/OneDrive/Escritorio/TFG/IAM.xls")








