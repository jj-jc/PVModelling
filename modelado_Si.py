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
import plotly.graph_objects as go

#Codigo para poder expresar las gráfcas en plotly
import plotly.io as pio
pio.renderers.default='browser'
#AOILIMIT
AOILIMIT=55.0
df=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/filt_df_Si.csv',encoding='utf-8')
smaller_AOI=df[(df['aoi']<AOILIMIT)]
smaller_AOI_=smaller_AOI
greater_AOI=df[(df['aoi']>AOILIMIT)]
filt_x=greater_AOI['aoi'].values
filt_y=greater_AOI['ISC_Si/Irra_vista (A m2/W)'].values
greater_AOI_=greater_AOI

plt.figure(figsize=(30,15))
plt.plot(filt_x,filt_y,'o',markersize=2,label='Previsión actual')
# plt.plot(CPV['aoi'],Potencias_estimadas['Potencias_estimadas (W)'],'o',markersize=2,label='Con UF')
plt.xlabel('Ángulo de incidencia (º)')
plt.ylabel('Eficiencia de intensidad (A m2/W)')
plt.title('Eficiencia de intensidad en función del ángulo de incidencia')
plt.legend()

plt.figure(figsize=(30,15))
plt.plot(greater_AOI['airmass_relative'],filt_y,'o',markersize=2,label='Previsión actual')
# plt.plot(CPV['aoi'],Potencias_estimadas['Potencias_estimadas (W)'],'o',markersize=2,label='Con UF')
plt.xlabel('airmass (n.d.)')
plt.ylabel('Eficiencia de intensidad (A m2/W)')
plt.title('Eficiencia de intensidad en función del airmass')
plt.legend()

plt.figure(figsize=(30,15))
plt.plot(greater_AOI['T_Amb (ºC)'],filt_y,'o',markersize=2,label='Previsión actual')
# plt.plot(CPV['aoi'],Potencias_estimadas['Potencias_estimadas (W)'],'o',markersize=2,label='Con UF')
plt.xlabel('Ángulo de incidencia (º)')
plt.ylabel('Eficiencia de intensidad (A m2/W)')
plt.title('Eficiencia de intensidad en función de la temperatura')
plt.legend()

#------------------------------------------<AOI
plt.figure(figsize=(30,15))
plt.plot(smaller_AOI['aoi'],smaller_AOI['ISC_Si/Irra_vista (A m2/W)'],'o',markersize=2,label='Previsión actual')
# plt.plot(CPV['aoi'],Potencias_estimadas['Potencias_estimadas (W)'],'o',markersize=2,label='Con UF')
plt.xlabel('Ángulo de incidencia (º)')
plt.ylabel('Eficiencia de intensidad (A m2/W)')
plt.title('Eficiencia de intensidad en función del ángulo de incidencia')
plt.legend()

plt.figure(figsize=(30,15))
plt.plot(smaller_AOI['airmass_relative'],smaller_AOI['ISC_Si/Irra_vista (A m2/W)'],'o',markersize=2,label='Previsión actual')
# plt.plot(CPV['aoi'],Potencias_estimadas['Potencias_estimadas (W)'],'o',markersize=2,label='Con UF')
plt.xlabel('airmass (n.d.)')
plt.ylabel('Eficiencia de intensidad (A m2/W)')
plt.title('Eficiencia de intensidad en función del airmass')
plt.legend()

plt.figure(figsize=(30,15))
plt.plot(smaller_AOI['T_Amb (ºC)'],smaller_AOI['ISC_Si/Irra_vista (A m2/W)'],'o',markersize=2,label='Previsión actual')
# plt.plot(CPV['aoi'],Potencias_estimadas['Potencias_estimadas (W)'],'o',markersize=2,label='Con UF')
plt.xlabel('Ángulo de incidencia (º)')
plt.ylabel('Eficiencia de intensidad (A m2/W)')
plt.title('Eficiencia de intensidad en función de la temperatura')
plt.legend()


#%% PROCESO PARA ESTUDIAR EL IAM CUANDO smaller_AOI
Incremento=.1
Max_temp=math.ceil(smaller_AOI['Wind Speed (m/s)'].max())
Min_temp=math.floor(smaller_AOI['Wind Speed (m/s)'].min())
fig=go.Figure()
contador=np.arange(Min_temp,Max_temp,Incremento)
for i in contador:
    AUX=smaller_AOI[(smaller_AOI['Wind Speed (m/s)']>=float(i))]
    AUX=AUX[((AUX['Wind Speed (m/s)'])<i+Incremento)]    

    fig.add_trace(go.Scatter(
    y=AUX['ISC_Si/Irra_vista (A m2/W)'],
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

Incremento=10
Max_temp=math.ceil(smaller_AOI['Wind Dir. (m/s)'].max())
Min_temp=math.floor(smaller_AOI['Wind Dir. (m/s)'].min())
fig=go.Figure()
contador=np.arange(Min_temp,Max_temp,Incremento)
for i in contador:
    AUX=smaller_AOI[(smaller_AOI['Wind Dir. (m/s)']>=float(i))]
    AUX=AUX[((AUX['Wind Dir. (m/s)'])<i+Incremento)]    

    fig.add_trace(go.Scatter(
    y=AUX['ISC_Si/Irra_vista (A m2/W)'],
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

Incremento=1
Max_temp=math.ceil(smaller_AOI['T_Amb (ºC)'].max())
Min_temp=math.floor(smaller_AOI['T_Amb (ºC)'].min())
fig=go.Figure()
contador=np.arange(Min_temp,Max_temp,Incremento)
for i in contador:
    AUX=smaller_AOI[(smaller_AOI['T_Amb (ºC)']>=float(i))]
    AUX=AUX[((AUX['T_Amb (ºC)'])<i+Incremento)]    

    fig.add_trace(go.Scatter(
    y=AUX['ISC_Si/Irra_vista (A m2/W)'],
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
#%% Hacemos el filtrado para el cálculo del iam

smaller_AOI=smaller_AOI[smaller_AOI['T_Amb (ºC)']>=30.0]
# smaller_AOI=smaller_AOI[smaller_AOI['T_Amb (ºC)']>=30]
smaller_AOI=smaller_AOI[smaller_AOI['Wind Speed (m/s)']>=0.8]
smaller_AOI=smaller_AOI[smaller_AOI['Wind Speed (m/s)']<1.2]
smaller_AOI=smaller_AOI[smaller_AOI['Wind Dir. (m/s)']>=79.0]
smaller_AOI=smaller_AOI[smaller_AOI['Wind Dir. (m/s)']<=150.0]

plt.figure(figsize=(30,15))
plt.plot(smaller_AOI_['aoi'].values,smaller_AOI_['ISC_Si/Irra_vista (A m2/W)'].values,'o',markersize=4,label='Datos')
plt.plot(smaller_AOI['aoi'].values,smaller_AOI['ISC_Si/Irra_vista (A m2/W)'].values,'o',markersize=4,label='Datos escogidos')
# plt.plot(CPV['aoi'],Potencias_estimadas['Potencias_estimadas (W)'],'o',markersize=2,label='Con UF')
plt.xlabel('Ángulo de incidencia (º)')
plt.ylabel('Potencia (III-V)(W)')
# plt.title('Comparación de los resultados con los datos estimados de potencias en funcion del UF')
plt.legend()

#%% Vamos a utilizar la media para limpiar los datos sueltos:
#----poli2
y_poli2,RR_poli2,a_s2,b2=Error.regresion_polinomica(smaller_AOI['aoi'].values,smaller_AOI['ISC_Si/Irra_vista (A m2/W)'].values,2)
#-----poli3
y_poli3,RR_poli3,a_s3,b3=Error.regresion_polinomica(smaller_AOI['aoi'].values,smaller_AOI['ISC_Si/Irra_vista (A m2/W)'].values,3)

prueba=smaller_AOI
    
limSup=smaller_AOI['aoi'].max()
limInf=smaller_AOI['aoi'].min()
Rango=limSup-limInf
n_intervalos=4
porcent_mediana=3
incremento=Rango/n_intervalos
for i in range(n_intervalos):
    AUX=smaller_AOI[smaller_AOI['aoi']>limInf+i*incremento]
    AUX=AUX[AUX['aoi']<=limInf+incremento*(1+i)]
    Mediana=Error.mediana(AUX['ISC_Si/Irra_vista (A m2/W)'])
    DEBAJO=AUX[AUX['ISC_Si/Irra_vista (A m2/W)']<Mediana*(1-porcent_mediana/100)]   
    prueba=prueba.drop(DEBAJO.index[:],axis=0)
    ENCIMA=AUX[AUX['ISC_Si/Irra_vista (A m2/W)']>Mediana*(1+porcent_mediana/100)]
    prueba=prueba.drop(ENCIMA.index[:],axis=0)

plt.figure(figsize=(30,15))
plt.plot(smaller_AOI['aoi'].values,smaller_AOI['ISC_Si/Irra_vista (A m2/W)'].values,'o',markersize=4,label='Datos escogidos')
plt.plot(prueba['aoi'].values,prueba['ISC_Si/Irra_vista (A m2/W)'].values,'o',markersize=4,label='Datos')
# plt.plot(CPV['aoi'],Potencias_estimadas['Potencias_estimadas (W)'],'o',markersize=2,label='Con UF')
plt.xlabel('Ángulo de incidencia (º)')
plt.ylabel('Potencia (III-V)(W)')
# plt.title('Comparación de los resultados con los datos estimados de potencias en funcion del UF')
plt.legend()

#----poli2
y_poli2,RR_poli2,a_s2,b2=Error.regresion_polinomica(prueba['aoi'].values,prueba['ISC_Si/Irra_vista (A m2/W)'].values,2)
#-----poli3
y_poli3,RR_poli3,a_s3,b3=Error.regresion_polinomica(prueba['aoi'].values,prueba['ISC_Si/Irra_vista (A m2/W)'].values,3)
x=np.arange(0, 55, 1)
y_2=a_s2[2]*x**2+a_s2[1]*x + b2
y_3=a_s3[3]*x**3+a_s3[2]*x**2+a_s3[1]*x+b3

plt.figure(figsize=(30,20))
plt.plot(prueba['aoi'].values,prueba['ISC_Si/Irra_vista (A m2/W)'].values,'o',markersize=4,label='Datos')
plt.plot(x,y_2,'-',label='Segundo grado')
plt.plot(x,y_3,'-',label='Tercer grado')
plt.legend()

#%%
#COMO en la parte de cpv hace falta añadir unos puntos aritificiales
muestra=prueba[prueba['aoi']>44.0]

y_poli,RR_poli,a_s,b=Error.regresion_polinomica(muestra['aoi'].values,muestra['ISC_Si/Irra_vista (A m2/W)'].values,1)

x_artificial=np.arange(50,56,1)
y_artificial=a_s[1]*x_artificial+b

y_total=np.concatenate((prueba['ISC_Si/Irra_vista (A m2/W)'].values,y_artificial))
x_total=np.concatenate((prueba['aoi'].values,x_artificial))
#----poli2
y_poli2,RR_poli2,a_s2,b2=Error.regresion_polinomica(x_total,y_total,2)
print('EL COEFICIENTE DE DETERMINACIÓN PARA LA REGRESION DE SEGUNDO GRADO CUANDO EL AOI<AOILIMIT' + str(RR_poli2))
#-----poli3
y_poli3,RR_poli3,a_s3,b3=Error.regresion_polinomica(x_total,y_total,3)

x=np.arange(0, 56, 1)
y_2=a_s2[2]*x**2+a_s2[1]*x + b2
y_3=a_s3[3]*x**3+a_s3[2]*x**2+a_s3[1]*x+b3

plt.figure(figsize=(30,20))

plt.plot(x_total,y_total,'o',markersize=4,label='Datos')
plt.plot(x,y_2,'-',label='Segundo grado')
plt.plot(x,y_3,'-',label='Tercer grado')
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.xlabel('Ángulo de incidencia (º)',fontsize=30)
plt.ylabel('ISC_IIIV/DII (A m2/W)',fontsize=30)
plt.title('Regresiones polinómicas',fontsize=40)
plt.legend(fontsize=30,markerscale=3) 

VALOR_NORMALIZAR=y_2.max()
#%%Se estudian las influencias de demás variables en la de estudio.
# Incremento=.1
# Max_temp=math.ceil(greater_AOI['Wind Speed (m/s)'].max())
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
#     xaxis_title="Ángulo de incidencia (º)",
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
#     xaxis_title="Ángulo de incidencia (º)",
#     yaxis_title="ISC_IIIV/DII (A m2/W)",
# )
# fig.show()

# Incremento=1
# Max_temp=math.ceil(filt_df2['T_Amb (ºC)'].max())
# Min_temp=math.floor(filt_df2['T_Amb (ºC)'].min())
# fig=go.Figure()
# contador=np.arange(Min_temp,Max_temp,Incremento)
# for i in contador:
#     AUX=filt_df2[(filt_df2['T_Amb (ºC)']>=float(i))]
#     AUX=AUX[((AUX['T_Amb (ºC)'])<i+Incremento)]    

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
#     xaxis_title="Ángulo de incidencia (º)",
#     yaxis_title="ISC_IIIV/DII (A m2/W)",
# )

# fig.show()

#%% Como se puede observar con el código anterior, existe una linea de tendencia muy clara dependiente de la temperatura
#En este caso se ha escogido una temperatura de 30 a 31 grados centígrados
greater_AOI=greater_AOI[greater_AOI['T_Amb (ºC)']>=30.0]
greater_AOI=greater_AOI[greater_AOI['T_Amb (ºC)']<32]
filt_x=greater_AOI['aoi'].values
filt_y=greater_AOI['ISC_Si/Irra_vista (A m2/W)'].values


plt.figure(figsize=(30,15))
plt.plot(greater_AOI_['aoi'].values,greater_AOI_['ISC_Si/Irra_vista (A m2/W)'].values,'o',markersize=2,label='Previsión actual')
plt.plot(filt_x,filt_y,'o',markersize=2,label='Previsión actual')
# plt.plot(CPV['aoi'],Potencias_estimadas['Potencias_estimadas (W)'],'o',markersize=2,label='Con UF')
plt.xlabel('Ángulo de incidencia (º)')
plt.ylabel('Potencia (III-V)(W)')
# plt.title('Comparación de los resultados con los datos estimados de potencias en funcion del UF')
plt.legend()

plt.figure(figsize=(30,15))
plt.plot(greater_AOI['T_Amb (ºC)'],filt_y,'o',markersize=2,label='Previsión actual')
# plt.plot(CPV['aoi'],Potencias_estimadas['Potencias_estimadas (W)'],'o',markersize=2,label='Con UF')
plt.xlabel('Ángulo de incidencia (º)')
plt.ylabel('Potencia (III-V)(W)')
# plt.title('Comparación de los resultados con los datos estimados de potencias en funcion del UF')
plt.legend()


#REGRESION DE PRIMER GRADO
#ESTE PROGRAMA ES PARA AVERIGUAR CUAL ES EL MEJOR THLDS  PARA EL AOI 
aux=np.arange(greater_AOI['aoi'].min(),greater_AOI['aoi'].max(),1) 
thdl=30
RR_max=0.01
for i in aux:
    filt_df_low=greater_AOI[greater_AOI['aoi']<=i]
    filt_df_high=greater_AOI[greater_AOI['aoi']>i]

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

filt_df_low=greater_AOI[greater_AOI['aoi']<=thld]
filt_df_high=greater_AOI[greater_AOI['aoi']>thld]

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
y_poli2,RR_poli2,a_s2,b2=Error.regresion_polinomica(greater_AOI['aoi'].values,greater_AOI['ISC_Si/Irra_vista (A m2/W)'].values,2)
#-----poli3
y_poli3,RR_poli3,a_s3,b3=Error.regresion_polinomica(greater_AOI['aoi'].values,greater_AOI['ISC_Si/Irra_vista (A m2/W)'].values,3)


valores=[[RR_poli1],
         [RR_poli2],
         [RR_poli3]]
etiquetas_fil=('Regresión primer grado','Regresión segundo grado',
               'Regresión tercer grado')
etiquetas_col=(u'Coeficiente de determinación',u'Aproximación')

fig=plt.figure(figsize=(15,10))
plt.plot(greater_AOI['aoi'].values,greater_AOI['ISC_Si/Irra_vista (A m2/W)'].values,'o',markersize=4,label='Datos')
plt.plot(x_total,yr_total,'o',markersize=4,label='Regresión de primer grado')
plt.plot(greater_AOI['aoi'].values,y_poli2,'o',markersize=4,label='Regresión de segundo grado')
plt.plot(greater_AOI['aoi'].values,y_poli3,'o',markersize=4,label='Regresión de tercer grado')
plt.table(cellText=valores, rowLabels=etiquetas_fil, colLabels = etiquetas_col,colWidths=[0.3,0.1],  loc='lower center')
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.xlabel('Ángulo de incidencia (º)',fontsize=15)
plt.ylabel('ISC_IIIV/DII (A m2/W)',fontsize=15)
plt.title('Regresiones lineales para la obtención del IAM' ,fontsize=20)
plt.legend() 
print('El coeficiente de determinación para la regresión de primer grado es: '+str(RR_poli1))
print('El coeficiente de determinación para la regresión de segundo grado es: '+str(RR_poli2))
print('El coeficiente de determinación para la regresión de tercer grado es: '+str(RR_poli3))


#%% ASIGNAMOS EL VALOR_NORMALIZAR
VALOR_NORMALIZAR=y_poli3.max()
# VALOR_NORMALIZAR=y_poli3.max()
iam1_low=[a_s_low[1]/VALOR_NORMALIZAR,0,0,b_low/VALOR_NORMALIZAR,thld,RR_low]
iam1_high=[a_s_high[1]/VALOR_NORMALIZAR,0,0,b_high/VALOR_NORMALIZAR,0,RR_low]
iam2=[a_s2[1]/VALOR_NORMALIZAR,a_s2[2]/VALOR_NORMALIZAR,0,b2/VALOR_NORMALIZAR,0,RR_poli2]
iam3=[a_s3[1]/VALOR_NORMALIZAR,a_s3[2]/VALOR_NORMALIZAR,a_s3[3]/VALOR_NORMALIZAR,b3/VALOR_NORMALIZAR,0,RR_poli3]
IAM=pd.DataFrame(columns={'Primer grado low','Primer grado high','Segundo grado','Tercer grado'},index=['a1','a2','a3','b','thld','RR'])
IAM['Primer grado low']=iam1_low
IAM['Primer grado high']=iam1_high
IAM['Segundo grado']=iam2
IAM['Tercer grado']=iam3
IAM.to_csv("C://Users/juanj/OneDrive/Escritorio/TFG/IAM_Si.csv")
