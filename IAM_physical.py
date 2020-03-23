import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
import pvlib
import Error as E
from funciones_excel import f1

df=pd.read_excel('C://Users/juanj/OneDrive/Escritorio/TFG/Insolight_CPV_AOI_response.xlsx',encoding= 'unicode_escape')
# df=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/InsolightMay2019.csv',encoding= 'unicode_escape')
#recogemos los datos en un dataframe
df_CPV_AOI_response=pd.DataFrame(data=np.array(df.iloc[2:10,:],dtype='float64'), columns=np.array(df.iloc[1,:]))
Datos=df_CPV_AOI_response['UF (AOI) - Losses additional to cos(AOI) ']
print(f1(3))
''' Código para el physical'''
'''              
# probamos con physical

#varieblaes a usar      (Tener en cuenta que el 8 vine por el numero de datos que tenemos)
LON=10                   
IAM_physical=np.arange(LON*8).reshape(LON,8)
IAM_physical.dtype='float32'
n=np.arange(LON)
n.dtype='float32'
n_val=0.800
k=np.arange(LON)
k.dtype='float32'
k_val=5.000
l=np.arange(LON)
l.dtype='float32'
l_val=0.200
# l_val.dtype='float32'
Error=np.arange(LON)
Error.dtype='float32'

#dibujamos la funcion 

plt.close('all')
x=df_CPV_AOI_response['Angle']
y1=df_CPV_AOI_response['UF (AOI) - Losses additional to cos(AOI) ']    
plt.figure(figsize=(10,7))
plt.plot(x,y1,'o',markersize=2,label='IAM_datos')
plt.plot(x,f1(x),'X',markersize=2,label='IAM_curva_datos')
for i in range(LON):
    n[i]=n_val
    IAM_physical[i]=np.array(pvlib.iam.physical(aoi=df_CPV_AOI_response['Angle'], n=n[i], K=k_val, L=l_val))
    plt.plot(x,IAM_physical[i],'--',markersize=2,label='IAM_physical '+str(round(n_val,2)))
    Error[i]=E.SS_res(y1,IAM_physical[i])
    n_val=n_val+1/LON

plt.legend()
plt.show()

Pos_n=np.where(Error==Error.min())
n_val=float(n[Pos_n])
print('El error es de: ',Error[Pos_n])
print('El valor de la n es: ',float(n[Pos_n]))
plt.figure(figsize=(10,7))
plt.plot(x,y1,'o',markersize=2,label='IAM_datos')
plt.plot(x,f1(x),'X',markersize=2,label='IAM_curva_datos')
for i in range(LON):
    k[i]=k_val
    IAM_physical[i]=np.array(pvlib.iam.physical(aoi=df_CPV_AOI_response['Angle'], n=n_val, K=k[i], L=l_val))
    plt.plot(x,IAM_physical[i],'--',markersize=2,label='IAM_physical con k='+str(round(k_val,2)))
    Error[i]=E.SS_res(y1,IAM_physical[i])
    k_val=k_val+1/LON
plt.legend()
plt.show()
Pos_k=np.where(Error==Error.min())
k_val=float(k[Pos_k])
print('El error es de: ',Error[Pos_k])
print('El valor de la k es: ',k[Pos_k])

plt.figure(figsize=(10,7))
plt.plot(x,y1,'o',markersize=2,label='IAM_datos')
plt.plot(x,f1(x),'X',markersize=2,label='IAM_curva_datos')
for i in range(LON):
    l[i]=l_val
    IAM_physical[i]=np.array(pvlib.iam.physical(aoi=df_CPV_AOI_response['Angle'], n=n_val, K=k_val, L=l[i]))
    plt.plot(x,IAM_physical[i],'--',markersize=2,label='IAM_physical con k='+str(round(l_val,2)))
    Error[i]=E.SS_res(y1,IAM_physical[i])
    l_val=l_val+1/LON
plt.legend()
plt.show()
Pos_l=np.where(Error==Error.min())
l_val=float(l[Pos_l])
print('El error es de: ',Error[Pos_l])
print('El valor de la l es: ',l[Pos_l])
print('valor de n: ',float(n_val))
print('valor de k: ',float(k_val))
print('valor de l: ',float(l_val))


#print(E.SS_res(y1,np.array(pvlib.iam.physical(aoi=df_CPV_AOI_response['Angle'], n=0.9, K=5.4, L=0.2))))


                #-------------OTRO CÓDIGO-------------------
