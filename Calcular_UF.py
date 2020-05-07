# -*- coding: utf-8 -*-





from cpvtopvlib import uf_preprocessing



import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/Datos_filtrados_IIIV.csv')



#------------------------------------------Se trata de obtener los valores de los factores de utilizacion
#cogemos los datos y ponemos los nombres necesarios para que la librería de Marcos funcione

d = {'Isc/DNI': df['ISC_IIIV/DII (A m2/W)'].values, 'relative_airmass': df['airmass_relative'].values,'temp': df['T_Amb (°C)'].values}
Datos=pd.DataFrame(d)


#comprobanos que no haya ningún nan y que todos los valores sean finitos
np.any(np.isnan(Datos))
np.all(np.isfinite(Datos))
plt.figure(figsize=(30,15))
plt.plot( df['airmass_relative'],df['ISC_IIIV/DII (A m2/W)'],'o')


n,m,rmds=cpvtopvlib.uf_preprocessing.calc_regression_line(df['airmass_relative'],df['ISC_IIIV/DII (A m2/W)'])


#uf_preprocessing.calc_uf_lines(df['aoi'], df['T_Amb (°C)'], datatype = 'temp_air', limit = 200)


x=df['aoi']
x=x.values.reshape([x.values.shape[0],1])
y=df['ISC_IIIV/DII (A m2/W)']
y=y.values.reshape([y.values.shape[0],1])
uf_preprocessing.calc_uf_lines(x, y)
#
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
