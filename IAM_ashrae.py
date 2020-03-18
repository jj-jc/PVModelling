import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
import pvlib
import datetime as dt 
import Error as E

df=pd.read_excel('C://Users/juanj/OneDrive/Escritorio/TFG/Insolight_CPV_AOI_response.xlsx',encoding= 'unicode_escape')
# df=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/InsolightMay2019.csv',encoding= 'unicode_escape')
#recogemos los datos en un dataframe
df_CPV_AOI_response=pd.DataFrame(data=np.array(df.iloc[2:10,:],dtype='float64'), columns=np.array(df.iloc[1,:]))
Datos=df_CPV_AOI_response['UF (AOI) - Losses additional to cos(AOI) ']


#definimos la funcion que aproximan los resultados empíricos
def f1(x):
    return (-0.0003*(x**2) + 0.0027*(x) + 0.9893)
#Definimos las variables a usar
LON=100
IAM_ashrae=np.arange(LON*8).reshape(LON,8)
IAM_ashrae.dtype='float32'
b_val=float(1.1)
print(b_val)
b=np.arange(LON)
b.dtype='float32'
Error=np.arange(LON)
Error.dtype='float32'

#dibujamos las gráficas
plt.close('all')
x=df_CPV_AOI_response['Angle']
y1=df_CPV_AOI_response['UF (AOI) - Losses additional to cos(AOI) ']    
plt.figure(figsize=(10,7))
plt.plot(x,y1,'o',markersize=2,label='IAM_datos')
plt.plot(x,f1(x),'X',markersize=2,label='IAM_curva_datos')
for i in range(LON):
    b[i]=b_val
    print(b_val)
    IAM_ashrae[i]=np.array(pvlib.iam.ashrae(aoi=df_CPV_AOI_response['Angle'],b=b[i]))
    plt.plot(x,IAM_ashrae[i],'--',markersize=2,label='IAM_ashrae '+str(round(b_val,2)))
    Error[i]=E.ECM(y1,IAM_ashrae[i])
    b_val=b_val+float(0.001)

plt.legend()
plt.show()

Pos_b=np.where(Error==Error.min())
b_val=float(b[Pos_b])
print('El error es de: ',Error[Pos_b])
print('El valor de la b es: ',float(b[Pos_b]))
