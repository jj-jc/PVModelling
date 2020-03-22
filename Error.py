import numpy as np

def SS_res(datos,estimaciones):#residuos
    sum=0
    for i in range(len(datos)):
        sum=sum+(datos[i]-estimaciones[i])**2
    return float(sum)

def SS_tot(datos):#varianza de los datos
    sum=0
    num_datos=len(datos)
    for i in range(num_datos):
        sum=sum+datos[i]
    media=sum/num_datos
    sum=0
    for i in range(num_datos):
        sum=sum+((datos[i]-media)**2)
    return float(sum)

def SS_reg(datos,estimaciones):#Varianza de los datos estimados
    sum=0
    num_datos=len(datos)
    for i in range(num_datos):
        sum=sum+datos[i]
    media=sum/num_datos
    sum=0
    for i in range(num_datos):
        sum=sum+(estimaciones[i]-media)**2
    return float(sum)
def Determination_coefficient(datos,estimaciones):
    try:
        return 1-(SS_res(datos,estimaciones)/SS_tot(datos))
    except ZeroDivisionError:
        print('No se puede realizar una division por cero')
        return 1