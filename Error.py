

import numpy as np#para trabajas con vectores mucho más rapido

#estos son los modulos necesarios para el fiting polinomial
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures



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

    if len(datos) % 2 == 0:
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
   
    x=x.values.reshape([x.values.shape[0],1])#ponemos los vectorees en columnas
    poli_features = PolynomialFeatures(degree = grado)#Elegimos el grado del polinomio
    x=poli_features.fit_transform(x)
    pr = LinearRegression()#escogemos el modelo deseado
    pr.fit(x, y)#hacemos el fiting
    Y_pred=pr.predict(x)#recogemos los datos
    RR=Determination_coefficient(y,Y_pred)
    return Y_pred,RR, pr.coef_, pr.intercept_
    #representamos los datos obtenidos comparandolos con los datos 
#    plt.figure(figsize=(20,15))
#    plt.plot(df['aoi'],df['IAM_aoi_'],'o')
#    plt.plot(df['aoi'],Y_pred,'o')
#    #y_excel=-0.0004*(df['aoi']**2)+0.161*df['aoi']+0.8437
#    #plt.plot(df['aoi'],y_excel,'o')
#    E.Determination_coefficient(df['IAM_aoi_'],Y_pred)

    
    
    
    
    
    