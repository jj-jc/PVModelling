# -*- coding: utf-8 -*-


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import Error as E
import plotly.graph_objects as go

from mpl_toolkits.axes_grid1 import host_subplot
#Codigo para poder expresar las gráfcas en plotly
import plotly.io as pio
pio.renderers.default='browser'


#AOILIMIT
AOILIMIT=55.0

df=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/Datos_filtrados_IIIV.csv',encoding='utf-8')

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
fig.update_yaxes(title="Repeticiones")
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
fig.show()

####################################CODIGO PARA LA SUPERFCIE#################################
fig = go.Figure(data=[go.Scatter3d(
    x=df['aoi'],
    y=df['T_Amb (°C)'],
    z=df['ISC_IIIV/DII (A m2/W)'],
    mode='markers',
    marker=dict(
        size=1,
        color=df['ISC_IIIV/DII (A m2/W)'],                # set color to an array/list of desired values
        colorscale='Viridis',   # choose a colorscale
        opacity=0.8
    )
)])
fig.update_layout(scene = dict(
                    xaxis_title='Ángulo de incidencia (°)',
                    yaxis_title='Temperatura ambiente (°C)',
                    zaxis_title='ISC_IIIV/DII (A m2/W)'),
                    )
fig.show()




#%%
fig=plt.figure(figsize=(30,15))
Incremento=1
Max_temp=math.ceil(filt_df2['T_Amb (°C)'].max())
Min_temp=math.floor(filt_df2['T_Amb (°C)'].min())
fig=go.Figure()
for i in range(Min_temp,Max_temp,Incremento):
    AUX=filt_df2[(filt_df2['T_Amb (°C)']>=float(i))]
    AUX=AUX[((AUX['T_Amb (°C)'])<i+Incremento)]    
    x_aux=np.array(AUX['aoi'].values)
    y_aux=np.array(AUX['ISC_IIIV/DII (A m2/W)'].values)
    y_poli,RR_poli,a_s,b=E.regresion_polinomica(x_aux,y_aux,2)
    fig.add_trace(go.Scatter(
    y=y_poli,
    x=x_aux,
    mode='markers',
    visible=True,
    showlegend=True,
    name='Temperatura '+ str(i)
    ))
fig.show()
#%%  ##REPRESENTACION DE LA REGRESION DE TODAS LAS TEMPERAURAS
y_poli,RR_poli,a_s,b=E.regresion_polinomica(filt_x,filt_y,2)
plt.plot(x,y,'o',markersize=4,label='Datos')
plt.plot(filt_x,y_poli,'o',markersize=4,label='Regresion')
plt.title('Regresión polinómica')
plt.legend()

#%%
#Hay que tomar una decision, para ver qué tempetura o temperaturas escoger
#sumamos las probabilidades del intervalo escogido (de 19 a 27)
sumatorio=0
for i in range(6,15):
    sumatorio=sumatorio+prob[i]
Incremento=1
Max_temp=27.0
Min_temp=19.0

df_filt_temp=filt_df2[(filt_df2['T_Amb (°C)']>=Min_temp)]
df_filt_temp=df_filt_temp[((df_filt_temp['T_Amb (°C)'])<=Max_temp)] 


I_DII=np.array(filt_df2['ISC_IIIV/DII (A m2/W)'])
aoi=np.array(filt_df2['aoi'])
fig=plt.figure(figsize=(30,15))
y_poli,RR_poli,a_s,b=E.regresion_polinomica(aoi,I_DII,2)
plt.plot(aoi,I_DII,'o',markersize=4,label='Datos')
plt.plot(aoi,y_poli,'o',markersize=4,label='Regresion')
plt.title('Regresión polinómica')
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
Incremento=1
Max_temp=27.0
Min_temp=26.0

df_filt_temp=filt_df2[(filt_df2['T_Amb (°C)']>=Min_temp)]
df_filt_temp=df_filt_temp[((df_filt_temp['T_Amb (°C)'])<=Max_temp)] 


I_DII=np.array(filt_df2['ISC_IIIV/DII (A m2/W)'])
aoi=np.array(filt_df2['aoi'])
fig=plt.figure(figsize=(30,15))
y_poli,RR_poli,a_s,b=E.regresion_polinomica(aoi,I_DII,2)
plt.plot(aoi,I_DII,'o',markersize=4,label='Datos')
plt.plot(aoi,y_poli,'o',markersize=4,label='Regresion')
plt.title('Regresión polinómica')
plt.legend()  
print('Con el '+str(prob[13])+ ' de los datos')
print('Coeficiente de determinacion del ' +str(RR_poli))
print('Temperaturas entre '+ str(Min_temp) +' y '+str(Max_temp)+' °C')
Incremento=2
Max_temp=math.ceil(df_filt_temp['T_Amb (°C)'].max())*10
Min_temp=math.floor(df_filt_temp['T_Amb (°C)'].min())*10
fig=go.Figure()
for i in range(Min_temp,Max_temp,Incremento):
    AUX=df_filt_temp[(df_filt_temp['T_Amb (°C)']>=float(i/10))]
    AUX=AUX[((AUX['T_Amb (°C)'])<(i+Incremento)/10)]    

    fig.add_trace(go.Scatter(
    y=AUX['ISC_IIIV/DII (A m2/W)'],
    x=AUX['aoi'],
    mode='markers',
    visible=True,
    showlegend=True,
    name='Temperatura '+ str(i/10)
    ))
fig.show()
   
fig=go.Figure()
for i in range(Min_temp,Max_temp,Incremento):
    AUX=df_filt_temp[(df_filt_temp['T_Amb (°C)']>=float(i/10))]
    AUX=AUX[((AUX['T_Amb (°C)'])<(i+Incremento)/10)]    

    fig.add_trace(go.Scatter(
    y=AUX['SMR_Top_Mid (n.d.)'],
    x=AUX['aoi'],
    mode='markers',
    visible=True,
    showlegend=True,
    name='Temperatura '+ str(i/10)
    ))
fig.show()


#%%
#ESTDIAR LA POSIBILIDAD DE QUE DEPENDA DE SMR TAMBIEN, YA QUE EN LAS TEMPERATURAS HAY COMPORTAAMIENTOS QUE NO SE PUEDEN 
#EXPLICAR ÚNICAMENE POR LA TEMPERATURA


plt.figure(figsize=(30,20))
host = host_subplot(111)
par = host.twinx()
host.set_xlabel("Ángulo de incidencia (°)")
host.set_ylabel("Eficiencia de la captación de irradiancia del IIIV(A m2/W)")
par.set_ylabel("SMR")
p1, = host.plot(df_filt_temp['aoi'],df_filt_temp['ISC_IIIV/DII (A m2/W)'],'o',markersize=2,color='b',label='IIIV')
p2, = par.plot(df_filt_temp['aoi'],df_filt_temp['SMR_Top_Mid (n.d.)'],'o',markersize=2,color='g',label='SMR')
leg = plt.legend()
host.yaxis.get_label().set_color(p1.get_color())
leg.texts[0].set_color(p1.get_color())
par.yaxis.get_label().set_color(p2.get_color())
leg.texts[1].set_color(p2.get_color())
plt.show()








#POR AHORA ME QUEDO CON EL IAM OBTENIDO DEL INTERVALO DE 19 A 27 GRADOS
y_poli,RR_poli,a_s,b








