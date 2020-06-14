# -*- coding: utf-8 -*-

import pvlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from cpvtopvlib import cpvsystem
import Error as E
import datetime

tz='Europe/Berlin'

#AOILIMIT
AOILIMIT=55.0
pd.plotting.register_matplotlib_converters()#ESTA SENTENCIA ES NECESARIA PARA DIBUJAR DATE.TIMES

#%%
dataIV= pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/Curvas_IIIV.txt', sep='\t',header=0,encoding='latin1')
dataIV=dataIV[dataIV['Vmp (V)']<40]
dataIV=dataIV[dataIV['Imp (A)']<1]

lim_inferior=dataIV['Pmp (W)'].max()-1

dibujar_puntos=dataIV[dataIV['Pmp (W)']>lim_inferior]
datestr=dataIV['Date (DD/MM/YYYY)']+' '+dataIV['Time (CET)']

dateobject=pd.to_datetime(datestr, format='%d/%m/%Y %H:%M:%S')
Fecha=pd.DatetimeIndex(dateobject,tz=tz)
dataIV=dataIV.set_index(Fecha)

dataIV=dataIV.drop(['Date (DD/MM/YYYY)','Time (CET)'],axis=1)


#Se crean las curvas

V1=[0,30.98,35.65]
I1=[0.8708,0.8089,0]

V2=[0,31.03,35.37]
I2=[0.6473,0.6133,0]




#%%
fig=plt.figure(figsize=(30,15))
 
plt.plot(dataIV['Vmp (V)'],dataIV['Imp (A)'],'o',markersize=2,label='con DII_efectiva y 0.274 de eficiencia')  
plt.plot(dibujar_puntos['Vmp (V)'],dibujar_puntos['Imp (A)'],'o',markersize=2,label='con DII_efectiva y 0.274 de eficiencia')
plt.ylim(0,1) 
plt.xlim(0,50)

plt.xlabel('Horas')
plt.ylabel('Temperatura de célula (°C)')
plt.legend()
plt.title("Temperatura de célula a lo largo de las horas de un día ")



    
#%%código para cuando aoi<AOILIMIT
df=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/Datos_filtrados_IIIV.csv',encoding='utf-8')

#SE filtran los datos que no correspondan a una tendencia clara de la potencia.
CPV=df[(df['aoi']<=AOILIMIT)]
Fecha=pd.DatetimeIndex(CPV['Date Time'])
CPV=CPV.set_index(Fecha)
CPV=CPV.drop(['Date Time'],axis=1)


#%%
limSup=CPV['aoi'].max()
limInf=CPV['aoi'].min()
Rango=limSup-limInf
n_intervalos=100
porcent_mediana=20
incremento=Rango/n_intervalos
for i in range(n_intervalos):
    AUX=CPV[CPV['aoi']>limInf+i*incremento]
    AUX=AUX[AUX['aoi']<=limInf+incremento*(1+i)]
    Mediana=E.mediana(AUX['PMP_estimated_IIIV (W)'].values)
    DEBAJO=AUX[AUX['PMP_estimated_IIIV (W)']<(Mediana*(1-porcent_mediana/100))]   
    CPV=CPV.drop(DEBAJO.index[:],axis=0)
    ENCIMA=AUX[AUX['PMP_estimated_IIIV (W)']>(Mediana*(1+porcent_mediana/100))]
    CPV=CPV.drop(ENCIMA.index[:],axis=0)



Si=df[(df['aoi']>AOILIMIT)]


# CPV['DII_efectiva (W/m2)']=CPV['DII (W/m2)']*E.obtencion_dii_efectiva(CPV['aoi'].values)

CPV['DII_efectiva_tercer_grado (W/m2)']=CPV['DII (W/m2)']*E.calc_iam(CPV['aoi'].values,'Tercer grado')
CPV['DII_efectiva_segundo_grado (W/m2)']=CPV['DII (W/m2)']*E.calc_iam(CPV['aoi'].values,'Segundo grado')
CPV['DII_efectiva_primer_grado (W/m2)']=CPV['DII (W/m2)']*E.calc_iam(CPV['aoi'].values,'Primer grado')
CPV['ISC_IIIV/DII_efectiva_tercer_grado (W/m2)']=CPV['ISC_measured_IIIV (A)']/CPV['DII_efectiva_tercer_grado (W/m2)']
CPV['ISC_IIIV/DII_efectiva_segundo_grado (W/m2)']=CPV['ISC_measured_IIIV (A)']/CPV['DII_efectiva_segundo_grado (W/m2)']
CPV['ISC_IIIV/DII_efectiva_primer_grado (W/m2)']=CPV['ISC_measured_IIIV (A)']/CPV['DII_efectiva_primer_grado (W/m2)']
# Media_temp=df['T_Amb (°C)'].mean()
# df=df[(df['T_Amb (°C)']<Media_temp+3)]
# df=df[(df['T_Amb (°C)']>Media_temp-3)]

# Max_temp=27.0
# Min_temp=19.0
# df=df[(df['T_Amb (°C)']>=Min_temp)]
# df=df[((df['T_Amb (°C)'])<=Max_temp)] 

#------ parámetros de MArcos
module_parameters_IIIV={'gamma_ref': 5.524, 'mu_gamma': 0.003, 'I_L_ref':0.96,
                'I_o_ref': 0.00000000017,'R_sh_ref': 5226, 'R_sh_0':21000,
                'R_sh_exp': 5.50,'R_s': 0.01,'alpha_sc':0.00,'EgRef':3.91,
                'irrad_ref': 1000,'temp_ref':25, 'cells_in_series':12,
                'eta_m':0.274, 'alpha_absorption':0.9}
# module_parameters_Si={'gamma_ref': 6.359, 'mu_gamma': 0.439, 'I_L_ref':1.266,
#                 'I_o_ref': 0.0102,'R_sh_ref': 3200, 'R_sh_0':128000,
#                 'R_sh_exp': 5.5,'R_s': 0.2,'alpha_sc':0.05,'EgRef':1.121,
#                 'irrad_ref': 1000,'temp_ref':25, 'cells_in_series':3,
#                 'eta_m':0.32, 'alpha_absorption':0.9}




SistemaCPV=cpvsystem.StaticCPVSystem(module_parameters=module_parameters_IIIV, 
                                      modules_per_string=1,string_per_inverter=1,
                                      racking_model='freestanding')

# SistemaCPV=cpvsystem.StaticCPVSystem(module_parameters=module_parameters_Si, 
#                                       modules_per_string=1,string_per_inverter=1,
#                                       racking_model='freestanding')


#Se pone la eficiencia por defecto
# temp_cell_DII=pvlib.temperature.pvsyst_cell(poa_global=CPV['DII_efectiva (W/m2)'], temp_air=CPV['T_Amb (°C)'], wind_speed=CPV['Wind Speed (m/s)'], u_c=29.0, u_v=0.0, eta_m=0.1, alpha_absorption=0.9)
temp_cell_=pvlib.temperature.pvsyst_cell(poa_global=CPV['DII (W/m2)'], temp_air=CPV['T_Amb (°C)'], wind_speed=CPV['Wind Speed (m/s)'], u_c=29.0, u_v=0.0, eta_m=0.274, alpha_absorption=1)

#Se pone la eficiencia obtenida según el paper de ASkins=0.274
# temp_cell_DII2=pvlib.temperature.pvsyst_cell(poa_global=CPV['DII_efectiva (W/m2)'], temp_air=CPV['T_Amb (°C)'], wind_speed=CPV['Wind Speed (m/s)'], u_c=29.0, u_v=0.0, eta_m=0.274, alpha_absorption=1)
#Se pone la eficiencia obtenida según el paper de ASkins=0.274 y el coeficiente de 1 ya que no hay reflexion en los datos de DII efectiva
temp_cell_3=pvlib.temperature.pvsyst_cell(poa_global=CPV['DII_efectiva_tercer_grado (W/m2)'], temp_air=CPV['T_Amb (°C)'], wind_speed=CPV['Wind Speed (m/s)'], u_c=29.0, u_v=0.0, eta_m=0.274, alpha_absorption=1)
temp_cell_2=pvlib.temperature.pvsyst_cell(poa_global=CPV['DII_efectiva_segundo_grado (W/m2)'], temp_air=CPV['T_Amb (°C)'], wind_speed=CPV['Wind Speed (m/s)'], u_c=29.0, u_v=0.0, eta_m=0.274, alpha_absorption=1)
temp_cell_1=pvlib.temperature.pvsyst_cell(poa_global=CPV['DII_efectiva_primer_grado (W/m2)'], temp_air=CPV['T_Amb (°C)'], wind_speed=CPV['Wind Speed (m/s)'], u_c=29.0, u_v=0.0, eta_m=0.274, alpha_absorption=1)

# date=np.array(['2019-05-30'])
# for i in range(0,len(CPV.index.values)):
#     if(i==0):
#         date[0]=str(CPV.index[0].date())
#     elif(CPV.index[i-1].date()!=CPV.index[i].date()):
#         date=np.append(date,str(CPV.index[i].date()))
     
# #Para visualizar los datos
# pd.plotting.register_matplotlib_converters()#ESTA SENTENCIA ES NECESARIA PARA DIBUJAR DATE.TIMES
# for i in date:
#     fig=plt.figure(figsize=(30,15))
#     plt.plot(CPV[str(i)].index[:].time,temp_cell[str(i)],label='dni')   
#     plt.plot(CPV[str(i)].index[:].time,temp_cell_DII[str(i)],label='ghi')

#     plt.xlabel('Hora')
#     plt.ylabel('Irradiancia (W/m2)')
#     plt.legend()
#     plt.title("Irradiancias calculadas "+ str(i))
    
fig=plt.figure(figsize=(30,15))
plt.plot(CPV.index[:].time,temp_cell_,'o',markersize=2,label='con GII')   
# plt.plot(CPV.index[:].time,temp_cell_DII2,'o',markersize=2,label='con DII_efectiva y 0.274 de eficiencia')   
plt.plot(CPV.index[:].time,temp_cell_3,'o',markersize=2,label='con DII_efectiva y 0.274 de eficiencia y 1 como coeficiente de absorción')   
plt.plot(dataIV.index[:].time,dataIV['Tlens (°C)'],'o',markersize=2,label='datos')   

plt.xlabel('Horas')
plt.ylabel('Temperatura de célula (°C)')
plt.legend()
plt.title("Temperatura de célula a lo largo de las horas de un día ")


#%%
# y_poli,RR_poli,a_s,b=E.regresion_polinomica(df_filt_temp['aoi'].values,df_filt_temp['ISC_IIIV/DII (A m2/W)'].values,2)
# # Valor_normalizar=y_poli.max()
# Valor_normalizar=0.00096
# IAM=y_poli/Valor_normalizar

# iam=y_poli

# temp_cell_DII=temp_cell_DII3

Five_parameters=SistemaCPV.calcparams_pvsyst(CPV['DII (W/m2)'], temp_cell_)
Five_parameters_3=SistemaCPV.calcparams_pvsyst(CPV['DII_efectiva_tercer_grado (W/m2)'], temp_cell_3)
Five_parameters_2=SistemaCPV.calcparams_pvsyst(CPV['DII_efectiva_segundo_grado (W/m2)'], temp_cell_2)
Five_parameters_1=SistemaCPV.calcparams_pvsyst(CPV['DII_efectiva_primer_grado (W/m2)'], temp_cell_1)

# Five_parameters=SistemaCPV.calcparams_pvsyst(CPV['DII (W/m2)'], 53)
# Five_parameters_3=SistemaCPV.calcparams_pvsyst(CPV['DII_efectiva_tercer_grado (W/m2)'], 53)
# Five_parameters_2=SistemaCPV.calcparams_pvsyst(CPV['DII_efectiva_segundo_grado (W/m2)'], 53)
# Five_parameters_1=SistemaCPV.calcparams_pvsyst(CPV['DII_efectiva_primer_grado (W/m2)'], 53)
# Five_parameters2_GII=SistemaCPV.calcparams_pvsyst(CPV['DII_efectiva2 (W/m2)'], temp_cell_GII)

Curvas=pvlib.pvsystem.singlediode(photocurrent=Five_parameters[0], saturation_current=Five_parameters[1],
                                  resistance_series=Five_parameters[2],resistance_shunt=Five_parameters[3], 
                                  nNsVth=Five_parameters[4],ivcurve_pnts=100, method='lambertw')


Curvas_=pvlib.pvsystem.singlediode(photocurrent=Five_parameters[0], saturation_current=Five_parameters[1],
                                  resistance_series=Five_parameters[2],resistance_shunt=Five_parameters[3], 
                                  nNsVth=Five_parameters[4],ivcurve_pnts=100, method='lambertw')
Curvas_3=pvlib.pvsystem.singlediode(photocurrent=Five_parameters_3[0], saturation_current=Five_parameters_3[1],
                                  resistance_series=Five_parameters_3[2],resistance_shunt=Five_parameters_3[3], 
                                  nNsVth=Five_parameters_3[4],ivcurve_pnts=100, method='lambertw')
Curvas_2=pvlib.pvsystem.singlediode(photocurrent=Five_parameters_2[0], saturation_current=Five_parameters_2[1],
                                  resistance_series=Five_parameters_2[2],resistance_shunt=Five_parameters_2[3], 
                                  nNsVth=Five_parameters_2[4],ivcurve_pnts=100, method='lambertw')
Curvas_1=pvlib.pvsystem.singlediode(photocurrent=Five_parameters_1[0], saturation_current=Five_parameters_1[1],
                                  resistance_series=Five_parameters_1[2],resistance_shunt=Five_parameters_1[3], 
                                  nNsVth=Five_parameters_1[4],ivcurve_pnts=100, method='lambertw')

#Representamos unas cuantas curavs iv
plt.figure(figsize=(30,15))
plt.plot(Curvas_['v'][165],Curvas_['i'][165],'--',markersize=2,label='Sin IAM')
plt.plot(Curvas_3['v'][165],Curvas_3['i'][165],'--',markersize=2,label='IAM_tercer_grado')
plt.plot(Curvas_2['v'][165],Curvas_2['i'][165],'--',markersize=2,label='IAM_segundo_grado')
plt.plot(Curvas_1['v'][165],Curvas_1['i'][165],'--',markersize=2,label='IAM_primer_grado')
# plt.plot(Curvas['v'][165],Curvas['i'][165],'--',markersize=2,label='GII')
plt.plot(dibujar_puntos['Vmp (V)'],dibujar_puntos['Imp (A)'],'o',markersize=2,label='con DII_efectiva y 0.274 de eficiencia')
plt.plot()
plt.xlabel('Voltaje (III-V) (V)')
plt.ylabel('Corriente (III-V) (A)')
plt.title('Curvas I-V para validar el proceso anterior')
plt.legend()

#Comparamos los datos de Pmp con los calculados
plt.figure(figsize=(30,15))
plt.plot(CPV['aoi'],CPV['PMP_estimated_IIIV (W)'],'o',markersize=2,label='Datos ')
plt.plot(CPV['aoi'],Curvas_['p_mp'],'o',markersize=2,label='sin iam')
plt.plot(CPV['aoi'],Curvas_3['p_mp'],'o',markersize=2,label='IAM_tercer_grado')
plt.plot(CPV['aoi'],Curvas_2['p_mp'],'o',markersize=2,label='IAM_segundo_grado')
plt.plot(CPV['aoi'],Curvas_1['p_mp'],'o',markersize=2,label='IAM_primer_grado')
plt.xlabel('Ángulo de incidencia (°)')
plt.ylabel('Puntos de máxima potencia (W)')
plt.title('Comparación de los resultados con los datos estimados de potencias en funcion del iam')
plt.legend()



#%%
UF=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/UF.csv')
UF=UF.set_index(UF['Unnamed: 0'])
UF=UF.drop(['Unnamed: 0'],axis=1)

#AHORA HAY QUE GENERAR LOS VALORES CON LOS LAS PENDIENTES DE LOS UF
#hora hay que aplicar el método de UF
x_am=CPV['airmass_absolute'].values

# y=CPV['ISC_IIIV/DII (A m2/W)'].values
thld_am=UF.loc['thld']['UF_am_low']

a_am_low=UF.loc['a']['UF_am_low']
a_am_high=UF.loc['a']['UF_am_high']

UF_am=[]
for i in range(len(x_am)):
    if x_am[i]<=thld_am:
        UF_am.append(1 + ( x_am[i]- thld_am) * (a_am_low))
    else:
        UF_am.append(1 + ( x_am[i]- thld_am) * (a_am_high))
UF_am=np.array(UF_am)        
        

fig=plt.figure(figsize=(30,15))
plt.plot(x_am,UF_am,'o',markersize=4,label='Datos primera parte')
#%%

thld_temp=UF.loc['thld']['UF_temp']
x_temp=CPV['T_Amb (°C)'].values
a_temp=UF.loc['a']['UF_temp']

UF_temp=[]
for i in range(len(x_temp)):
    UF_temp.append(1 + ( x_temp[i]- thld_temp) * (a_temp))

        
        
UF_temp=np.array(UF_temp)
fig=plt.figure(figsize=(30,15))
plt.plot(x_temp,UF_temp,'o',markersize=4,label='Datos primera parte')

#%%COMPARACION CON EL METODO DE REGRESION POLINOMICA DE GRADO 3

#Ahora hay que buscar los pesos que mejor describan las potencias.
w_am=0.5
w_temp=0.5

Potencias_estimadas=pd.DataFrame(columns=['Potencias_estimadas (W)','diferencias', 'RMSE'])
datos_potencia=CPV['PMP_estimated_IIIV (W)'].values

aux=np.arange(0,1,0.001)
for i in aux:
    w_am=i
    w_temp=1-w_am    
    UF_total=w_am*UF_am+w_temp*UF_temp 
    estimacion=Curvas_3['p_mp']*UF_total
    Juntos=[estimacion,estimacion-datos_potencia,E.RMSE(datos_potencia,estimacion)]    
    Potencias_estimadas.loc['w_am='+str(i)]=Juntos
    

   
index=Potencias_estimadas[Potencias_estimadas['RMSE']==Potencias_estimadas['RMSE'].min()].index[0]
w_am=float(index[5:])
w_temp=1-w_am

plt.figure(figsize=(30,15))
plt.plot(CPV['aoi'],Curvas_3['p_mp'],'o',markersize=2,label='sin UF')
plt.plot(CPV['aoi'],Potencias_estimadas['Potencias_estimadas (W)'][index],'o',markersize=2,label='Con UF')
plt.plot(CPV['aoi'],CPV['PMP_estimated_IIIV (W)'],'o',markersize=2,label='Datos ')
plt.xlabel('Ángulo de incidencia (°)')
plt.ylabel('Potencia (III-V)(W)')
plt.title('Comparación de los resultados con los datos estimados de potencias en funcion del UF')
plt.legend()

plt.figure(figsize=(30,15))
plt.plot(CPV['aoi'],Potencias_estimadas['diferencias'][index],'o',markersize=4,label='Residuos de las potencias calculadas ')
plt.xlabel('Ángulo de incidencia (°)')
plt.ylabel('Potencia (III-V)(W)')
plt.title('Residuos de las potencias calculadas con los datos estimados')
plt.legend()


plt.figure(figsize=(30,15))
plt.plot(CPV['T_Amb (°C)'],Potencias_estimadas['diferencias'][index],'o',markersize=4,label='Residuos de las potencias calculadas ')
plt.xlabel('Temperatura ambiente (°C)')
plt.ylabel('Potencia (III-V)(W)')
plt.title('Residuos de las potencias calculadas con los datos estimados')
plt.legend()

plt.figure(figsize=(30,15))
plt.plot(CPV['airmass_absolute'],Potencias_estimadas['diferencias'][index],'o',markersize=4,label='Residuos de las potencias calculadas ')
plt.xlabel('airmass (n.d.)')
plt.ylabel('Potencia (III-V)(W)')
plt.title('Residuos de las potencias calculadas con los datos estimados')
plt.legend()
print('El error cuadrático medio de las estimación es de: ' + str(Potencias_estimadas['RMSE'][index]))
print('Los valores de los pesos son: ')
print('w_am= '+ str(w_am) + 'y '+ str(w_temp))

#%%COMPARACION CON LA REGRESION POLINOMICA DE GRADO 1

#Ahora hay que buscar los pesos que mejor describan las potencias.
w_am=0.5
w_temp=0.5

Potencias_estimadas=pd.DataFrame(columns=['Potencias_estimadas (W)','diferencias', 'RMSE'])
datos_potencia=CPV['PMP_estimated_IIIV (W)'].values

aux=np.arange(0,1,0.001)
for i in aux:
    w_am=i
    w_temp=1-w_am    
    UF_total=w_am*UF_am+w_temp*UF_temp 
    estimacion=Curvas_1['p_mp']*UF_total
    Juntos=[estimacion,estimacion-datos_potencia,E.RMSE(datos_potencia,estimacion)]    
    Potencias_estimadas.loc['w_am='+str(i)]=Juntos
    

   
index=Potencias_estimadas[Potencias_estimadas['RMSE']==Potencias_estimadas['RMSE'].min()].index[0]
w_am=float(index[5:])
w_temp=1-w_am

plt.figure(figsize=(30,15))
plt.plot(CPV['aoi'],Curvas_1['p_mp'],'o',markersize=2,label='sin UF')
plt.plot(CPV['aoi'],Potencias_estimadas['Potencias_estimadas (W)'][index],'o',markersize=2,label='Con UF')
plt.plot(CPV['aoi'],CPV['PMP_estimated_IIIV (W)'],'o',markersize=2,label='Datos ')
plt.xlabel('Ángulo de incidencia (°)')
plt.ylabel('Potencia (III-V)(W)')
plt.title('Comparación de los resultados con los datos estimados de potencias en funcion del UF')
plt.legend()

plt.figure(figsize=(30,15))
plt.plot(CPV['aoi'],Potencias_estimadas['diferencias'][index],'o',markersize=4,label='Residuos de las potencias calculadas ')
plt.xlabel('Ángulo de incidencia (°)')
plt.ylabel('Potencia (III-V)(W)')
plt.title('Residuos de las potencias calculadas con los datos estimados')
plt.legend()


plt.figure(figsize=(30,15))
plt.plot(CPV['T_Amb (°C)'],Potencias_estimadas['diferencias'][index],'o',markersize=4,label='Residuos de las potencias calculadas ')
plt.xlabel('Temperatura ambiente (°C)')
plt.ylabel('Potencia (III-V)(W)')
plt.title('Residuos de las potencias calculadas con los datos estimados')
plt.legend()

plt.figure(figsize=(30,15))
plt.plot(CPV['airmass_absolute'],Potencias_estimadas['diferencias'][index],'o',markersize=4,label='Residuos de las potencias calculadas ')
plt.xlabel('airmass (n.d.)')
plt.ylabel('Potencia (III-V)(W)')
plt.title('Residuos de las potencias calculadas con los datos estimados')
plt.legend()
print('El error cuadrático medio de las estimaciones es de: ' + str(Potencias_estimadas['RMSE'][index]))
print('Los valores de los pesos son: ')
print('w_am= '+ str(w_am) + 'y '+ str(w_temp))
#%%COMPARACION CON LA REGRESION POLINOMICA DE GRADO 2

#Ahora hay que buscar los pesos que mejor describan las potencias.
w_am=0.5
w_temp=0.5

Potencias_estimadas=pd.DataFrame(columns=['Potencias_estimadas (W)','diferencias', 'RMSE'])
datos_potencia=CPV['PMP_estimated_IIIV (W)'].values

aux=np.arange(0,1,0.001)
for i in aux:
    w_am=i
    w_temp=1-w_am    
    UF_total=w_am*UF_am+w_temp*UF_temp 
    estimacion=Curvas_2['p_mp']*UF_total
    Juntos=[estimacion,estimacion-datos_potencia,E.RMSE(datos_potencia,estimacion)]    
    Potencias_estimadas.loc['w_am='+str(i)]=Juntos
    

   
index=Potencias_estimadas[Potencias_estimadas['RMSE']==Potencias_estimadas['RMSE'].min()].index[0]
w_am=float(index[5:])
w_temp=1-w_am

plt.figure(figsize=(30,15))
plt.plot(CPV['aoi'],Curvas_2['p_mp'],'o',markersize=2,label='sin UF')
plt.plot(CPV['aoi'],Potencias_estimadas['Potencias_estimadas (W)'][index],'o',markersize=2,label='Con UF')
plt.plot(CPV['aoi'],CPV['PMP_estimated_IIIV (W)'],'o',markersize=2,label='Datos ')
plt.xlabel('Ángulo de incidencia (°)')
plt.ylabel('Potencia (III-V)(W)')
plt.title('Comparación de los resultados con los datos estimados de potencias en funcion del UF')
plt.legend()

plt.figure(figsize=(30,15))
plt.plot(CPV['aoi'],Potencias_estimadas['diferencias'][index],'o',markersize=4,label='Residuos de las potencias calculadas ')
plt.xlabel('Ángulo de incidencia (°)')
plt.ylabel('Potencia (III-V)(W)')
plt.title('Residuos de las potencias calculadas con los datos estimados')
plt.legend()


plt.figure(figsize=(30,15))
plt.plot(CPV['T_Amb (°C)'],Potencias_estimadas['diferencias'][index],'o',markersize=4,label='Residuos de las potencias calculadas ')
plt.xlabel('Temperatura ambiente (°C)')
plt.ylabel('Potencia (III-V)(W)')
plt.title('Residuos de las potencias calculadas con los datos estimados')
plt.legend()

plt.figure(figsize=(30,15))
plt.plot(CPV['airmass_absolute'],Potencias_estimadas['diferencias'][index],'o',markersize=4,label='Residuos de las potencias calculadas ')
plt.xlabel('airmass (n.d.)')
plt.ylabel('Potencia (III-V)(W)')
plt.title('Residuos de las potencias calculadas con los datos estimados')
plt.legend()
print('El error cuadrático medio de las estimaciones es de: ' + str(Potencias_estimadas['RMSE'][index]))
print('Los valores de los pesos son: ')
print('w_am= '+ str(w_am) + 'y '+ str(w_temp))

#%%COMPARACION CON LA ACTUAL PREVISION DE POTENCIA

#Ahora hay que buscar los pesos que mejor describan las potencias.


Potencias_estimadas=pd.DataFrame(columns=['Potencias_estimadas (W)','diferencias'])
datos_potencia=CPV['PMP_estimated_IIIV (W)'].values
Potencias_estimadas['Potencias_estimadas (W)']=Curvas_['p_mp']
Potencias_estimadas['diferencias']=Curvas_['p_mp']-datos_potencia
RMSE=E.RMSE(datos_potencia,Curvas_['p_mp'])


plt.figure(figsize=(30,15))
plt.plot(CPV['aoi'],Curvas_['p_mp'],'o',markersize=2,label='Previsión actual')
# plt.plot(CPV['aoi'],Potencias_estimadas['Potencias_estimadas (W)'],'o',markersize=2,label='Con UF')
plt.plot(CPV['aoi'],CPV['PMP_estimated_IIIV (W)'],'o',markersize=2,label='Datos ')
plt.xlabel('Ángulo de incidencia (°)')
plt.ylabel('Potencia (III-V)(W)')
plt.title('Comparación de los resultados con los datos estimados de potencias en funcion del UF')
plt.legend()

plt.figure(figsize=(30,15))
plt.plot(CPV['aoi'],Potencias_estimadas['diferencias'],'o',markersize=4,label='Residuos de las potencias calculadas ')
plt.xlabel('Ángulo de incidencia (°)')
plt.ylabel('Potencia (III-V)(W)')
plt.title('Residuos de las potencias calculadas con los datos estimados')
plt.legend()


plt.figure(figsize=(30,15))
plt.plot(CPV['T_Amb (°C)'],Potencias_estimadas['diferencias'],'o',markersize=4,label='Residuos de las potencias calculadas ')
plt.xlabel('Temperatura ambiente (°C)')
plt.ylabel('Potencia (III-V)(W)')
plt.title('Residuos de las potencias calculadas con los datos estimados')
plt.legend()

plt.figure(figsize=(30,15))
plt.plot(CPV['airmass_absolute'],Potencias_estimadas['diferencias'],'o',markersize=4,label='Residuos de las potencias calculadas ')
plt.xlabel('airmass (n.d.)')
plt.ylabel('Potencia (III-V)(W)')
plt.title('Residuos de las potencias calculadas con los datos estimados')
plt.legend()
print('El error cuadrático medio de las estimaciones es de: ' + str(RMSE))


#%%COMPROBAR CURVAS 3-5

module_parameters_IIIV={'gamma_ref': 5.524, 'mu_gamma': 0.003, 'I_L_ref':0.96,
                'I_o_ref': 0.00000000017,'R_sh_ref': 5226, 'R_sh_0':21000,
                'R_sh_exp': 5.50,'R_s': 0.01,'alpha_sc':0.00,'EgRef':3.91,
                'irrad_ref': 1000,'temp_ref':25, 'cells_in_series':12,
                'eta_m':0.274, 'alpha_absorption':1}





SistemaCPV=cpvsystem.StaticCPVSystem(module_parameters=module_parameters_IIIV, 
                                      modules_per_string=1,string_per_inverter=1,
                                      racking_model='freestanding')


Five_parameters=SistemaCPV.calcparams_pvsyst(890, 80)
Five_parameters1=SistemaCPV.calcparams_pvsyst(644, 80)

Curvas=pvlib.pvsystem.singlediode(photocurrent=Five_parameters[0], saturation_current=Five_parameters[1],
                                  resistance_series=Five_parameters[2],resistance_shunt=Five_parameters[3], 
                                  nNsVth=Five_parameters[4],ivcurve_pnts=100, method='lambertw')
Curvas1=pvlib.pvsystem.singlediode(photocurrent=Five_parameters1[0], saturation_current=Five_parameters1[1],
                                  resistance_series=Five_parameters1[2],resistance_shunt=Five_parameters1[3], 
                                  nNsVth=Five_parameters1[4],ivcurve_pnts=100, method='lambertw')


plt.figure(figsize=(30,15))

plt.plot(Curvas1['v'],Curvas1['i'],'--',markersize=2,label='644')
plt.plot(Curvas['v'],Curvas['i'],'--',markersize=2,label='890')
plt.plot(V1,I1,'--',markersize=2,label='datos_890')
plt.plot(V2,I2,'--',markersize=2,label='datos_644')

plt.title('Comparación de las curvas IV obtenidas con los datos')
plt.xlabel('V[V]')
plt.ylabel('I[A]')

plt.legend()


#%%CÓDIGO PARA CUANDO AOI>AOILIMIT ,no corre prisa es mas importante el silicio

# df_filt_AOILIMIT=df[(df['aoi']>AOILIMIT)]
# temp_cell=pvlib.temperature.pvsyst_cell(poa_global=df_filt_AOILIMIT['GII (W/m2)'], 
#                                         temp_air=df_filt_AOILIMIT['T_Amb (°C)'], 
#                                         wind_speed=df_filt_AOILIMIT['Wind Speed (m/s)'], 
#                                         u_c=29.0, u_v=0.0, eta_m=0.1, alpha_absorption=0.9)

# y_poli,RR_poli,a_s,b=E.regresion_polinomica(df_filt_AOILIMIT['aoi'].values,df_filt_AOILIMIT['ISC_IIIV/DII (A m2/W)'].values,2)

# Valor_normalizar=0.00096
# IAM=y_poli/Valor_normalizar


# effective_irradiance=df_filt_AOILIMIT['DII (W/m2)']*IAM



# Five_parameters=SistemaCPV.calcparams_pvsyst(effective_irradiance, temp_cell)
# Five_parameters1=SistemaCPV.calcparams_pvsyst(df_filt_AOILIMIT['DII (W/m2)'], temp_cell)


# Curvas=pvlib.pvsystem.singlediode(photocurrent=Five_parameters[0], saturation_current=Five_parameters[1],
#                                   resistance_series=Five_parameters[2],resistance_shunt=Five_parameters[3], 
#                                   nNsVth=Five_parameters[4],ivcurve_pnts=100, method='lambertw')
# Curvas1=pvlib.pvsystem.singlediode(photocurrent=Five_parameters1[0], saturation_current=Five_parameters1[1],
#                                   resistance_series=Five_parameters1[2],resistance_shunt=Five_parameters1[3], 
#                                   nNsVth=Five_parameters1[4],ivcurve_pnts=100, method='lambertw')

# # #Representamos unas cuantas curavs iv
# plt.figure(figsize=(30,15))

# plt.plot(Curvas['v'][0],Curvas['i'][0],'--',markersize=2,label='IAM(AOI)')
# plt.plot(Curvas['v'][5],Curvas['i'][5],'--',markersize=2,label='IAM(AOI)')
# plt.plot(Curvas['v'][10],Curvas['i'][10],'--',markersize=2,label='IAM(AOI)')
# plt.plot(Curvas['v'][50],Curvas['i'][50],'--',markersize=2,label='IAM(AOI)')

# #Comparamos los datos de Pmp con los calculados
# plt.figure(figsize=(30,15))
# plt.plot(df_filt_AOILIMIT['aoi'],Curvas['p_mp'],'o',markersize=2,label='con iam')
# plt.plot(df_filt_AOILIMIT['aoi'],Curvas1['p_mp'],'o',markersize=2,label='sin iam')
# plt.plot(df_filt_AOILIMIT['aoi'],df_filt_AOILIMIT['PMP_estimated_IIIV (W)'],'o',markersize=2,label='Datos ')
# plt.legend()

# # UF=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/UF.csv',encoding='utf-8')

# # Max_temp=27.0
# # Min_temp=19.0
# # UF=UF[(UF['temp']>=Min_temp)]
# # UF=UF[((UF['temp'])<=Max_temp)] 



# # #Ahora hay que buscar los pesos que mejor describan las potencias.
# # w_am=0.5
# # w_temp=0.5

# # UF_total=w_am*UF['UF_am']+w_temp*UF['UF_temp']
# # Potencia_estimada=Curvas['p_mp']*UF_total

# # plt.figure(figsize=(30,15))
# # plt.plot(df_filt_temp['aoi'],Curvas['p_mp'],'o',markersize=2,label='con iam')
# # plt.plot(df_filt_temp['aoi'],Potencia_estimada,'o',markersize=2,label='sin iam')
# # plt.plot(df_filt_temp['aoi'],df_filt_temp['PMP_estimated_IIIV (W)'],'o',markersize=2,label='Datos ')
# # plt.legend()

# # Potencias_estimadas=pd.DataFrame(columns=['Potencias_estimadas (W)','diferencias', 'RMSE'])
# # datos_potencia=df_filt_temp['PMP_estimated_IIIV (W)'].values

# # aux=np.arange(0,1,0.01)
# # for i in aux:
# #     w_am=i
# #     w_temp=1-w_am    
# #     UF_total=w_am*UF['UF_am']+w_temp*UF['UF_temp']   
# #     estimacion=Curvas['p_mp']*UF_total
# #     Juntos=[estimacion,datos_potencia-estimacion,E.RMSE(datos_potencia,estimacion)]    
# #     Potencias_estimadas.loc['w_am='+str(i)]=Juntos
    

   
# # index=Potencias_estimadas[Potencias_estimadas['RMSE']==Potencias_estimadas['RMSE'].min()].index[0]


# # plt.figure(figsize=(30,15))
# # plt.plot(df_filt_temp['aoi'],Potencias_estimadas['diferencias'][index],'o',markersize=4,label='con iam')
# # plt.legend()

# # plt.figure(figsize=(30,15))
# # plt.plot(df_filt_temp['aoi'],Potencias_estimadas['Potencias_estimadas (W)'][index],'o',markersize=4,label='Potencia estimada')
# # plt.plot(df_filt_temp['aoi'],datos_potencia,'o',markersize=4,label='Datos de potencia')
# # plt.legend()


