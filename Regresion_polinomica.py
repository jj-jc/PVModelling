# -*- coding: utf-8 -*-


import pandas as pd
from cpvtopvlib import uf_preprocessing
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import matplotlib.pyplot as plt
import Error as E
#cargamos los datos en un dataframe y recogemos las comlumnas que nos interesan en numpy.arrays

    
df=pd.read_excel('C://Users/juanj/OneDrive/Escritorio/TFG/Datos_filtrados_IIIV_temp26.xls',encoding='utf-8')
df=df.drop(['Unnamed: 0'],axis=1)
df['IAM_aoi_']=(df['ISC_IIIV/DII (A m2/W)'])/(df['ISC_IIIV/DII (A m2/W)'].max())
X=df['aoi']
Y=df['IAM_aoi_']


Y_pred,coef,interp=E.regresion_polinomica(X,Y,3)




plt.figure(figsize=(20,15))
plt.plot(X, Y_pred,'o')
plt.plot(X,Y,'o')

print(E.Determination_coefficient(Y,Y_pred))


