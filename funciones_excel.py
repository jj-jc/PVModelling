#definimos la funcion que aproximan los resultados empíricos
def f1(x):
    return (-0.0003*(x**2) + 0.0027*(x) + 0.9893)
def f_regre(x,a,b,c):
    return a+b*x+c*(x**2)