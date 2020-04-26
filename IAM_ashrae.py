import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
import pvlib
import datetime as dt 
import Error as E

#df=pd.read_excel('C://Users/juanj/OneDrive/Escritorio/TFG/Insolight_CPV_AOI_response.xlsx',encoding= 'unicode_escape')
## df=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/InsolightMay2019.csv',encoding= 'unicode_escape')
##recogemos los datos en un dataframe
#df_CPV_AOI_response=pd.DataFrame(data=np.array(df.iloc[2:10,:],dtype='float32'), columns=np.array(df.iloc[1,:]))
#
##definimos la funcion que aproximan los resultados empíricos
#def f1(x):
#    return (-0.0003*(x**2) + 0.0027*(x) + 0.9893)
##Definimos las variables a usar
#LON=10
#IAM_ashrae=np.arange(LON*8,dtype='float32').reshape(LON,8)
#b_val=float(1)
#b=np.arange(LON,dtype='float32')
#R=np.arange(LON,dtype='float32')
#Er=np.arange(LON,dtype='float32')
##dibujamos las gráficas
#plt.close('all')
#x=df_CPV_AOI_response['Angle']
#y1=df_CPV_AOI_response['UF (AOI) - Losses additional to cos(AOI) ']    
#plt.figure(figsize=(20,15))
#plt.plot(x,y1,'o',markersize=2,label='IAM_datos')
#plt.plot(x,f1(x),'X',markersize=2,label='IAM_curva_datos')
#for i in range(LON):
#    b[i]=b_val
#    IAM_ashrae[i]=np.array(pvlib.iam.ashrae(aoi=df_CPV_AOI_response['Angle'],b=b[i]))
#    plt.plot(x,IAM_ashrae[i],'--',markersize=2,label='IAM_ashrae '+str(round(b_val,2)))
#    R[i]=E.Determination_coefficient(y1,IAM_ashrae[i])
#    Er[i]=E.SS_res(y1,IAM_ashrae[i])
#    b_val=b_val+float(0.001)
#plt.legend()
#plt.show()
#print('El valor de b ha ido desde: '+str(b[0])+ ' al ' + str(b[i]))
#
#Pos_b=np.where(R==R.max())[0][0]##Esto se hace para que pase únicamente el indice únicamente
#b_val=float(b[Pos_b])
#print('Del coeficiente de determinación es de: ',R[Pos_b])
#print('El valor de la b es: ',float(b[Pos_b]))
#Pos_Er=np.where(Er==Er.min())[0][0]
#b_val=float(b[Pos_Er])
#print('Del sumatorio de residuos es de: ',Er[Pos_Er])
#print('El valor de la b es: ',float(b[Pos_Er]))




def regresion_ashrae(aoi,datos):
    b=0.0
    RR=0.0
    for i in range(1000):     
        IAM_ashrae=pvlib.iam.ashrae(aoi=aoi,b=b)
        RR_nuevo=E.Determination_coefficient(datos,IAM_ashrae)
        if(abs(RR_nuevo)<RR):#como es una aproximacion lineal, en el momento que el que el RR se reduce significa que se esta se aleja del fitting por ello hay que dejar de iterar.
            break 
        else:
            RR=RR_nuevo
            b=b+0.01
    return RR,b



#La mejor b encontrada es de : 1.1779999732971191







