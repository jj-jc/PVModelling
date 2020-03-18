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

x=df_CPV_AOI_response['Angle']
y1=df_CPV_AOI_response['UF (AOI) - Losses additional to cos(AOI) ']  
y2=f1(x)

#creamos las diferentes combinaciones de los tres parámetros 
LON=10
incremento=.1
#tenemos que poner el valor inicial
n_val=0.7
k_val=5.0
l_val=0.1

Combinaciones=pd.DataFrame(data=np.zeros(((LON**3)+1,4)), dtype='float32', columns=['n','k','l','E'])
Combinaciones.iloc[0][0]=n_val
Combinaciones.iloc[0][1]=k_val
Combinaciones.iloc[0][2]=l_val
i=0
j=0
p=0
for i in range(LON):#se ocupará de las centenas, en la base que se ponga de LON
    for j in range(LON):#se ocupará de las decenas
        for p in range(LON):#se ocupará de las unidades
            Combinaciones.iloc[p+LON*j+LON**2*i][3]=E.ECM(y1,np.array(pvlib.iam.physical(aoi=x, n=Combinaciones.iloc[p+LON*j+LON**2*i][0],K=Combinaciones.iloc[p+LON*j+LON**2*i][1], L=Combinaciones.iloc[p+LON*j+LON**2*i][2])))
            Combinaciones.iloc[p+LON*j+LON**2*i+1]=Combinaciones.iloc[p+LON*j+LON**2*i]
            Combinaciones.iloc[p+LON*j+LON**2*i+1][0]=Combinaciones.iloc[p+LON*j+LON**2*i][0]+incremento
        Combinaciones.iloc[p+LON*j+LON**2*i+1][0]=n_val
        Combinaciones.iloc[p+LON*j+LON**2*i+1][1]=Combinaciones.iloc[p+LON*j+LON**2*i][1]+incremento
    Combinaciones.iloc[p+LON*j+LON**2*i+1][0]=n_val
    Combinaciones.iloc[p+LON*j+LON**2*i+1][1]=k_val
    Combinaciones.iloc[p+LON*j+LON**2*i+1][2]=Combinaciones.iloc[p+LON*j+LON**2*i][2]+incremento
Combinaciones_sin_Nan=Combinaciones.dropna(how='any')

Valores=Combinaciones[Combinaciones['E']==Combinaciones[:]['E'].min()]
print('El valor de la n: ', float(Valores['n']))
print('El valor de la k: ', float(Valores['k']))
print('El valor de la l: ', float(Valores['l']))
print('El valor del error es: ', float(Valores['E']))
print('El error de la funcion aproximación es: ', E.ECM(y1,y2))
#Este es el rsultado de la ejecución con LON a 10
#El valor de la n:  0.9000000357627869
#El valor de la k:  5.399999618530273
#El valor de la l:  0.20000000298023224
#El valor del error es:  8.786098624113947e-05




#Este es el resultado de la ultima ejecucion con 100 de LON
# # El valor de la n:  0.9000000357627869
# El valor de la k:  10.900008201599121
# El valor de la l:  0.10000000149011612
# El valor del error es:  8.683190390001982e-05

plt.close('all')
y3=np.array(pvlib.iam.physical(aoi=x, n=float(Valores['n']),K=float(Valores['k']), L=float(Valores['l'])))
y4=np.array(pvlib.iam.physical(aoi=x, n=0.9000000357627869,K=10.900008201599121, L=0.10000000149011612))
plt.figure(figsize=(10,7))
plt.plot(x,y1,'o',markersize=2,label='Datos')
plt.plot(x,y2,'--',markersize=2,label='Aproximacion')
plt.plot(x,y3,'--',markersize=2,label='Calculados')
plt.plot(x,y4,'--',markersize=2,label='Calculados mejorados')
plt.legend()
plt.show()

















