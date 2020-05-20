# -*- coding: utf-8 -*-



import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import Error as E
from cpvtopvlib import uf_preprocessing
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default='browser'
AOILIMIT=55.0

df=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/Datos_filtrados_IIIV.csv')

#%%Primero obtenemos el AM con la libreria de Marcos

x=df['airmass_relative'].values
y=df['ISC_IIIV/DII (A m2/W)'].values

#tenemes que localizar el limit 
fig=go.Figure()
fig.add_trace(go.Scatter(
    y=y,
    x=x,
    mode='markers',
    visible=True,
    showlegend=True
    ))
fig.update_xaxes(title="AM")
fig.update_yaxes(title="ISC/DII")
fig.show()

#Limite localizado 1.555 

m_low, n_low, m_high, n_high, thld=uf_preprocessing.calc_uf_lines(x,y, limit = 1.555)


#dividimos en partes 
filt_df=df[df['airmass_relative']<=1.555]
x1=filt_df['airmass_relative'].values
y1=filt_df['ISC_IIIV/DII (A m2/W)'].values

filt_df2=df[df['airmass_relative']>1.555]
x2=filt_df2['airmass_relative'].values
y2=filt_df2['ISC_IIIV/DII (A m2/W)'].values

#cálculos 
y1_regre=x1*m_low+n_low
y2_regre=x2*m_high+n_high
RR1=E.Determination_coefficient(y1, y1_regre)
RR2=E.Determination_coefficient(y2, y2_regre)
x12=np.concatenate((x1,x2))
y12=np.concatenate((y1,y2))
y12_regre=np.concatenate((y1_regre,y2_regre))
RR=E.Determination_coefficient(y12, y12_regre)


#se dibujan las regresiones
fig=plt.figure(figsize=(30,15))
plt.plot(x,y,'o',markersize=4,label='Datos')
plt.plot(x1,y1_regre,'o',markersize=4,label='Regresion parte1')
plt.plot(x2,y2_regre,'o',markersize=4,label='Regresion parte1')
plt.title('Regresión polinómica')
plt.legend()
fig=plt.figure(figsize=(30,15))
plt.plot(x,y,'o',markersize=4,label='Datos')
plt.plot(x12,y12_regre,'o',markersize=4,label='Regresion parte1')
plt.title('Regresión polinómica de grado 1')
plt.legend()
print(RR1)
print(RR2)
print(RR)


#%%AHORA SE HACE LO MISMO PERO CON UNA REGRESION POLINOMICA DE GRADO 2
filt_df=df[df['airmass_relative']<=1.555]
filt_x=filt_df['airmass_relative'].values
filt_y=filt_df['ISC_IIIV/DII (A m2/W)'].values

filt_df2=df[df['airmass_relative']>1.555]
filt2_x=filt_df2['airmass_relative'].values
filt2_y=filt_df2['ISC_IIIV/DII (A m2/W)'].values

#Cálculos

y1_regre,RR1,a_s1,b1=E.regresion_polinomica(filt_x,filt_y,2)
y2_regre,RR2,a_s2,b2=E.regresion_polinomica(filt2_x,filt2_y,2)
x12=np.concatenate((filt_x,filt2_x))
y12=np.concatenate((filt_y,filt2_y))
y12_regre=np.concatenate((y1_regre,y2_regre))
RR=E.Determination_coefficient(y12, y12_regre)

#se dibujan las regresiones
fig=plt.figure(figsize=(30,15))
plt.plot(x,y,'o',markersize=4,label='Datos')
plt.plot(x1,y1_regre,'o',markersize=4,label='Regresion parte1')
plt.plot(x2,y2_regre,'o',markersize=4,label='Regresion parte1')
plt.title('Regresión polinómica')
plt.legend()
fig=plt.figure(figsize=(30,15))
plt.plot(x,y,'o',markersize=4,label='Datos')
plt.plot(x12,y12_regre,'o',markersize=4,label='Regresion parte1')
plt.title('Regresión polinómica de grado 2')
plt.legend()
print(RR1)
print(RR2)
print(RR)



#%%AHORA SE HACE LO MISMO PERO CON UNA REGRESION POLINOMICA DE GRADO 3
filt_df=df[df['airmass_relative']<=1.555]
filt_x=filt_df['airmass_relative'].values
filt_y=filt_df['ISC_IIIV/DII (A m2/W)'].values

filt_df2=df[df['airmass_relative']>1.555]
filt2_x=filt_df2['airmass_relative'].values
filt2_y=filt_df2['ISC_IIIV/DII (A m2/W)'].values

#Cálculos

y1_regre,RR1,a_s1,b1=E.regresion_polinomica(filt_x,filt_y,3)
y2_regre,RR2,a_s2,b2=E.regresion_polinomica(filt2_x,filt2_y,3)
x12=np.concatenate((filt_x,filt2_x))
y12=np.concatenate((filt_y,filt2_y))
y12_regre=np.concatenate((y1_regre,y2_regre))
RR=E.Determination_coefficient(y12, y12_regre)

#se dibujan las regresiones
fig=plt.figure(figsize=(30,15))
plt.plot(x,y,'o',markersize=4,label='Datos')
plt.plot(x1,y1_regre,'o',markersize=4,label='Regresion parte1')
plt.plot(x2,y2_regre,'o',markersize=4,label='Regresion parte1')
plt.title('Regresión polinómica de grado 3')
plt.legend()
fig=plt.figure(figsize=(30,15))
plt.plot(x,y,'o',markersize=4,label='Datos')
plt.plot(x12,y12_regre,'o',markersize=4,label='Regresion parte1')
plt.title('Regresión polinómica')
plt.legend()
print(RR1)
print(RR2)
print(RR)

#%%AHORA SE ESTUDIA EN FUNCIÓN DE LA TEMPERATURA


filt_df=df
filt_x=filt_df['T_Amb (°C)'].values
filt_y=filt_df['ISC_IIIV/DII (A m2/W)'].values

y1_regre,RR1,a_s1,b1=E.regresion_polinomica(filt_x,filt_y,1)


fig=plt.figure(figsize=(30,15))
plt.plot(filt_x,filt_y,'o',markersize=4,label='Datos primera parte')
plt.plot(filt_x,y1_regre,'o',markersize=4,label='Regresion')
plt.title('Regresión polinómica')
plt.legend()
print(RR1)


#%%
#COMO ES MUY DISPERSO SE PIENSA EN DIVIR EN DOS RANGOS EN FUNCIÓN DEL AOILIMIT
filt_df=df[df['aoi']<=AOILIMIT]
filt_x=filt_df['T_Amb (°C)'].values
filt_y=filt_df['ISC_IIIV/DII (A m2/W)'].values

filt_df2=df[df['aoi']>AOILIMIT]
filt2_x=filt_df2['T_Amb (°C)'].values
filt2_y=filt_df2['ISC_IIIV/DII (A m2/W)'].values


y1_regre,RR1,a_s1,b1=E.regresion_polinomica(filt_x,filt_y,1)
y2_regre,RR2,a_s2,b2=E.regresion_polinomica(filt2_x,filt2_y,1)
x12=np.concatenate((filt_x,filt2_x))
y12=np.concatenate((filt_y,filt2_y))
y12_regre=np.concatenate((y1_regre,y2_regre))
RR=E.Determination_coefficient(y12, y12_regre)
fig=plt.figure(figsize=(30,15))
plt.plot(filt_x,filt_y,'o',markersize=4,label='Datos primera parte')
plt.plot(filt2_x,filt2_y,'o',markersize=4,label='Datos segunda parte')
plt.plot(x12,y12_regre,'o',markersize=4,label='Regresion parte1')
plt.title('Regresión polinómica')
plt.legend()
print(RR1)
print(RR2)
print(RR)





