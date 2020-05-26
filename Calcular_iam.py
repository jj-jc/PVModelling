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
Valor_normalizar=0.00096#Este valor es el valor que Marcos utiliza para normalizar 


df=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/Datos_filtrados_IIIV.csv',encoding='utf-8')


#%%Este es el código para calcular iam cuando AOI<AOILIMIT
#Se recogen en numpy los vectores que se van a usar
x=df['aoi']
y=df['ISC_IIIV/DII (A m2/W)'].values



filt_df2=df[(df['aoi']<AOILIMIT)]
filt_x=filt_df2['aoi']
filt_y=filt_df2['ISC_IIIV/DII (A m2/W)'].values



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

# fig.update_layout(scene = dict(
#                     xaxis_title='Ángulo de incidencia (°)',
#                     yaxis_title='Temperatura ambiente (°C)',
#                     zaxis_title='ISC_IIIV/DII (A m2/W)'),
#                     )





#%%Dibujo todas las regresiones por cada temperatura
# fig=plt.figure(figsize=(30,15))
# Incremento=1
# Max_temp=math.ceil(filt_df2['T_Amb (°C)'].max())
# Min_temp=math.floor(filt_df2['T_Amb (°C)'].min())
# fig=go.Figure()
# for i in range(Min_temp,Max_temp,Incremento):
#     AUX=filt_df2[(filt_df2['T_Amb (°C)']>=float(i))]
#     AUX=AUX[((AUX['T_Amb (°C)'])<i+Incremento)]    
#     x_aux=np.array(AUX['aoi'].values)
#     y_aux=np.array(AUX['ISC_IIIV/DII (A m2/W)'].values)
#     y_poli,RR_poli,a_s,b=E.regresion_polinomica(x_aux,y_aux,2)
#     fig.add_trace(go.Scatter(
#     y=y_poli,
#     x=x_aux,
#     mode='markers',
#     visible=True,
#     showlegend=True,
#     name='Temperatura '+ str(i)
#     ))
# fig.show()
#%%  ##REPRESENTACION DE LA REGRESION DE TODAS LAS TEMPERAURAS
y_poli,RR_poli,a_s,b=Error.regresion_polinomica(filt_x,filt_y,2)
fig=plt.figure(figsize=(30,15))
plt.plot(x,y,'o',markersize=4,label='Datos')
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
#sumamos las probabilidades del intervalo escogido (26)
# sumatorio=0
# for i in range(6):
#     sumatorio=sumatorio+prob[i]

Max_temp=28.0
Min_temp=26.0

df_filt_26=filt_df2[(filt_df2['T_Amb (°C)']>=Min_temp)]
df_filt_26=df_filt_26[((df_filt_26['T_Amb (°C)'])<=Max_temp)] 

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



Incremento=2
Max_temp=math.ceil(df_filt_26['T_Amb (°C)'].max())*10
Min_temp=math.floor(df_filt_26['T_Amb (°C)'].min())*10
fig=go.Figure()
for i in range(Min_temp,Max_temp,Incremento):
    AUX=df_filt_26[(df_filt_26['T_Amb (°C)']>=float(i/10))]
    AUX=AUX[((AUX['T_Amb (°C)'])<(i+Incremento)/10)]    

    fig.add_trace(go.Scatter(
    y=AUX['ISC_IIIV/DII (A m2/W)'],
    x=AUX['aoi'],
    mode='markers',
    visible=True,
    showlegend=True,
    name='Temperatura '+ str(i/10)
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
IAM2=obtención_dii_efectiva(datos)
fig=plt.figure(figsize=(30,15))
plt.plot(datos,IAM,'o',markersize=4,label='Datos')
plt.plot(datos,IAM2,'o',markersize=4,label='Datos')
plt.xlabel('Ángulo de incidencia (°)')
plt.ylabel('ISC_IIIV/DII (A m2/W)')
plt.title('Regresión polinómica para 26 °C' )
plt.legend()  
 
 
#%%
df_filt_26.to_csv("C://Users/juanj/OneDrive/Escritorio/TFG/IIIV.csv",encoding='utf-8')







# fig=go.Figure()
# for i in range(Min_temp,Max_temp,Incremento):
#     AUX=df_filt_26[(df_filt_26['T_Amb (°C)']>=float(i/10))]
#     AUX=AUX[((AUX['T_Amb (°C)'])<(i+Incremento)/10)]    

#     fig.add_trace(go.Scatter(
#     y=AUX['SMR_Top_Mid (n.d.)'],
#     x=AUX['aoi'],
#     mode='markers',
#     visible=True,
#     showlegend=True,
#     name='Temperatura '+ str(i/10)
#     ))
# fig.update_layout(
#     title="SMR_Top_Mid en función del ángulo de incidencia para la temperatura de 26°C",
#     xaxis_title="Ángulo de incidencia (°)",
#     yaxis_title="SMR_Top_Mid (n.d.)",
# )
# fig.show()


#%%
#ESTDIAR LA POSIBILIDAD DE QUE DEPENDA DE SMR TAMBIEN, YA QUE EN LAS TEMPERATURAS HAY COMPORTAMIENTOS QUE NO SE PUEDEN 
#EXPLICAR ÚNICAMENE POR LA TEMPERATURA


# plt.figure(figsize=(30,20))
# host = host_subplot(111)
# par = host.twinx()
# host.set_xlabel("Ángulo de incidencia (°)")
# host.set_ylabel("Eficiencia de la captación de irradiancia del IIIV(A m2/W)")
# par.set_ylabel("SMR")
# p1, = host.plot(df_filt_temp['aoi'],df_filt_temp['ISC_IIIV/DII (A m2/W)'],'o',markersize=4,color='b',label='IIIV')
# p2, = par.plot(df_filt_temp['aoi'],df_filt_temp['SMR_Top_Mid (n.d.)'],'o',markersize=4,color='g',label='SMR')
# leg = plt.legend()
# host.yaxis.get_label().set_color(p1.get_color())
# leg.texts[0].set_color(p1.get_color())
# par.yaxis.get_label().set_color(p2.get_color())
# leg.texts[1].set_color(p2.get_color())
# plt.title('Comparacion de ISC con SMR para buscar explicación a datos extraños')
# plt.show()


# fig=plt.figure(figsize=(30,15))
# plt.plot(df_filt_temp['aoi'],df_filt_temp['DII (W/m2)'],'o',markersize=4,color='b',label='DII')
# plt.xlabel('Ángulo de incidencia (°)')
# plt.ylabel('DII (W/m2)')
# plt.title('DII')
# plt.legend()  

# fig=plt.figure(figsize=(30,15))
# plt.plot(df_filt_temp['aoi'],df_filt_temp['ISC_measured_IIIV (A)'],'o',markersize=4,color='b',label='ISC de todos los datos')
# plt.plot(df_filt_26['aoi'],df_filt_26['ISC_measured_IIIV (A)'],'o',markersize=4,color='g',label='ISC para la temperatura de 26 °C ')
# plt.xlabel('Ángulo de incidencia (°)')
# plt.ylabel('DII (W/m2)')
# plt.title('ISC_IIIV_medida')
# plt.legend()  



# fig=plt.figure(figsize=(30,15))
# plt.plot(df_filt_temp['aoi'],df_filt_temp['DNI_Mid (W/m2)'],'o',markersize=4,color='b',label='DNI_mid')
# plt.xlabel('Ángulo de incidencia (°)')
# plt.ylabel('DNI_Mid (W/m2)')
# plt.title('DNI_Mid (W/m2)')
# plt.legend()  


# fig=plt.figure(figsize=(30,15))
# plt.plot(df_filt_temp['aoi'],df_filt_temp['DNI_Top (W/m2)'],'o',markersize=4,color='b',label='DNI_mid')
# plt.xlabel('Ángulo de incidencia (°)')
# plt.ylabel('DNI_Top (W/m2)')
# plt.title('DNI_Top (W/m2)')
# plt.legend()  






#%%
#POR AHORA ME QUEDO CON EL IAM OBTENIDO DEL INTERVALO DE 19 A 27 GRADOS


# I_DII=np.array(df_filt_temp['ISC_IIIV/DII (A m2/W)'])
# aoi=np.array(df_filt_temp['aoi'])

# y_poli,RR_poli,a_s,b=E.regresion_polinomica(aoi,I_DII,2)
# #tengo que decidir un valor para normalizar
# # Valor_normalizar=y_poli.max()
# Valor_normalizar=0.00096
# IAM=y_poli/Valor_normalizar
# # fig=plt.figure(figsize=(30,15))
# # plt.plot(aoi,IAM, 'o',markersize=4,color='b',label='IAM')
# # plt.title('Regresión polinómica')
# # plt.legend()

#%%CÓDIGO PARA OBTENCION DE IAM CUANDO AOI>AOILIMIT


# filt_AOILIMIT=df[(df['aoi']>AOILIMIT)]

# x_AOILIMIT=filt_AOILIMIT['aoi']
# y_AOILIMIT=filt_AOILIMIT['ISC_IIIV/DII (A m2/W)'].values

# # Incremento=1
# # Max_temp=math.ceil(filt_AOILIMIT['T_Amb (°C)'].max())
# # Min_temp=math.floor(filt_AOILIMIT['T_Amb (°C)'].min())
# # Temperaturas=[]
# # rep=[]
# # for i in range(Min_temp,Max_temp,Incremento):
# #     AUX=filt_AOILIMIT[(filt_AOILIMIT['T_Amb (°C)']>i)]
# #     AUX=AUX[((AUX['T_Amb (°C)'])<i+Incremento)]
# #     rep.append(AUX['T_Amb (°C)'].count())
# #     Temperaturas.append(i)


# # rep=np.array(rep)
# # prob=rep/rep.sum()

# # fig = go.Figure(
# #     data=[go.Bar(
# #             x=Temperaturas,
# #             y=prob)],
# #     layout_title_text="Histograma con la probabilidad de cada temperatura"
    
# # )
# # fig.update_xaxes(title="Temperaturas (°C)")
# # fig.update_yaxes(title="Repeticiones")
# # fig.show()


# # #COn el siguiente código representamos los datos en fiferentes temperaturas, el incremento es de 1º
# # #el intervalo es desde el valor más pequeño aumentado en uno, es decir tempera 14 signififca desde el 14 al 15 sin incluir

# # Incremento=1
# # Max_temp=math.ceil(filt_AOILIMIT['T_Amb (°C)'].max())
# # Min_temp=math.floor(filt_AOILIMIT['T_Amb (°C)'].min())
# # fig=go.Figure()
# # for i in range(Min_temp,Max_temp,Incremento):
# #     AUX=filt_AOILIMIT[(filt_AOILIMIT['T_Amb (°C)']>=float(i))]
# #     AUX=AUX[((AUX['T_Amb (°C)'])<i+Incremento)]    

# #     fig.add_trace(go.Scatter(
# #     y=AUX['ISC_IIIV/DII (A m2/W)'],
# #     x=AUX['aoi'],
# #     mode='markers',
# #     visible=True,
# #     showlegend=True,
# #     name='Temperatura '+ str(i)
# #     ))
# # fig.show()



# Max_temp=27.0
# Min_temp=19.0
# filt_AOILIMIT=filt_AOILIMIT[(filt_AOILIMIT['T_Amb (°C)']>=Min_temp)]
# filt_AOILIMIT=filt_AOILIMIT[((filt_AOILIMIT['T_Amb (°C)'])<=Max_temp)] 


# I_DII=np.array(filt_AOILIMIT['ISC_IIIV/DII (A m2/W)'])
# aoi=np.array(filt_AOILIMIT['aoi'])
# fig=plt.figure(figsize=(30,15))
# y_poli,RR_poli,a_s,b=E.regresion_polinomica(aoi,I_DII,2)
# plt.plot(aoi,I_DII,'o',markersize=4,label='Datos')
# plt.plot(aoi,y_poli,'o',markersize=4,label='Regresion')
# plt.xlabel('Ángulo de incidencia (°)')
# plt.ylabel('ISC_IIIV/DII (W/m2)')
# plt.title('Regresión polinómica')
# plt.legend()  
# # print('Con el '+str(sumatorio)+ 'de los datos')
# print(RR_poli)
# print('Temperaturas entre '+ str(Min_temp) +' y '+str(Max_temp)+' °C')
    

# Valor_normalizar=0.00096
# IAM=y_poli/Valor_normalizar
# fig=plt.figure(figsize=(30,15))
# plt.plot(aoi,IAM, 'o',markersize=4,color='b',label='IAM')
# plt.title('Regresión polinómica')
# plt.legend()







