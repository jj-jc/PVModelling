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
# Valor_normalizar=0.00091802
# VALOR_NORMALIZAR=0.00096

df=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/Datos_filtrados_IIIV.csv',encoding='utf-8')





filt_df2=df[(df['aoi']<AOILIMIT)]
filt_x=filt_df2['aoi']
filt_y=filt_df2['ISC_IIIV/DII (A m2/W)'].values


#%%
# Incremento=1
# Max_temp=math.ceil(filt_df2['T_Amb (ºC)'].max())
# Min_temp=math.floor(filt_df2['T_Amb (ºC)'].min())
# Temperaturas=[]
# rep=[]
# for i in range(Min_temp,Max_temp,Incremento):
#     AUX=filt_df2[(filt_df2['T_Amb (ºC)']>i)]
#     AUX=AUX[((AUX['T_Amb (ºC)'])<i+Incremento)]
#     rep.append(AUX['T_Amb (ºC)'].count())
#     Temperaturas.append(i)


# rep=np.array(rep)
# prob=rep/rep.sum()

# fig = go.Figure(
#     data=[go.Bar(
#             x=Temperaturas,
#             y=prob)],
#     layout_title_text="Histograma con la probabilidad de cada temperatura"
    
# )
# fig.update_xaxes(title="Temperaturas (ºC)")
# fig.update_yaxes(title="Repeticiones (n.d.)")
# fig.show()


# #COn el siguiente código representamos los datos en fiferentes temperaturas, el incremento es de 1º
# #el intervalo es desde el valor más pequeño aumentado en uno, es decir tempera 14 signififca desde el 14 al 15 sin incluir

# Incremento=1
# Max_temp=math.ceil(filt_df2['T_Amb (ºC)'].max())
# Min_temp=math.floor(filt_df2['T_Amb (ºC)'].min())
# fig=go.Figure()
# for i in range(Min_temp,Max_temp,Incremento):
#     AUX=filt_df2[(filt_df2['T_Amb (ºC)']>=float(i))]
#     AUX=AUX[((AUX['T_Amb (ºC)'])<i+Incremento)]    

#     fig.add_trace(go.Scatter(
#     y=AUX['ISC_IIIV/DII (A m2/W)'],
#     x=AUX['aoi'],
#     mode='markers',
#     visible=True,
#     showlegend=True,
#     name='Temperatura '+ str(i)
#     ))
# fig.update_layout(
#     title="Isc_IIIV/DII en función del ángulo de incidencia, divido por intervalos de temperatura",
#     xaxis_title="Ángulo de incidencia (º)",
#     yaxis_title="ISC_IIIV/DII (A m2/W)",
# )


# fig.show()

# ####################################CODIGO PARA LA SUPERFCIE#################################
# fig = go.Figure(data=[go.Scatter3d(
#     x=filt_df2['aoi'],
#     y=filt_df2['T_Amb (ºC)'],
#     z=filt_df2['ISC_IIIV/DII (A m2/W)'],
#     mode='markers',
#     marker=dict(
#         size=1,
#         color=df['ISC_IIIV/DII (A m2/W)'],                # set color to an array/list of desired values
#         colorscale='Viridis',   # choose a colorscale
#         opacity=0.8
#     )
# )])
# fig.update_layout(
#     title="Isc_IIIV/DII en función del ángulo de incidencia y temperatura ambiente",
#     xaxis_title="Ángulo de incidencia (º)",
#     yaxis_title="ISC_IIIV/DII (A m2/W)",
#     scene = dict(
#                     xaxis_title='Ángulo de incidencia (º)',
#                     yaxis_title='Temperatura ambiente (ºC)',
#                     zaxis_title='ISC_IIIV/DII (A m2/W)'),
#                     )
# fig.show()




#%%  ##REPRESENTACION DE LA REGRESION DE TODAS LAS TEMPERAURAS
# y_poli,RR_poli,a_s,b=Error.regresion_polinomica(filt_x,filt_y,2)
# fig=plt.figure(figsize=(30,15))
# plt.plot(filt_x,filt_y,'o',markersize=4,label='Datos')
# plt.plot(filt_x,y_poli,'o',markersize=4,label='Regresion')
# plt.xlabel('Ángulo de incidencia (º)')
# plt.ylabel('ISC_IIIV/DII (A m2/W)')
# plt.title('Regresión polinómica de grado 2 para todas las temperaturas')
# plt.legend()
# print('Con el total de los datos')
# print(RR_poli)
# print('Temperaturas entre '+ str(Min_temp) +' y '+str(Max_temp)+' ºC')

#%%
#Hay que tomar una decision, para ver qué tempetura o temperaturas escoger
#sumamos las probabilidades del intervalo escogido (de 19 a 27)
# sumatorio=0
# for i in range(6,15):
#     sumatorio=sumatorio+prob[i]

# Max_temp=27.0
# Min_temp=19.0

# df_filt_temp=filt_df2[(filt_df2['T_Amb (ºC)']>=Min_temp)]
# df_filt_temp=df_filt_temp[((df_filt_temp['T_Amb (ºC)'])<=Max_temp)] 


# I_DII=np.array(df_filt_temp['ISC_IIIV/DII (A m2/W)'])
# aoi=np.array(df_filt_temp['aoi'])
# fig=plt.figure(figsize=(30,15))
# y_poli,RR_poli,a_s,b=Error.regresion_polinomica(aoi,I_DII,2)
# plt.plot(aoi,I_DII,'o',markersize=4,label='Datos')
# plt.plot(aoi,y_poli,'o',markersize=4,label='Regresion')
# plt.xlabel('Ángulo de incidencia (º)')
# plt.ylabel('ISC_IIIV/DII (A m2/W)')
# plt.title('Regresión polinómica de grado 2 para temperaturas entre 19ºC y 27ºC ')
# plt.legend()  
# print('Con el '+str(sumatorio)+ 'de los datos')
# print(RR_poli)
# print('Temperaturas entre '+ str(Min_temp) +' y '+str(Max_temp)+' ºC')
    

# #%%
# #Hay que tomar una decision, para ver qué tempetura o temperaturas escoger
# #sumamos las probabilidades del intervalo escogido (26 y 27)
# # sumatorio=0
# # for i in range(6):
# #     sumatorio=sumatorio+prob[i]

# Max_temp=28.0
# Min_temp=26.0

# df_filt_26=filt_df2[(filt_df2['T_Amb (ºC)']>=Min_temp)]
# df_filt_26=df_filt_26[((df_filt_26['T_Amb (ºC)'])<=Max_temp)] 

# #%%
# # Ahora pasamos al filtrado de los datos entre 26 y 28
# for i in df_filt_26.index[:]:
#     if (df_filt_26.loc[i]['aoi']<33.0) & (df_filt_26.loc[i]['ISC_IIIV/DII (A m2/W)']<0.000810):
#         df_filt_26=df_filt_26.drop(i,axis=0)
#     elif (df_filt_26.loc[i]['aoi']<36.5) & (df_filt_26.loc[i]['ISC_IIIV/DII (A m2/W)']<0.000760):
#         df_filt_26=df_filt_26.drop(i,axis=0)
# #%%
# limSup=df_filt_26['aoi'].max()
# limInf=df_filt_26['aoi'].min()
# Rango=limSup-limInf
# n_intervalos=100
# porcent_mediana=3
# incremento=Rango/n_intervalos
# for i in range(n_intervalos):
#     AUX=df_filt_26[df_filt_26['aoi']>limInf+i*incremento]
#     AUX=AUX[AUX['aoi']<=limInf+incremento*(1+i)]
#     Mediana=Error.mediana(AUX['ISC_IIIV/DII (A m2/W)'])
#     DEBAJO=AUX[AUX['ISC_IIIV/DII (A m2/W)']<Mediana*(1-porcent_mediana/100)]   
#     df_filt_26=df_filt_26.drop(DEBAJO.index[:],axis=0)
#     ENCIMA=AUX[AUX['ISC_IIIV/DII (A m2/W)']>Mediana*(1+porcent_mediana/100)]
#     df_filt_26=df_filt_26.drop(ENCIMA.index[:],axis=0)


# #%%
# I_DII=np.array(df_filt_26['ISC_IIIV/DII (A m2/W)'])
# aoi=np.array(df_filt_26['aoi'])
# fig=plt.figure(figsize=(30,15))
# y_poli,RR_poli,a_s,b=Error.regresion_polinomica(aoi,I_DII,2)
# plt.plot(aoi,I_DII,'o',markersize=4,label='Datos')
# plt.plot(aoi,y_poli,'o',markersize=4,label='Regresion')
# plt.xlabel('Ángulo de incidencia (º)')
# plt.ylabel('ISC_IIIV/DII (A m2/W)')
# plt.title('Regresión polinómica para 26 ºC' )
# plt.legend()  
# print('Con el '+str(prob[13])+ ' de los datos')
# print('Coeficiente de determinacion del ' +str(RR_poli))
# print('Temperaturas entre '+ str(Min_temp) +' y '+str(Max_temp)+' ºC')
# # print('El valor de los coeficientes de la regresion son: a_1=' + str(a_s[1])+ ' a_2=' +str(a_s[2]+ ' b='+str(b)))



# Incremento=.2
# Max_temp=math.ceil(df_filt_26['T_Amb (ºC)'].max())
# Min_temp=math.floor(df_filt_26['T_Amb (ºC)'].min())
# contador=np.arange(Min_temp,Max_temp,Incremento)
# fig=go.Figure()
# for i in contador:
#     AUX=df_filt_26[(df_filt_26['T_Amb (ºC)']>=float(i))]
#     AUX=AUX[((AUX['T_Amb (ºC)'])<(i+Incremento))]    

#     fig.add_trace(go.Scatter(
#     y=AUX['ISC_IIIV/DII (A m2/W)'],
#     x=AUX['aoi'],
#     mode='markers',
#     visible=True,
#     showlegend=True,
#     name='Temperatura '+ str(i)
#     ))
    
# fig.update_layout(
#     title="Isc_IIIV/DII en función del ángulo de incidencia para la temperatura de 26ºC",
#     xaxis_title="Ángulo de incidencia (º)",
#     yaxis_title="ISC_IIIV/DII (A m2/W)",
# )
# fig.show()



# IAM=y_poli/Valor_normalizar
#%%

# Valor_normalizar=0.00096
# a1=1.45965860e-05
# a2=-3.50234258e-07
# b=0.0007236846839700705

# datos=np.arange(10,55,0.1)
# IAM=(datos*a1+datos**2*a2+b)/Valor_normalizar
# IAM2=Error.obtencion_dii_efectiva(datos)
# fig=plt.figure(figsize=(30,15))
# plt.plot(datos,IAM,'o',markersize=4,label='Datos')
# plt.plot(datos,IAM2,'o',markersize=4,label='Datos')
# plt.xlabel('Ángulo de incidencia (º)')
# plt.ylabel('ISC_IIIV/DII (A m2/W)')
# plt.title('Regresión polinómica para 26 ºC' )
# plt.legend()  
 
 
#%%
# df_filt_26.to_csv("C://Users/juanj/OneDrive/Escritorio/TFG/IIIV.csv",encoding='utf-8')




#%% Estudiamos el iam añadiendo importancia a la velocidad del viento, ya que se observa que la eficiencia
# depende de esta variable.
# Incremento=.1
# Max_temp=math.ceil(filt_df2['Wind Speed (m/s)'].max())
# Min_temp=math.floor(filt_df2['Wind Speed (m/s)'].min())
# fig=go.Figure()
# contador=np.arange(Min_temp,Max_temp,Incremento)
# for i in contador:
#     AUX=filt_df2[(filt_df2['Wind Speed (m/s)']>=float(i))]
#     AUX=AUX[((AUX['Wind Speed (m/s)'])<i+Incremento)]    

#     fig.add_trace(go.Scatter(
#     y=AUX['ISC_IIIV/DII (A m2/W)'],
#     x=AUX['aoi'],
#     mode='markers',
#     visible=True,
#     showlegend=True,
#     name='Velocidad '+ str(i)
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
#     y=AUX['ISC_IIIV/DII (A m2/W)'],
#     x=AUX['aoi'],
#     mode='markers',
#     visible=True,
#     showlegend=True,
#     name='Dirección'+ str(i)
#     ))
# fig.update_layout(
#     title="Isc_IIIV/DII en función del ángulo de incidencia, divido por intervalos de dirección del viento",
#     xaxis_title="Ángulo de incidencia (º)",
#     yaxis_title="ISC_IIIV/DII (A m2/W)",
# )

# fig.show()





#%%
# #REGRESION FILTRANDO SOLO LA VELOCIDAD DEL VIENTO
# filt_df3=filt_df2
# filt_df3=filt_df3[filt_df3['Wind Speed (m/s)']<=1.1]
# filt_df3=filt_df3[filt_df3['Wind Speed (m/s)']>=.9]

# filt_df4=filt_df3
# limSup=filt_df3['aoi'].max()
# limInf=filt_df3['aoi'].min()
# Rango=limSup-limInf
# n_intervalos=50
# porcent_mediana=5
# incremento=Rango/n_intervalos
# for i in range(n_intervalos):
#     AUX=filt_df4[filt_df4['aoi']>limInf+i*incremento]
#     AUX=AUX[AUX['aoi']<=limInf+incremento*(1+i)]
#     Mediana=Error.mediana(AUX['ISC_IIIV/DII (A m2/W)'])
#     DEBAJO=AUX[AUX['ISC_IIIV/DII (A m2/W)']<Mediana*(1-porcent_mediana/100)]   
#     filt_df4=filt_df4.drop(DEBAJO.index[:],axis=0)
#     ENCIMA=AUX[AUX['ISC_IIIV/DII (A m2/W)']>Mediana*(1+porcent_mediana/100)]
#     filt_df4=filt_df4.drop(ENCIMA.index[:],axis=0)


# y_poli,RR_poli,a_s,b=Error.regresion_polinomica(filt_df3['aoi'].values,filt_df3['ISC_IIIV/DII (A m2/W)'].values,2)
# y_poli2,RR_poli2,a_s2,b2=Error.regresion_polinomica(filt_df4['aoi'].values,filt_df4['ISC_IIIV/DII (A m2/W)'].values,2)

# fig=plt.figure(figsize=(30,15))
# plt.plot(filt_df3['aoi'].values,filt_df3['ISC_IIIV/DII (A m2/W)'].values,'o',markersize=4,label='Datos')
# plt.plot(filt_df3['aoi'].values,y_poli,'o',markersize=4,label='Datos')
# plt.plot(filt_df4['aoi'].values,filt_df4['ISC_IIIV/DII (A m2/W)'].values,'o',markersize=4,label='Datos')
# plt.plot(filt_df4['aoi'].values,y_poli2,'o',markersize=4,label='Datos')
# plt.xlabel('Ángulo de incidencia (º)')
# plt.ylabel('ISC_IIIV/DII (A m2/W)')
# plt.title('Regresión polinómica para 26 ºC' )
# plt.legend()  

#%% 
#CON EL FILTRADO ANTERIOR OBSERVAMOS LA INFLUENCIA DE LA TEMPERATURA
# Incremento=1
# Max_temp=math.ceil(filt_df3['T_Amb (ºC)'].max())
# Min_temp=math.floor(filt_df3['T_Amb (ºC)'].min())
# contador=np.arange(Min_temp,Max_temp,Incremento)
# fig=go.Figure()
# for i in contador:
#     AUX=filt_df3[(filt_df3['T_Amb (ºC)']>=float(i))]
#     AUX=AUX[((AUX['T_Amb (ºC)'])<(i+Incremento))]    

#     fig.add_trace(go.Scatter(
#     y=AUX['ISC_IIIV/DII (A m2/W)'],
#     x=AUX['aoi'],
#     mode='markers',
#     visible=True,
#     showlegend=True,
#     name='Temperatura '+ str(i)
#     ))
    
# fig.update_layout(
#     title="Isc_IIIV/DII en función del ángulo de incidencia para la temperatura de 26ºC",
#     xaxis_title="Ángulo de incidencia (º)",
#     yaxis_title="ISC_IIIV/DII (A m2/W)",
# )
# fig.show()


# #%%

# fig=plt.figure(figsize=(30,15))
# plt.plot(filt_df2['T_Amb (ºC)'].values,filt_df2['Wind Speed (m/s)'].values,'o',markersize=4,label='Datos')
# plt.xlabel('Ángulo de incidencia (º)')
# plt.ylabel('ISC_IIIV/DII (A m2/W)')
# plt.title('Regresión polinómica para 26 ºC' )
# plt.legend()  


# filt_cuadro=filt_df2
# filt_cuadro=filt_cuadro[filt_cuadro['T_Amb (ºC)']>23.0]
# filt_cuadro=filt_cuadro[filt_cuadro['T_Amb (ºC)']<29]
# filt_cuadro=filt_cuadro[filt_cuadro['Wind Speed (m/s)']>=1.0]
# filt_cuadro=filt_cuadro[filt_cuadro['Wind Speed (m/s)']<2.5]

# fig=plt.figure(figsize=(30,15))
# plt.plot(filt_cuadro['aoi'].values,filt_cuadro['ISC_IIIV/DII (A m2/W)'].values,'o',markersize=4,label='Datos')
# plt.xlabel('Ángulo de incidencia (º)')
# plt.ylabel('ISC_IIIV/DII (A m2/W)')
# plt.title('Regresión polinómica para 26 ºC' )
# plt.legend()  

# Incremento=.1
# Max_temp=math.ceil(filt_cuadro['Wind Speed (m/s)'].max())
# Min_temp=math.floor(filt_cuadro['Wind Speed (m/s)'].min())
# fig=go.Figure()
# contador=np.arange(Min_temp,Max_temp,Incremento)
# for i in contador:
#     AUX=filt_cuadro[(filt_cuadro['Wind Speed (m/s)']>=float(i))]
#     AUX=AUX[((AUX['Wind Speed (m/s)'])<i+Incremento)]    

#     fig.add_trace(go.Scatter(
#     y=AUX['ISC_IIIV/DII (A m2/W)'],
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
# Max_temp=math.ceil(filt_cuadro['T_Amb (ºC)'].max())
# Min_temp=math.floor(filt_cuadro['T_Amb (ºC)'].min())
# fig=go.Figure()
# contador=np.arange(Min_temp,Max_temp,Incremento)
# for i in contador:
#     AUX=filt_cuadro[(filt_cuadro['T_Amb (ºC)']>=float(i))]
#     AUX=AUX[((AUX['T_Amb (ºC)'])<i+Incremento)]    

#     fig.add_trace(go.Scatter(
#     y=AUX['ISC_IIIV/DII (A m2/W)'],
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


#%%

# filt_cuadro2=filt_cuadro
# # filt_cuadro2=filt_cuadro2[filt_cuadro2['T_Amb (ºC)']>=26.0]
# # filt_cuadro2=filt_cuadro2[filt_cuadro2['T_Amb (ºC)']<28]
# filt_cuadro2=filt_cuadro2[filt_cuadro2['Wind Speed (m/s)']>=2]
# filt_cuadro2=filt_cuadro2[filt_cuadro2['Wind Speed (m/s)']<2.5]

# fig.show()
# Incremento=1
# Max_temp=math.ceil(filt_cuadro['T_Amb (ºC)'].max())
# Min_temp=math.floor(filt_cuadro['T_Amb (ºC)'].min())
# fig=go.Figure()
# contador=np.arange(Min_temp,Max_temp,Incremento)
# for i in contador:
#     AUX=filt_cuadro[(filt_cuadro['T_Amb (ºC)']>=float(i))]
#     AUX=AUX[((AUX['T_Amb (ºC)'])<i+Incremento)]    

#     fig.add_trace(go.Scatter(
#     y=AUX['ISC_IIIV/DII (A m2/W)'],
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
#%%
# filt_cuadro2=filt_df2
# # filt_cuadro2=filt_cuadro2[filt_cuadro2['T_Amb (ºC)']>=26.0]
# # filt_cuadro2=filt_cuadro2[filt_cuadro2['T_Amb (ºC)']<28]


# Incremento=10
# Max_temp=153
# Min_temp=103
# contador=np.arange(Min_temp,Max_temp,Incremento)
# fig=go.Figure()
# for i in contador:
#     AUX=filt_cuadro2[(filt_cuadro2['Wind Dir. (m/s)']>=float(i))]
#     AUX=AUX[((AUX['Wind Dir. (m/s)'])<i+Incremento)]    

#     fig.add_trace(go.Scatter(
#     y=AUX['ISC_IIIV/DII (A m2/W)'],
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


#%%
#Tras el estudio de las variables anteriormente se determina el siguiente código para la obtencion de IAM

filt_cuadro2=filt_df2
filt_cuadro2=filt_cuadro2[filt_cuadro2['Wind Dir. (m/s)']>=133.0]
filt_cuadro2=filt_cuadro2[filt_cuadro2['Wind Dir. (m/s)']<143]
filt_cuadro2=filt_cuadro2[filt_cuadro2['Wind Speed (m/s)']>=1.4]
filt_cuadro2=filt_cuadro2[filt_cuadro2['Wind Speed (m/s)']<2.5]

filt_prueba=filt_cuadro2
filt_cuadro2=filt_cuadro2[filt_cuadro2['T_Amb (ºC)']>=26.0]
filt_cuadro2=filt_cuadro2[filt_cuadro2['T_Amb (ºC)']<28]

#%%ANTES ES NECESARIO AÑADIR UNOS VALORES SINTÉTICOS PARA LIMITAR LAS LIBERTADES DE LAS REGRESIONES POLINÓMICAS ya que los datos no llegan a 0 grados de aoi

df_extrapola=filt_cuadro2
df_extrapola=df_extrapola[df_extrapola['aoi']>=10.0]
df_extrapola=df_extrapola[df_extrapola['aoi']<30]
yr_extrapola, RR_extrapola, a_s_extrapola, b_extrapola=Error.regresion_polinomica(df_extrapola['aoi'].values, df_extrapola['ISC_IIIV/DII (A m2/W)'].values, 1)
x_añadir=np.arange(0,12,.5)
y_añadir=x_añadir*a_s_extrapola[1]+b_extrapola

'''AHORA VOY A CREAR DOS VECTORES QUE RECOGERÁN TODOS LOS DATOS A APROXIMAR'''
x_regresion=np.concatenate((x_añadir,filt_cuadro2['aoi'].values))
y_regresion=np.concatenate((y_añadir,filt_cuadro2['ISC_IIIV/DII (A m2/W)'].values))

fig=plt.figure(figsize=(30,15))
plt.plot(df_extrapola['aoi'].values,df_extrapola['ISC_IIIV/DII (A m2/W)'].values,'o',markersize=4,label='Datos')
plt.plot(x_regresion,y_regresion,'o',markersize=4,label='Datos escogidos')
plt.plot(filt_cuadro2['aoi'].values,filt_cuadro2['ISC_IIIV/DII (A m2/W)'].values,'o',markersize=4,label='Datos')


#%% RECOGEMOS LOS DATOS IMPORTANTES Y LOS GUARDAMOS EN UN EXCEL PARA MANTENERLOS Y PORDE ENVIARSELOS A LA CLASE


filt_regresion=pd.DataFrame({'aoi':x_regresion,'ISC_IIIV/DII (A m2/W)':y_regresion})




#%%

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

x_RR=filt_cuadro2['aoi'].values
y_RR=filt_cuadro2['ISC_IIIV/DII (A m2/W)'].values
#ahora buscamos las mejores regresiones
#----poli2
y_poli2,RR_poli2,a_s2,b2=Error.regresion_polinomica(filt_regresion['aoi'].values,filt_regresion['ISC_IIIV/DII (A m2/W)'].values,2)
y_p2=a_s2[2]*x_RR**2+a_s2[1]*x_RR+b2
RR_poli2=Error.Determination_coefficient(y_RR,y_p2)
print('MI ERROR ES DE :'+ str(RR_poli2))
#-----poli3
y_poli3,RR_poli3,a_s3,b3=Error.regresion_polinomica(filt_regresion['aoi'].values,filt_regresion['ISC_IIIV/DII (A m2/W)'].values,3)
y_p3=a_s3[3]*x_RR**3+a_s3[2]*x_RR**2+a_s3[1]*x_RR+b3
RR_poli3=Error.Determination_coefficient(y_RR,y_p3)
print('MI ERROR ES DE :'+ str(RR_poli3))


VALOR_NORMALIZAR=y_poli3.max()


#-----poli1
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

#-------ashrae
IAM_ashrae,RR_ashrae,b_ashrae=Error.regresion_ashrae(filt_regresion['aoi'].values,filt_regresion['ISC_IIIV/DII (A m2/W)'].values/VALOR_NORMALIZAR)
#b=a1

#-------physical
IAM_physical,RR_physical,n,k,l=Error.regresion_physical(filt_regresion['aoi'].values,filt_regresion['ISC_IIIV/DII (A m2/W)'].values/VALOR_NORMALIZAR)
#n=a1,k=a2,l=a3

#-------Martin Ruiz
IAM_martin_ruiz,RR_martin_ruiz,a_r=Error.regresion_martin_ruiz(filt_regresion['aoi'].values,filt_regresion['ISC_IIIV/DII (A m2/W)'].values/VALOR_NORMALIZAR)
#a_r=a1

fig=plt.figure(figsize=(30,15))
plt.plot(filt_df2['aoi'].values,filt_df2['ISC_IIIV/DII (A m2/W)'].values,'o',markersize=4,label='Datos')
plt.plot(filt_cuadro2['aoi'].values,filt_cuadro2['ISC_IIIV/DII (A m2/W)'].values,'o',markersize=4,label='Datos escogidos')

plt.xlabel('Ángulo de incidencia (º)')
plt.ylabel('ISC_IIIV/DII (A m2/W)')
plt.title('Datos filtrados para 26 ºC' )
plt.legend()

fig=plt.figure(figsize=(30,15))
plt.plot(filt_regresion['aoi'].values,filt_regresion['ISC_IIIV/DII (A m2/W)'].values,'o',markersize=4,label='Datos')
plt.plot(x_total,yr_total,'o',markersize=4,label='regresión de primer grado')
plt.plot(filt_regresion['aoi'].values,y_poli2,'o',markersize=4,label='regresión de segundo grado')
plt.plot(filt_regresion['aoi'].values,y_poli3,'o',markersize=4,label='regresión de tercer grado')

plt.xlabel('Ángulo de incidencia (º)')
plt.ylabel('ISC_IIIV/DII (A m2/W)')
plt.title('Regresión polinómica para 26 ºC' )
plt.legend() 
print('El coeficiente de determinación para la regresión de primer grado es: '+str(RR_poli1))
print('El coeficiente de determinación para la regresión de segundo grado es: '+str(RR_poli2))
print('El coeficiente de determinación para la regresión de tercer grado es: '+str(RR_poli3))
print('El coeficiente de determinación para la regresión de ashrae es: '+str(RR_ashrae))
print('El coeficiente de determinación para la regresión de martin_ruiz es: '+str(RR_martin_ruiz))
print('El coeficiente de determinación para la regresión de physical es: '+str(RR_physical))

# fig=plt.figure(figsize=(30,15))
# plt.plot(filt_prueba['aoi'].values,filt_prueba['ISC_IIIV/DII (A m2/W)'].values,'o',markersize=4,label='Datos')

# plt.xlabel('Ángulo de incidencia (º)')
# plt.ylabel('ISC_IIIV/DII (A m2/W)')
# plt.title('Regresión polinómica para 26 ºC' )
# plt.legend() 




#%% PARA CALCULAR EL NUEVO VALOR PARA NORMALIZAR

#este no puede ser el valor para normzalizar, debido que tiene la influecnia del aoi. Por ello no está corregido 
#y como no está corregido, no se conoce el valor de ISC/DII normal.
VALOR_NORMALIZAR=y_poli3.max()

x=np.arange(0,55,1)
y3=(a_s3[3]*x**3+a_s3[2]*x**2+a_s3[1]*x+b3)/VALOR_NORMALIZAR
y1=(a_s_low[1]*x+b_low)/VALOR_NORMALIZAR
y2=(a_s2[2]*x**2+a_s2[1]*x+b2)/VALOR_NORMALIZAR

 

fig=plt.figure(figsize=(30,15))
plt.plot(filt_cuadro2['aoi'].values,filt_cuadro2['ISC_IIIV/DII (A m2/W)'].values/VALOR_NORMALIZAR,'o',markersize=4,label='IAM_tercer_grado')
plt.plot(x,y3,'o',markersize=4,label='IAM_tercer_grado')
plt.plot(x,y2,'o',markersize=4,label='IAM_segundo_grado')
plt.plot(x,y1,'o',markersize=4,label='IAM_primer_grado')
plt.plot(filt_regresion['aoi'].values,IAM_martin_ruiz,'o',markersize=4,label='IAM_martin_ruiz')
plt.plot(filt_regresion['aoi'].values,IAM_ashrae,'o',markersize=4,label='IAM_ashrae')
plt.plot(filt_regresion['aoi'].values,IAM_physical,'o',markersize=4,label='IAM_physical')

plt.xlabel('Ángulo de incidencia (º)')
plt.ylabel('ISC_IIIV/DII (A m2/W)')
plt.title('Regresión polinómica para 26 ºC' )
plt.legend() 
# print('El coeficiente de determinación para la regresión de primer grado es: '+str(RR_poli1))
# print('El coeficiente de determinación para la regresión de segundo grado es: '+str(RR_poli2))
# print('El coeficiente de determinación para la regresión de tercer grado es: '+str(RR_poli3))

# estructura para el dataframe
# [a1,a2,a3,b,thld,RR] con la peculiaridad de que, el iam es el que nos va a determinar el valor a normalizar por medio de la b, por lo qu eeste valor no se 
#normalizará (daría 1) y además nos da la información del valor a normalizar para los factores de utilización.
iam1_low=[a_s_low[1]/VALOR_NORMALIZAR,0,0,b_low,thld,RR_low]
iam1_high=[a_s_high[1]/VALOR_NORMALIZAR,0,0,b_high,0,RR_low]

iam2=[a_s2[1]/VALOR_NORMALIZAR,a_s2[2]/VALOR_NORMALIZAR,0,b2,0,RR_poli2]

iam3=[a_s3[1]/VALOR_NORMALIZAR,a_s3[2]/VALOR_NORMALIZAR,a_s3[3]/VALOR_NORMALIZAR,b3,0,RR_poli3]

iam_ashrae=[b_ashrae,0,0,0,0,RR_ashrae]
iam_martin_ruiz=[a_r,0,0,0,0,RR_martin_ruiz]
iam_physical=[n,k,l,0,0,RR_physical]


#%%
IAM=pd.DataFrame(columns={'Primer grado low','Primer grado high','Segundo grado','Tercer grado','ashrae','physical','martin_ruiz'},index=['a1','a2','a3','b','thld','RR'])


IAM['Primer grado low']=iam1_low
IAM['Primer grado high']=iam1_high
IAM['Segundo grado']=iam2
IAM['Tercer grado']=iam3
IAM['ashrae']=iam_ashrae
IAM['physical']=iam_physical
IAM['martin_ruiz']=iam_physical





IAM.to_csv("C://Users/juanj/OneDrive/Escritorio/TFG/IAM.csv")








