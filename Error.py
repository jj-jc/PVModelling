import numpy as np

def ECM(datos,estimaciones):
    sum=0
    for i in range(len(datos)):
        sum=sum+(datos[i]-estimaciones[i])**2
    return float(sum/len(datos))


