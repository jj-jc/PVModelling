import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
import pvlib
import datetime as dt 
import Error as E

df=pd.read_excel('C://Users/juanj/OneDrive/Escritorio/TFG/Insolight_CPV_AOI_response.xlsx',encoding= 'unicode_escape')
# df=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/InsolightMay2019.csv',encoding= 'unicode_escape')
#recogemos los datos en un dataframe
df_CPV_AOI_response=pd.DataFrame(data=np.array(df.iloc[2:10,:],dtype='float32'), columns=np.array(df.iloc[1,:]))

#definimos la funcion que aproximan los resultados empíricos
def f1(x):
    return (-0.0003*(x**2) + 0.0027*(x) + 0.9893)
#Definimos las variables a usar
LON=5
IAM_Martin=np.arange(LON*8,dtype='float32').reshape(LON,8)
ar_val=float(1.1)
ar=np.arange(LON,dtype='float32')
R=np.arange(LON,dtype='float32')

#dibujamos las gráficas
plt.close('all')
x=df_CPV_AOI_response['Angle']
y1=df_CPV_AOI_response['UF (AOI) - Losses additional to cos(AOI) ']    
plt.figure(figsize=(10,7))
plt.plot(x,y1,'o',markersize=2,label='IAM_datos')
plt.plot(x,f1(x),'X',markersize=2,label='IAM_curva_datos')
for i in range(LON):
    ar[i]=ar_val
    IAM_Martin[i]=np.array(pvlib.iam.martin_ruiz(aoi=df_CPV_AOI_response['Angle'],a_r=ar[i]))
    plt.plot(x,IAM_Martin[i],'--',markersize=2,label='IAM_Martin '+str(round(ar_val,2)))
    Error[i]=E.ECM(y1,IAM_Martin[i])
    ar_val=ar_val+100
plt.legend()
plt.show()

Pos_ar=np.where(Error==Error.min())
ar_val=float(ar[Pos_ar])
print('El error es de: ',Error[Pos_ar])
print('El valor de la ar es: ',ar[Pos_ar])
#con este cógido vemos que hay un valor de ar al cual satura, y no se consigue que 
#aproxime más a la curva