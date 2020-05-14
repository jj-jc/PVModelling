# -*- coding: utf-8 -*-


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import Error 
#import IAM_ashrae
#import IAM_pysical_bruto
#import IAM_Martin
import plotly.graph_objects as go
#AOILIMIt
AOILIMIT=55.0

df=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/Datos_filtrados_IIIV.csv',encoding='utf-8')

#Se recogen en numpy los vectores que se van a usar
x=df['aoi'].values
y=df['ISC_IIIV/DII (A m2/W)']
#primero hacemos un fitting de los datos y comparamos las diferentes funciones de regresion
IAM_ashrae,RR_ashrae,b_ashrae=Error.regresion_ashrae(x,y)
IAM_physical,RR_physical,n_physical,k_physical,l_physical=Error.regresion_physical(x,y)
IAM_martin_ruiz,RR,a_r=Error.regresion_martin_ruiz(x,y)






filt_df2=df

filt_df3=filt_df2[(filt_df2['aoi']<AOILIMIT)]


Incremento=1
Max_temp=math.ceil(filt_df3['T_Amb (°C)'].max())
Min_temp=math.floor(filt_df3['T_Amb (°C)'].min())
Temperaturas=[]
rep=[]
for i in range(Min_temp,Max_temp,Incremento):
    AUX=filt_df3[(filt_df3['T_Amb (°C)']>i)]
    AUX=AUX[((AUX['T_Amb (°C)'])<i+Incremento)]
    rep.append(AUX['T_Amb (°C)'].count())
    Temperaturas.append(i)
    Datos_irradiancia=AUX['ISC_IIIV/DII (A m2/W)']

    

fig = go.Figure(
    data=[go.Bar(
            x=Temperaturas,
            y=rep)],
    layout_title_text="A Figure Displayed with fig.show()"
    
)
fig.update_xaxes(title="Temperaturas (°C)")
fig.update_yaxes(title="Repeticiones")
fig.show()




#COn el siguiente código representamos los datos en fiferentes temperaturas, el incremento es de 1º
#el intervalo es desde el valor más pequeño aumentado en uno, es decir tempera 14 signififca desde el 14 al 15 sin incluir

Incremento=1
Max_temp=math.ceil(filt_df3['T_Amb (°C)'].max())
Min_temp=math.floor(filt_df3['T_Amb (°C)'].min())
fig=go.Figure()
for i in range(Min_temp,Max_temp,Incremento):
    AUX=filt_df3[(filt_df3['T_Amb (°C)']>=float(i))]
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

#A partir del histograma anterior y las formas de los datos, se decide trabajr con el tmp26.


filt_df4=filt_df3
filt_df4=filt_df4[(filt_df4['T_Amb (°C)']<27.0)]
filt_df4=filt_df4[(filt_df4['T_Amb (°C)']>=26.0)]

fig=plt.figure(figsize=(30,15))
plt.plot(filt_df4['aoi'],filt_df4['ISC_IIIV/DII (A m2/W)'],'o',markersize=4,label='Datos de 26ºC')


porcent_mediana=5

AUX=filt_df4[filt_df4['aoi']<=31]
Mediana=Error.mediana(AUX['ISC_IIIV/DII (A m2/W)'])
DEBAJO=AUX[AUX['ISC_IIIV/DII (A m2/W)']<Mediana*(1-porcent_mediana/100)]   
filt_df4=filt_df4.drop(DEBAJO.index[:],axis=0)
ENCIMA=AUX[AUX['ISC_IIIV/DII (A m2/W)']>Mediana*(1+porcent_mediana/100)]
filt_df4=filt_df4.drop(ENCIMA.index[:],axis=0)
plt.plot(filt_df4['aoi'],filt_df4['ISC_IIIV/DII (A m2/W)'],'o',markersize=4,label='Primer filtrado por debajo de 31º de aoi')

#filtrado un poco a huevo

limSup=filt_df4['aoi'].max()
limInf=30
Rango=limSup-limInf
n_intervalos=20
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
plt.plot(filt_df4['aoi'],filt_df4['ISC_IIIV/DII (A m2/W)'],'o',markersize=2,label='Segundo filtrado por encima de 31º de aoi')
plt.legend()


#este codigo es para comprobar con otras temperaturas, y para calcular 
#
#filt_df4=filt_df3
#filt_df4=filt_df4[(filt_df4['T_Amb (°C)']<28.0)]
#filt_df4=filt_df4[(filt_df4['T_Amb (°C)']>=27.0)]
#
#fig=plt.figure(figsize=(30,15))
#plt.plot(filt_df4['aoi'],filt_df4['ISC_IIIV/DII (A m2/W)'],'o',markersize=4,label='Datos de 26ºC')
#
#
#
#
Y_regre,RR,a_s,b=Error.regresion_polinomica(filt_df4['aoi'],filt_df4['ISC_IIIV/DII (A m2/W)'],2)
fig=plt.figure(figsize=(30,15))
plt.plot(filt_df4['aoi'],filt_df4['ISC_IIIV/DII (A m2/W)'],'o',markersize=4,label='Datos de 26ºC')

plt.plot(filt_df3['aoi'],Y_regre,'o',markersize=4,label='Datos de 26ºC')





a=np.arange(0,len(filt_df4.index))
filt_df5=filt_df4.set_index(a)
filt_df5.to_excel("C://Users/juanj/OneDrive/Escritorio/TFG/Datos_filtrados_IIIV_temp26.xls")







# #######CODIGO PARA LA SUPERFCIE#################################3

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


fig.show()


