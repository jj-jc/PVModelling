# -*- coding: utf-8 -*-



import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from cpvtopvlib import uf_preprocessing





df=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/Datos_filtrados_IIIV.csv')



#------------------------------------------Se trata de obtener los valores de los factores de utilizacion
#cogemos los datos y ponemos los nombres necesarios para que la librería de Marcos funcione
#
#d = {'Isc/DNI': df['ISC_IIIV/DII (A m2/W)'].values, 'relative_airmass': df['airmass_relative'].values,'temp': df['T_Amb (°C)'].values}
#Datos=pd.DataFrame(d)

#
##comprobanos que no haya ningún nan y que todos los valores sean finitos
#np.any(np.isnan(Datos))
#np.all(np.isfinite(Datos))
#df2= df.sort_values('airmass_relative')
#for i in range(len(df.index[:])):
#    df2[]
#    

#df=df[df['airmass_relative']<1.50]
x=df['airmass_relative'] 
y=df['ISC_IIIV/DII (A m2/W)'] 

#tenemes que localizar el limit
#am

m_low, n_low, m_high, n_high, thld=uf_preprocessing.calc_uf_lines(x,y, limit = 1.4)
y1=m_low*x+n_low
y2=m_high*x+n_high
#y_regresion1=m_low*x+n_low

plt.figure(figsize=(10,10))
plt.plot( x,y,'o')
plt.plot( x,y1,'o')
plt.plot( x,y2,'o')


#uf_preprocessing.calc_uf_lines(df['aoi'], df['T_Amb (°C)'], datatype = 'temp_air', limit = 200)
#
#
#x=df['aoi']
#x=x.values.reshape([x.values.shape[0],1])
#y=df['ISC_IIIV/DII (A m2/W)']
#y=y.values.reshape([y.values.shape[0],1])
#uf_preprocessing.calc_uf_lines(x, y)
##
#x=df['aoi']
#x=x.values.reshape([x.values.shape[0],1])#ponemos los vectorees en columnas
#y=df['ISC_IIIV/DII (A m2/W)']
#y=y.values.reshape([y.values.shape[0],1])#ponemos los vectorees en columnas
#
#m_low, n_low, m_high, n_high, thld=uf_preprocessing.calc_uf_lines(x,y,limit=60)
#
#
#calc_two_regression_lines(df['aoi'].values, y, limit = 50)
#
#
#
#uf_preprocessing.calculate_UF(Datos)
