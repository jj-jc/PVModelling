# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 17:07:44 2020

@author: juanj
"""




import CPVClass
import pandas as pd
import matplotlib.pyplot as plt
import Error as E
AOILIMIT=55.0
#%%código para cuando aoi<AOILIMIT
df=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/Datos_filtrados_IIIV.csv',encoding='utf-8')

#SE filtran los datos que no correspondan a una tendencia clara de la potencia.
CPV=df[(df['aoi']<=AOILIMIT)]
Fecha=pd.DatetimeIndex(CPV['Date Time'])
CPV=CPV.set_index(Fecha)
CPV=CPV.drop(['Date Time'],axis=1)
#de esta forma nos quitamos los valores que sean muy dispares.
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


#%% Probamos la clase creada.
Mi_CPV=CPVClass.CPVSystem(surface_tilt=0, surface_azimuth=180,
                 albedo=None, surface_type=None,
                 module=None, module_type='glass_polymer',
                 module_parameters=None,
                 temperature_model_parameters=None,
                 modules_per_string=1, strings_per_inverter=1,
                 inverter=None, inverter_parameters=None,
                 racking_model='open_rack', losses_parameters=None, name=None,
                 iam_parameters=None)

Mi_CPV.module_parameters={'gamma_ref': 5.524, 'mu_gamma': 0.003, 'I_L_ref':0.96,
                'I_o_ref': 0.00000000017,'R_sh_ref': 5226, 'R_sh_0':21000,
                'R_sh_exp': 5.50,'R_s': 0.01,'alpha_sc':0.00,'EgRef':3.91,
                'irrad_ref': 1000,'temp_ref':25, 'cells_in_series':12,
                'eta_m':0.274, 'alpha_absorption':1}

Mi_CPV.temperature_model_parameters={'u_c': 29,
                                     'u_v':0}


Mi_CPV.iam_parameters={'a3':-8.315977512579898e-06,'a2':0.00039212250547851236,
                        'a1':-0.006006260890940105,'b':1.0}

Mi_CPV.uf_parameters={'m1_am':0.167973, 'thld_am':1.284187 ,'m2_am':-0.396000,
                      'm_temp':-0.006439, 'thld_temp':15.18,
                      'w_am':0.031,'w_temp': 0.969}

IAM=Mi_CPV.get_iam(aoi=CPV['aoi'],iam_model='tercer grado')

CPV['DII_efectiva']=CPV['DII (W/m2)']*IAM



temp_cell_=Mi_CPV.pvsyst_celltemp(poa_global=CPV['DII_efectiva'], temp_air=CPV['T_Amb (°C)'], wind_speed=CPV['Wind Speed (m/s)'])



Five_parameters=Mi_CPV.calcparams_pvsyst(CPV['DII_efectiva'], temp_cell_)



Curvas=Mi_CPV.singlediode(photocurrent=Five_parameters[0], saturation_current=Five_parameters[1],
                                  resistance_series=Five_parameters[2],resistance_shunt=Five_parameters[3], 
                                  nNsVth=Five_parameters[4],ivcurve_pnts=100)


plt.figure(figsize=(30,15))
plt.plot(Curvas['v'][165],Curvas['i'][165],'--',markersize=2,label='Sin IAM')
plt.plot()
plt.xlabel('Voltaje (III-V) (V)')
plt.ylabel('Corriente (III-V) (A)')
plt.title('Curvas I-V para validar el proceso anterior')
plt.legend()


UF=Mi_CPV.get_uf(CPV['airmass_relative'].values, CPV['T_Amb (°C)'].values)

Potencias_estimadas=Curvas['p_mp']*UF


plt.figure(figsize=(30,15))
plt.plot(CPV['aoi'],Curvas['p_mp'],'o',markersize=2,label='sin UF')
plt.plot(CPV['aoi'],Potencias_estimadas,'o',markersize=2,label='Con UF')
plt.plot(CPV['aoi'],CPV['PMP_estimated_IIIV (W)'],'o',markersize=2,label='Datos ')
plt.xlabel('Ángulo de incidencia (°)')
plt.ylabel('Potencia (III-V)(W)')
plt.title('Comparación de los resultados con los datos estimados de potencias en funcion del UF')
plt.legend()

df=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/Datos_filtrados_IIIV.csv')




filt_df=df[df['aoi']<=AOILIMIT]
filt_df['DII_efectiva (W/m2)']=filt_df['DII (W/m2)']*E.calc_iam(filt_df['aoi'].values,'Tercer grado')
filt_df['ISC_IIIV/DII_efectiva (A m2/W)']=filt_df['ISC_measured_IIIV (A)']/filt_df['DII_efectiva (W/m2)']
filt_x=filt_df['T_Amb (°C)'].values
filt_y=filt_df['ISC_IIIV/DII_efectiva (A m2/W)'].values


filt_df_am=filt_df
filt_df_am=filt_df_am[filt_df_am['Wind Speed (m/s)']>=0.9]
filt_df_am=filt_df_am[filt_df_am['Wind Speed (m/s)']<1.1]
filt_df_am=filt_df_am[filt_df_am['T_Amb (°C)']>=20]
filt_df_am=filt_df_am[filt_df_am['T_Amb (°C)']<28]


Mi_CPV.generate_uf_am_params(filt_df_am['airmass_relative'].values,filt_df_am['airmass_relative'].values)






