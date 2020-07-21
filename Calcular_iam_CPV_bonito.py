# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 15:56:55 2020

@author: juanjo
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import Error 
import plotly.graph_objects as go
from mpl_toolkits.axes_grid1 import host_subplot
#Sentencia para poder expresar las gráfcas en plotly
import plotly.io as pio
pio.renderers.default='browser'
AOILIMIT=55.0

df=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/Datos_filtrados_IIIV.csv',encoding='utf-8')
filt_df2=df[(df['aoi']<AOILIMIT)]
filt_x=filt_df2['aoi']
filt_y=filt_df2['ISC_IIIV/DII (A m2/W)'].values
'''Ahora se estudian las frecuencias de las temperaturas para escoger cúal es más representativa de los datos'''
Incremento=1
Max_temp=math.ceil(filt_df2['T_Amb (ºC)'].max())
Min_temp=math.floor(filt_df2['T_Amb (ºC)'].min())
Temperaturas=[]
rep=[]
for i in range(Min_temp,Max_temp,Incremento):
    AUX=filt_df2[(filt_df2['T_Amb (ºC)']>i)]
    AUX=AUX[((AUX['T_Amb (ºC)'])<i+Incremento)]
    rep.append(AUX['T_Amb (ºC)'].count())
    Temperaturas.append(i)
rep=np.array(rep)
prob=rep/rep.sum()

fig = go.Figure(
    data=[go.Bar(
            x=Temperaturas,
            y=prob)],
    layout_title_text="Histograma con la probabilidad de cada temperatura"
)
fig.update_xaxes(title="Temperaturas (ºC)")
fig.update_yaxes(title="Repeticiones (n.d.)")
fig.show()
#COn el siguiente código se representan los datos en diferentes temperaturas, el incremento es de 1º
#el intervalo es desde el valor más pequeño aumentado en uno, es decir tempera 14 signififca desde el 14 al 15 
#sin incluir. Y des esta forma se puede interaccionar con la gráfica y observar la tendencia por cada temperatura.
Incremento=1
Max_temp=math.ceil(filt_df2['T_Amb (ºC)'].max())
Min_temp=math.floor(filt_df2['T_Amb (ºC)'].min())
fig=go.Figure()
for i in range(Min_temp,Max_temp,Incremento):
    AUX=filt_df2[(filt_df2['T_Amb (ºC)']>=float(i))]
    AUX=AUX[((AUX['T_Amb (ºC)'])<i+Incremento)]    

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
    xaxis_title="Ángulo de incidencia (º)",
    yaxis_title="ISC_IIIV/DII (A m2/W)",
)
fig.show()
'''           CODIGO PARA LA SUPERFCIE                '''

fig = go.Figure(data=[go.Scatter3d(
    x=filt_df2['aoi'],
    y=filt_df2['T_Amb (ºC)'],
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
    xaxis_title="Ángulo de incidencia (º)",
    yaxis_title="ISC_IIIV/DII (A m2/W)",
    scene = dict(
                    xaxis_title='Ángulo de incidencia (º)',
                    yaxis_title='Temperatura ambiente (ºC)',
                    zaxis_title='ISC_IIIV/DII (A m2/W)'),
                    )
fig.show()

''' Código para observar la influencia de las variables sobre los datos y poder escoger un intervalo '''
#Temperatura 

Incremento=1
Max_temp=math.ceil(filt_df2['T_Amb (ºC)'].max())
Min_temp=math.floor(filt_df2['T_Amb (ºC)'].min())
contador=np.arange(Min_temp,Max_temp,Incremento)
fig=go.Figure()
for i in contador:
    AUX=filt_df2[(filt_df2['T_Amb (ºC)']>=float(i))]
    AUX=AUX[((AUX['T_Amb (ºC)'])<(i+Incremento))]    

    fig.add_trace(go.Scatter(
    y=AUX['ISC_IIIV/DII (A m2/W)'],
    x=AUX['aoi'],
    mode='markers',
    visible=True,
    showlegend=True,
    name='Temperatura '+ str(i)
    ))
    
fig.update_layout(
    title="Isc_IIIV/DII en función del ángulo de incidencia para la temperatura de 26ºC",
    xaxis_title="Ángulo de incidencia (º)",
    yaxis_title="ISC_IIIV/DII (A m2/W)",
)
fig.show()
#Velocidad del aire
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
    xaxis_title="Ángulo de incidencia (º)",
    yaxis_title="ISC_IIIV/DII (A m2/W)",
)
fig.show()
#Dirección del viento
Incremento=10
Max_temp=math.ceil(filt_df2['Wind Dir. (m/s)'].max())
Min_temp=math.floor(filt_df2['Wind Dir. (m/s)'].min())
fig=go.Figure()
contador=np.arange(Min_temp,Max_temp,Incremento)
for i in contador:
    AUX=filt_df2[(filt_df2['Wind Dir. (m/s)']>=float(i))]
    AUX=AUX[((AUX['Wind Dir. (m/s)'])<i+Incremento)]    

    fig.add_trace(go.Scatter(
    y=AUX['ISC_IIIV/DII (A m2/W)'],
    x=AUX['aoi'],
    mode='markers',
    visible=True,
    showlegend=True,
    name='Dirección'+ str(i)
    ))
fig.update_layout(
    title="Isc_IIIV/DII en función del ángulo de incidencia, divido por intervalos de dirección del viento",
    xaxis_title="Ángulo de incidencia (º)",
    yaxis_title="ISC_IIIV/DII (A m2/W)",
)
fig.show()
'''Tras varias iteraciones se decide que el filtrado para la obtención del iam es:'''

filt_cuadro2=filt_df2
filt_cuadro2=filt_cuadro2[filt_cuadro2['Wind Dir. (m/s)']>=133.0]
filt_cuadro2=filt_cuadro2[filt_cuadro2['Wind Dir. (m/s)']<143]
filt_cuadro2=filt_cuadro2[filt_cuadro2['Wind Speed (m/s)']>=1.4]
filt_cuadro2=filt_cuadro2[filt_cuadro2['Wind Speed (m/s)']<2.5]
filt_cuadro2=filt_cuadro2[filt_cuadro2['T_Amb (ºC)']>=26.0]
filt_cuadro2=filt_cuadro2[filt_cuadro2['T_Amb (ºC)']<28]

fig=plt.figure(figsize=(30,15))
plt.ylim(0,0.0015 )
plt.plot(filt_df2['aoi'],filt_df2['ISC_IIIV/DII (A m2/W)'], 'o',markersize='2',label='Sin filtrado')    
plt.plot(filt_cuadro2['aoi'],filt_cuadro2['ISC_IIIV/DII (A m2/W)'],'o', markersize='4',label='Con filtrado')    
plt.xlabel('Ángulo de incidencia (º)',fontsize=30)
plt.ylabel('ISC_IIIV/DII (A m2/W)',fontsize=30)
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.legend(fontsize=30,markerscale=3)
plt.title("Datos de eficiencia de captación en función del ángulo de incidencia",fontsize=40)
# ANTES ES NECESARIO AÑADIR UNOS VALORES SINTÉTICOS PARA LIMITAR LAS LIBERTADES DE LAS REGRESIONES POLINÓMICAS ya que los datos no llegan a 0 grados de aoi
df_extrapola=filt_cuadro2
df_extrapola=df_extrapola[df_extrapola['aoi']>=10.0]
df_extrapola=df_extrapola[df_extrapola['aoi']<30]
yr_extrapola, RR_extrapola, a_s_extrapola, b_extrapola=Error.regresion_polinomica(df_extrapola['aoi'].values, df_extrapola['ISC_IIIV/DII (A m2/W)'].values, 1)
x_añadir=np.arange(0,12,0.5)
y_añadir=x_añadir*a_s_extrapola[1]+b_extrapola
x_regresion=np.concatenate((x_añadir,filt_cuadro2['aoi'].values))
y_regresion=np.concatenate((y_añadir,filt_cuadro2['ISC_IIIV/DII (A m2/W)'].values))

fig=plt.figure(figsize=(30,15))
# plt.plot(df_extrapola['aoi'].values,df_extrapola['ISC_IIIV/DII (A m2/W)'].values,'o',markersize=4,label='Datos')
plt.plot(x_regresion,y_regresion,'o',markersize=4,label='Datos añadidos')
plt.plot(filt_cuadro2['aoi'].values,filt_cuadro2['ISC_IIIV/DII (A m2/W)'].values,'o',markersize=4,label='Datos')
plt.xlabel('Ángulo de incidencia (º)',fontsize=30)
plt.ylabel('ISC_IIIV/DII (A m2/W)',fontsize=30)
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.legend(fontsize=30,markerscale=3)
plt.title("Datos de eficiencia de intensidad en función del ángulo de incidencia",fontsize=40)

'''Se guardan los datos filtrados'''
filt_regresion=pd.DataFrame({'aoi':x_regresion,'ISC_IIIV/DII (A m2/W)':y_regresion})
'''Se procede al cálculo del iam'''
#regresiones
x_RR=filt_cuadro2['aoi'].values
y_RR=filt_cuadro2['ISC_IIIV/DII (A m2/W)'].values
#-----Primer grado en dos tramos
aux=np.arange(filt_regresion['aoi'].min(),filt_regresion['aoi'].max(),1) 
thdl=30
RR_max=0.01
for i in aux:
    filt_df_low=filt_regresion[filt_regresion['aoi']<=i]
    filt_df_high=filt_regresion[filt_regresion['aoi']>i]
    x_low=filt_df_low['aoi'].values
    y_low=filt_df_low['ISC_IIIV/DII (A m2/W)'].values
    yr_low, RR_low, a_s_low, b_low=Error.regresion_polinomica(x_low, y_low, 1)    
    x_high=filt_df_high['aoi'].values
    y_high=filt_df_high['ISC_IIIV/DII (A m2/W)'].values
    yr_high, RR_high, a_s_high, b_high=Error.regresion_polinomica(x_high, y_high, 1)
    # y_datos=filt_df['ISC_IIIV/DII (A m2/W)'].values
    y=np.concatenate((y_low,y_high))
    yr=np.concatenate((yr_low,yr_high))
    xr=np.concatenate((x_low,x_high))
    RR=Error.Determination_coefficient(y,yr)   
    if RR_max < RR:
        RR_max=RR
        thld=i
filt_df_low=filt_regresion[filt_regresion['aoi']<=thld]
filt_df_high=filt_regresion[filt_regresion['aoi']>thld]
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
yr_total=np.concatenate((yr_low,yr_high))
RR_poli1=Error.Determination_coefficient(y_total, yr_total)
#----Segundo Grado
y_poli2,RR_poli2,a_s2,b2=Error.regresion_polinomica(filt_regresion['aoi'].values,filt_regresion['ISC_IIIV/DII (A m2/W)'].values,2)
y_p2=a_s2[2]*x_RR**2+a_s2[1]*x_RR+b2
RR_poli2=Error.Determination_coefficient(y_RR,y_p2)
print('MI ERROR ES DE :'+ str(RR_poli2))
#-----Tercer Grado
y_poli3,RR_poli3,a_s3,b3=Error.regresion_polinomica(filt_regresion['aoi'].values,filt_regresion['ISC_IIIV/DII (A m2/W)'].values,3)
y_p3=a_s3[3]*x_RR**3+a_s3[2]*x_RR**2+a_s3[1]*x_RR+b3
RR_poli3=Error.Determination_coefficient(y_RR,y_p3)
print('MI ERROR ES DE :'+ str(RR_poli3))
#Una vez comparados los errores, se normalizan los valores
VALOR_NORMALIZAR=y_poli3.max()
yr_total_normalizado=yr_total/VALOR_NORMALIZAR
y_poli2_normalizado=y_poli2/VALOR_NORMALIZAR
y_poli3_normalizado=y_poli3/VALOR_NORMALIZAR

#-------ashrae
IAM_ashrae,RR_ashrae,b_ashrae=Error.regresion_ashrae(filt_regresion['aoi'].values,filt_regresion['ISC_IIIV/DII (A m2/W)'].values/VALOR_NORMALIZAR)
#b=a1
#-------physical
IAM_physical,RR_physical,n,k,l=Error.regresion_physical(filt_regresion['aoi'].values,filt_regresion['ISC_IIIV/DII (A m2/W)'].values/VALOR_NORMALIZAR)
#n=a1,k=a2,l=a3
#-------Martin Ruiz
IAM_martin_ruiz,RR_martin_ruiz,a_r=Error.regresion_martin_ruiz(filt_regresion['aoi'].values,filt_regresion['ISC_IIIV/DII (A m2/W)'].values/VALOR_NORMALIZAR)
#a_r=a1
x=np.arange(0,55,1)
y3=(a_s3[3]*x**3+a_s3[2]*x**2+a_s3[1]*x+b3)/VALOR_NORMALIZAR
y1=(a_s_low[1]*x+b_low)/VALOR_NORMALIZAR
y2=(a_s2[2]*x**2+a_s2[1]*x+b2)/VALOR_NORMALIZAR



fig=plt.figure(figsize=(30,15))
plt.plot(filt_regresion['aoi'].values,filt_regresion['ISC_IIIV/DII (A m2/W)'].values,'o',markersize=4,label='Datos')
plt.plot(x_total,yr_total,'o',markersize=4,label='Regresión de primer grado')
plt.plot(filt_regresion['aoi'].values,y_poli2,'o',markersize=4,label='Regresión de segundo grado')
plt.plot(filt_regresion['aoi'].values,y_poli3,'o',markersize=4,label='Regresión de tercer grado')
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.xlabel('Ángulo de incidencia (º)',fontsize=30)
plt.ylabel('ISC_IIIV/DII (A m2/W)',fontsize=30)
plt.title('Regresiones polinómicas',fontsize=40)
plt.legend(fontsize=30,markerscale=3) 
valores=[[RR_poli1],
         [RR_poli2],
         [RR_poli3],
         [RR_ashrae],
         [RR_martin_ruiz],
         [RR_physical]]
etiquetas_fil=('Regresión primer grado','Regresión segundo grado',
               'Regresión tercer grado','Ashrae',
               'Martin_ruiz','Physical')
etiquetas_col=(u'Coeficiente de determinación',u'Aproximación')
fig=plt.figure(figsize=(15,10))
plt.plot(filt_regresion['aoi'].values,filt_regresion['ISC_IIIV/DII (A m2/W)'].values/VALOR_NORMALIZAR,'o',markersize=4,label='Datos')
plt.plot(x_total,yr_total_normalizado,'o',markersize=4,label='Regresión de primer grado')
plt.plot(filt_regresion['aoi'].values,y_poli2_normalizado,'o',markersize=4,label='Regresión de segundo grado')
plt.plot(filt_regresion['aoi'].values,y_poli3_normalizado,'o',markersize=4,label='Regresión de tercer grado')
plt.plot(filt_regresion['aoi'].values,IAM_ashrae,'o',markersize=4,label='Ashrae')
plt.plot(filt_regresion['aoi'].values,IAM_physical,'o',markersize=4,label='Physical')
plt.plot(filt_regresion['aoi'].values,IAM_martin_ruiz,'o',markersize=4,label='Martin_ruiz')
plt.table(cellText=valores, rowLabels=etiquetas_fil, colLabels = etiquetas_col,colWidths=[0.3,0.1],  loc='lower center')
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.xlabel('Ángulo de incidencia (º)',fontsize=15)
plt.ylabel('ISC_IIIV/DII (A m2/W)',fontsize=15)
plt.title('Regresiones polinómicas',fontsize=20)
plt.legend()

print('El coeficiente de determinación para la regresión de primer grado es: '+str(RR_poli1))
print('El coeficiente de determinación para la regresión de segundo grado es: '+str(RR_poli2))
print('El coeficiente de determinación para la regresión de tercer grado es: '+str(RR_poli3))
print('El coeficiente de determinación para la regresión de ashrae es: '+str(RR_ashrae))
print('El coeficiente de determinación para la regresión de martin_ruiz es: '+str(RR_martin_ruiz))
print('El coeficiente de determinación para la regresión de physical es: '+str(RR_physical))

iam1_low=[a_s_low[1]/VALOR_NORMALIZAR,0,0,b_low,thld,RR_low]
iam1_high=[a_s_high[1]/VALOR_NORMALIZAR,0,0,b_high,0,RR_low]

iam2=[a_s2[1]/VALOR_NORMALIZAR,a_s2[2]/VALOR_NORMALIZAR,0,b2,0,RR_poli2]

iam3=[a_s3[1]/VALOR_NORMALIZAR,a_s3[2]/VALOR_NORMALIZAR,a_s3[3]/VALOR_NORMALIZAR,b3,0,RR_poli3]

iam_ashrae=[b_ashrae,0,0,0,0,RR_ashrae]
iam_martin_ruiz=[a_r,0,0,0,0,RR_martin_ruiz]
iam_physical=[n,k,l,0,0,RR_physical]

#%% Se almacenan los resultados en un excel 
IAM=pd.DataFrame(columns={'Primer grado low','Primer grado high','Segundo grado','Tercer grado','ashrae','physical','martin_ruiz'},index=['a1','a2','a3','b','thld','RR'])

IAM['Primer grado low']=iam1_low
IAM['Primer grado high']=iam1_high
IAM['Segundo grado']=iam2
IAM['Tercer grado']=iam3
IAM['ashrae']=iam_ashrae
IAM['physical']=iam_physical
IAM['martin_ruiz']=iam_physical

IAM.to_csv("C://Users/juanj/OneDrive/Escritorio/TFG/IAM.csv")













