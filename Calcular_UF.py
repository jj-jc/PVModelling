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

#CREO UN PANDAS PARA RECOGER LOS RESULTADOS QUE VAYA OBTENIENDO
# Max_temp=27.0
# Min_temp=19.0
# df=df[(df['T_Amb (°C)']>=Min_temp)]
# df=df[((df['T_Amb (°C)'])<=Max_temp)] 


UF=pd.DataFrame(columns=['temp','UF_temp','UF_am','UF_am_2'])



#%%AHORA SE ESTUDIA EN FUNCIÓN DE LA TEMPERATURA


# filt_df=df
# filt_x=filt_df['T_Amb (°C)'].values
# filt_y=filt_df['ISC_IIIV/DII (A m2/W)'].values

# y1_regre,RR1,a_s1,b1=E.regresion_polinomica(filt_x,filt_y,1)


# fig=plt.figure(figsize=(30,15))
# plt.plot(filt_x,filt_y,'o',markersize=4,label='Datos primera parte')
# plt.plot(filt_x,y1_regre,'o',markersize=4,label='Regresion')
# plt.title('Regresión polinómica')
# plt.legend()
# print(RR1)


#%%Cálculo del UF_temp
#SE DIVIDE LA TEMPERATURA EN LOS DOS INTERVALOS < Y > QUE AOILIMIT
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
plt.plot(filt_x,filt_y,'o',markersize=4,label='Datos por debajo de AOILIMIT')
plt.plot(filt2_x,filt2_y,'o',markersize=4,label='Datos por encima de AOILIMIT')
plt.plot(x12,y12_regre,'o',markersize=4,label='Líneas de regresión')
plt.xlabel('Temperatura ambiente (°C) ')
plt.ylabel('ISC_IIIV/DII (A m2/W)')
plt.title('Cálculo del UF para la temperatura')
plt.legend()
# print(RR1)
# print(RR2)
print('El coeficiente de determinación para los datos por debajo de AOILIMIT es de: '+str(RR1))

#OBTENCIÓN DEL SIMPLE UF CAUNDO AOI<AOILIMIT
Valor_normalizar=0.00096

thld=filt_x[np.where(y1_regre==y1_regre.max())]

simple_uf= 1 + (filt_x - thld) * (a_s1[1])/Valor_normalizar

fig=plt.figure(figsize=(30,15))
plt.plot(filt_x,simple_uf,'o',markersize=4,label='Datos primera parte')

UF_temp=simple_uf

#OBTENCIÓN DEL SIMPLE UF CAUNDO AOI>AOILIMIT en este estado hay que coger otro valor para normalizar
# Valor_normalizar=0.0012678049960699205

# thld=filt_x[np.where(y1_regre==y1_regre.max())]

# simple_uf= 1 + (filt_x - thld) * (a_s1[1])/Valor_normalizar

# fig=plt.figure(figsize=(30,15))
# plt.plot(filt_x,simple_uf,'o',markersize=4,label='Datos primera parte')




#%%Cálculo del UF_am 
filt_df=df[df['aoi']<=AOILIMIT]
filt_x=filt_df['airmass_relative'].values
filt_y=filt_df['ISC_IIIV/DII (A m2/W)'].values

filt_df2=df[df['aoi']>AOILIMIT]
filt2_x=filt_df2['airmass_relative'].values
filt2_y=filt_df2['ISC_IIIV/DII (A m2/W)'].values


##ESTE PROGRAMA ES PARA AVERIGUAR CUAL ES EL MEJOR THLDS
#Se obtiene un RR=0.8540025403043598 y un thld=1.2425999999999844
# aux=np.arange(1.1,1.3,0.0001) 
# thdl=0
# RR_max=0
# for i in aux:
#     filt_df_low=filt_df[filt_df['airmass_relative']<=i]
#     filt_df_high=filt_df[filt_df['airmass_relative']>i]

#     x_low=filt_df_low['airmass_relative'].values
#     y_low=filt_df_low['ISC_IIIV/DII (A m2/W)'].values
#     yr_low, RR_low, a_s_low, b_low=E.regresion_polinomica(x_low, y_low, 1)
    
#     x_high=filt_df_high['airmass_relative'].values
#     y_high=filt_df_high['ISC_IIIV/DII (A m2/W)'].values
#     yr_high, RR_high, a_s_high, b_high=E.regresion_polinomica(x_high, y_high, 1)
    

#     y_datos=filt_df['ISC_IIIV/DII (A m2/W)'].values
#     y=np.concatenate((y_low,y_high))
#     yr=np.concatenate((yr_low,yr_high))
#     xr=np.concatenate((x_low,x_high))
#     RR=E.Determination_coefficient(y,yr)   
#     if RR_max < RR:
#         RR_max=RR
#         thld=i

filt_df_low=filt_df[filt_df['airmass_relative']<=1.2425999999999844]
filt_df_high=filt_df[filt_df['airmass_relative']>1.2425999999999844]

x_low=filt_df_low['airmass_relative'].values
y_low=filt_df_low['ISC_IIIV/DII (A m2/W)'].values
yr_low, RR_low, a_s_low, b_low=E.regresion_polinomica(x_low, y_low, 1)

x_high=filt_df_high['airmass_relative'].values
y_high=filt_df_high['ISC_IIIV/DII (A m2/W)'].values
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
Valor_normalizar=0.00096
thld=1.2425999999999844

thld_low=filt_x.min()

y_low_min=float(1 + (x_low[np.where(yr_low==yr_low.min())] - thld_low) * (a_s_low[1])/Valor_normalizar)


simple_uf=[]
for i in filt_df['airmass_relative'].values:
    if i < thld:
        simple_uf.append(float(1 + (i - thld_low) * (a_s_low[1])/Valor_normalizar))


    else:
        simple_uf.append(float(y_low_min + ((i - thld) * a_s_high[1])/Valor_normalizar))
        

fig=plt.figure(figsize=(30,15))
plt.plot(filt_x,simple_uf,'o',markersize=4,label='Datos primera parte')



UF_am=simple_uf
# fig=plt.figure(figsize=(30,15))
# plt.plot(x_low,simple_uf_low,'o',markersize=4,label='Datos primera parte')
# plt.plot(x_high,simple_uf_high,'o',markersize=4,label='Datos primera parte')


# UF_am=np.concatenate((simple_uf_low,simple_uf_high))
# x_am=np.concatenate((x_low,x_high))






#%%Compruebo con un segundo grado
x=filt_df['airmass_relative'].values
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
Valor_normalizar=0.00096
UF_am_2=yr/Valor_normalizar
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

#%%Recojo los UF obtenidos y los guardo en un archivo csv



UF['UF_temp']=UF_temp
UF['temp']=filt_df['T_Amb (°C)'].values
UF['UF_am']=UF_am
UF['UF_am_2']=UF_am_2_retocado
UF.to_csv('C://Users/juanj/OneDrive/Escritorio/TFG/UF.csv', index=False)







