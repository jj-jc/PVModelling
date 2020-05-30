

import numpy as np#para trabajas con vectores mucho más rapido
import pvlib
import pandas as pd
#estos son los modulos necesarios para el fiting polinomial
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import math


def promedio(datos):
    sumatoria = sum(datos)
    longitud = float(len(datos))
    resultado = sumatoria / longitud
    return float(resultado)
    
def moda(datos):
    repeticiones = 0
    for i in datos:
        n = datos.count(i)
        if n > repeticiones:
            repeticiones = n

    moda = [] 

    for i in datos:
        n = datos.count(i) 
        if n == repeticiones and i not in moda:
            moda.append(i)

    if len(moda) != len(datos):
        return moda
    else:
        print ('No hay moda')

def mediana(datos):
    datos=np.array(datos)
    datos.sort() # Ordena los datos de la lista
    if len(datos)==0:
        mediana=0

    elif len(datos) % 2 == 0:
        n = len(datos)
        mediana = (datos[int(n / 2 - 1)] + datos[int(n / 2)]) / 2
    else:
        mediana = datos[int(len(datos)/ 2)]

    return mediana

def SS_res(datos,estimaciones):#residuos
    sumatorio=0
    for i in range(len(datos)):
        sumatorio=sumatorio+(datos[i]-estimaciones[i])**2
    return float(sumatorio)

def SS_tot(datos):#varianza de los datos
    num_datos=len(datos)
    sumatorio=sum(datos)
    media=sumatorio/num_datos
    sumatorio=0
    for i in range(num_datos):
        sumatorio=sumatorio+((datos[i]-media)**2)
    return float(sumatorio)

def SS_reg(datos,estimaciones):#Varianza de los datos estimados
    num_datos=len(datos)
    sumatorio=sum(datos)
    media=sumatorio/num_datos
    sumatorio=0
    for i in range(num_datos):
        sumatorio=sumatorio+(estimaciones[i]-media)**2
    return float(sumatorio)
def Determination_coefficient(datos,estimaciones):
    try:
        return 1-(SS_res(datos,estimaciones)/SS_tot(datos))
    except ZeroDivisionError:
        print('No se puede realizar una division por cero')
        return 1
def RMSE(datos, estimaciones):
    Error_cuadrado=(datos-estimaciones)**2
    rmse=math.sqrt((sum(Error_cuadrado))/len(datos))
    return rmse
    
    
def crear_estimaciones(a_s,b,x):
#como el vector que devuelve la recta de regresión es siempre [0, a1,a2...]
#eesta funcion no sirve para la de marcos
    if (np.count_nonzero(a_s)==1):
        y_estimados=a_s[1]*x+b
    elif (np.count_nonzero(a_s)==2):
        y_estimados=a_s[2]*x**2+a_s[1]*x+b
    return y_estimados

    
    
    
#############################################Regresiones
def regresion_lineal(x,y):
    # coeficientes de regresion
    # y =beta0+beta1*x
#    if isinstance(x,np.ndarray):
#        x=np.array(x)
#    if isinstance(y,np.ndarray):
#        x=np.array(y)
    Mediax=promedio(x)
    Mediay=promedio(y)
    sumatorio=0
    for i in range(len(x)):
        sumatorio=sumatorio+((x[i]-Mediax)*(y[i]-Mediay))
    beta1=sumatorio/SS_tot(x)
    beta0=Mediay-beta1*Mediax
    y_regresion=beta0+beta1*(x)
    RR=Determination_coefficient(y,y_regresion)
    return RR,y_regresion,beta0,beta1
def regresion_polinomica(x,y,grado):
#la ecu a2*x2+a1*x+b
#b=pr.intercept_
#a2=pr.coef_[2]
#a1=pr.coef_[1]  
    if isinstance(x, pd.core.series.Series):
        x=x.values.reshape([x.values.shape[0],1])#ponemos los vectorees en columnas
        poli_features = PolynomialFeatures(degree = grado)#Elegimos el grado del polinomio
        x=poli_features.fit_transform(x)
        pr = LinearRegression()#escogemos el modelo deseado
        pr.fit(x, y)#hacemos el fiting
        Y_pred=pr.predict(x)#recogemos los datos
        RR=Determination_coefficient(y,Y_pred)
    elif isinstance(x,np.ndarray):
        x=x.reshape([x.shape[0],1])#ponemos los vectorees en columnas
        poli_features = PolynomialFeatures(degree = grado)#Elegimos el grado del polinomio
        x=poli_features.fit_transform(x)
        pr = LinearRegression()#escogemos el modelo deseado
        pr.fit(x, y)#hacemos el fiting
        Y_pred=pr.predict(x)#recogemos los datos
        RR=Determination_coefficient(y,Y_pred)
    return Y_pred,RR, pr.coef_, pr.intercept_



def regresion_martin_ruiz(aoi,datos):
    a_r=1
    RR=0.0
    for i in range(100):     
        IAM_martin_ruiz=pvlib.iam.martin_ruiz(aoi=aoi,a_r=a_r)
        RR_nuevo=Determination_coefficient(datos,IAM_martin_ruiz)
        if(abs(RR_nuevo)<RR):#como es una aproximacion lineal, en el momento que el error se reduce, en la siguiente iteración aumentara este.
            break 
        else:
            RR=RR_nuevo
            a_r=a_r+100000
    return IAM_martin_ruiz,RR,a_r


def regresion_ashrae(aoi,datos):
    b=0.0
    RR=0.0
    for i in range(1000):     
        IAM_ashrae=pvlib.iam.ashrae(aoi=aoi,b=b)
        RR_nuevo=Determination_coefficient(datos,IAM_ashrae)
        if(abs(RR_nuevo)<RR):#como es una aproximacion lineal, en el momento que el que el RR se reduce significa que se esta se aleja del fitting por ello hay que dejar de iterar.
            break 
        else:
            RR=RR_nuevo
            b=b+0.001
    return IAM_ashrae,RR,b


def regresion_physical(aoi, datos):
    x=aoi
    y1=datos  
    LON=10
    incremento=.2
    #tenemos que poner el valor inicial
    n_val=0.7
    k_val=5.0
    l_val=0.1

    Combinaciones=pd.DataFrame(data=np.zeros(((LON**3)+1,4)), dtype='float32', columns=['n','k','l','RR'])
    Combinaciones.iloc[0][0]=n_val
    Combinaciones.iloc[0][1]=k_val
    Combinaciones.iloc[0][2]=l_val
    i=0
    j=0
    p=0
    for i in range(LON):#se ocupará de las centenas, en la base que se ponga de LON
        for j in range(LON):#se ocupará de las decenas
            for p in range(LON):#se ocupará de las unidades
                Combinaciones.iloc[p+LON*j+LON**2*i][3]=Determination_coefficient(y1,np.array(pvlib.iam.physical(aoi=x, n=Combinaciones.iloc[p+LON*j+LON**2*i][0],K=Combinaciones.iloc[p+LON*j+LON**2*i][1], L=Combinaciones.iloc[p+LON*j+LON**2*i][2])))
                Combinaciones.iloc[p+LON*j+LON**2*i+1]=Combinaciones.iloc[p+LON*j+LON**2*i]
                Combinaciones.iloc[p+LON*j+LON**2*i+1][0]=Combinaciones.iloc[p+LON*j+LON**2*i][0]+incremento
            Combinaciones.iloc[p+LON*j+LON**2*i+1][0]=n_val
            Combinaciones.iloc[p+LON*j+LON**2*i+1][1]=Combinaciones.iloc[p+LON*j+LON**2*i][1]+incremento
        Combinaciones.iloc[p+LON*j+LON**2*i+1][0]=n_val
        Combinaciones.iloc[p+LON*j+LON**2*i+1][1]=k_val
        Combinaciones.iloc[p+LON*j+LON**2*i+1][2]=Combinaciones.iloc[p+LON*j+LON**2*i][2]+incremento
    Valores=Combinaciones[Combinaciones['RR']==Combinaciones[:]['RR'].max()]
    IAM_physical=pvlib.iam.physical(aoi=x, n=float(Valores['n']),K=float(Valores['k']), L=float(Valores['l']))
    return IAM_physical,float(Valores['RR']),float(Valores['n']),float(Valores['k']),float(Valores['l'])

# def obtención_dii_efectiva(datos,regresion):
#     df_iam=pd.read_excel("C://Users/juanj/OneDrive/Escritorio/TFG/IAM.xls",encoding='utf-8', dtype={'Segundo grado': np.ndarray})
#     df_iam=df_iam.set_index(df_iam['Unnamed: 0'].values)
#     df_iam=df_iam.drop('Unnamed: 0',axis=1)
#     if regresion=='Segundo grado':
#           IAM_c=(df_iam['Segundo grado']['a_s'][2]*datos**2+df_iam['Segundo grado']['a_s'][1]*datos+df_iam['Segundo grado']['b'])
        
#     elif regresion=='Primer grado':
#         1
#     elif regresion=='Tercer grado':
#         1
#     # a1=1.45965860e-05
#     # a2=-3.50234258e-07
#     # b=0.0007236846839700705
#     # IAM=(datos*a1+datos**2*a2+b)/Valor_normalizar
#     return IAM
def obtencion_dii_efectiva(datos):
    a1=-9.79645026e-03*0.0009180248205304829/0.00096
    a2=5.17456391e-04*0.0009180248205304829/0.00096
    a3=-9.47190593e-06*0.0009180248205304829/0.00096
    b=1.0*0.0009180248205304829/0.00096
    IAM=(a3*datos**3+a2*datos**2+a1*datos+b)
    return IAM


#calcula el iam con los parametros obtenidos tras el estudio de los datos.
#faltaría añadir los tres posibles cálculos de iam implementados en pvlib. Aunque se demostró que se determinaba
#mejor el comportamiento con las regrsiones lineales
def calc_iam(datos,tipo):
    
    df=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/Datos_filtrados_IIIV.csv')
    df_iam=pd.read_csv("C://Users/juanj/OneDrive/Escritorio/TFG/IAM.csv")
    df_iam=df_iam.set_index(df_iam['Unnamed: 0'].values)
    df_iam=df_iam.drop('Unnamed: 0',axis=1)
    if tipo=='Tercer grado':
        a1=df_iam['Tercer grado']['a1']
        a2=df_iam['Tercer grado']['a2']
        a3=df_iam['Tercer grado']['a3']
        b=df_iam['Tercer grado']['b']
        IAM=a1*datos+a2*datos**2+a3*datos**3+b   
    elif tipo=='Segundo grado':
        a1=df_iam['Segundo grado']['a1']
        a2=df_iam['Segundo grado']['a2']
        b=df_iam['Segundo grado']['b']
        IAM=a1*datos+a2*datos**2+b
    elif tipo=='Primer grado':
        thld=df_iam['Primer grado low']['thld']
        a1_low=df_iam['Primer grado low']['a1']
        b_low=df_iam['Primer grado low']['b']
        a1_high=df_iam['Primer grado high']['a1']
        b_high=df_iam['Primer grado high']['b']
        IAM=[]
        for i in range(len(datos)):
            if datos[i]<=thld:
                IAM.append(a1_low*datos[i]+b_low)
            else:
                IAM.append(a1_high*datos[i]+b_high)
    return IAM

# def obtencion_dii_efectiva(datos):
#     a1=-9.79645026e-03
#     a2=5.17456391e-04
#     a3=-9.47190593e-06
#     b=1.0
#     IAM=(a3*datos**3+a2*datos**2+a1*datos+b)
#     return IAM




    
    
    