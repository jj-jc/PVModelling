# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 11:03:31 2020

@author: juanj
"""


import plotly.io as pio
import plotly.graph_objects as go





import plotly.express as px
import numpy as np

filt_df3=filt_df2
Incremento=1
Max_temp=math.ceil(filt_df3['T_Amb (°C)'].max())
Min_temp=math.floor(filt_df3['T_Amb (°C)'].min())

Temperaturas=[]
rep=[]
Datos=pd.DataFrame()



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
#
#fig=go.Figure()
#for i in range(int(len(Datos.columns)/2)-1):
#    fig.add_trace(go.Scatter(
#        y=Datos.iloc[:,2*i],
#        x=Datos.iloc[:,2*i+1],
#        mode='markers',
#        visible=True,
#        showlegend=True,
#        name=Datos.columns[2*i]
#        ))
##        marker=dict(color=self.color[acimut],colorscale=px.colors.sequential.matter,showscale=True)))
#            
#        
#
#
#
#fig.show()
