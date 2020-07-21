# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 09:35:03 2020

@author: juanj
"""

import pvlib
import pandas as pd
import matplotlib.pyplot as plt

tz='Europe/Berlin'
#AOILIMIT
AOILIMIT=55.0
pd.plotting.register_matplotlib_converters()#ESTA SENTENCIA ES NECESARIA PARA DIBUJAR DATE.TIMES
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
primero=pd.DataFrame(dataIV['2018-11-23 14:39']).iloc[2]
primero_V=[primero['Voc (V)'],primero['Vmp (V)'],0.0]
primero_I=[0.0, primero['Imp (A)'],primero['Isc (A)']]

module_parameters_IIIV={'gamma_ref': 5.524, 'mu_gamma': 0.003, 'I_L_ref':0.96,
                'I_o_ref': 0.00000000017,'R_sh_ref': 5226, 'R_sh_0':21000,
                'R_sh_exp': 5.50,'R_s': 0.01,'alpha_sc':0.00,'EgRef':3.91,
                'irrad_ref': 1000,'temp_ref':25, 'cells_in_series':12, 
                'cells_in_parallel': 48, 'eta': 0.32, 'alpha_absorption':0.9,
                'Area':1.2688, 'Impo': 8.3, 'Vmpo':43.9}
#yyyy/mm/dd  	hh:mm	V_Viento	D_Viento	Temp_Air	Rad_Dir	Ele_Sol	  Ori_Sol	Top     	Mid	     Bot	  Cal_Top	 Cal_Mid	Cal_Bot	 Pres_Aire
# 2018/11/23	14:38	1.191	    130.864	    11.413	   341.246	 19.104	  218.791	322.651	  355.873	349.012	   9.766	  10.076	6.977	  350.010
# 2018/11/23	14:39	0.871	    108.398	    11.520	   738.927	 18.989	  218.997	678.662	  755.282	746.253	   59.925	  64.570	46.106	  350.011
temp_cell=pvlib.temperature.pvsyst_cell(poa_global=892, 
                                        temp_air=primero['Tair (°C)'],
                                        wind_speed=1.191, 
                                        u_c=4.5, u_v=0.0, 
                                        eta_m=0.32, alpha_absorption=0.9)
Five_parameters1=pvlib.pvsystem.calcparams_pvsyst(892, temp_cell, alpha_sc=module_parameters_IIIV['alpha_sc'],
                                 gamma_ref=module_parameters_IIIV['gamma_ref'], mu_gamma=module_parameters_IIIV['mu_gamma'],
                                 I_L_ref=module_parameters_IIIV['I_L_ref'], I_o_ref=module_parameters_IIIV['I_o_ref'],
                                 R_sh_ref=module_parameters_IIIV['R_sh_ref'], R_sh_0=module_parameters_IIIV['R_sh_0'], 
                                 R_s=module_parameters_IIIV['R_s'], cells_in_series=module_parameters_IIIV['cells_in_series'], 
                                 R_sh_exp=module_parameters_IIIV['R_sh_exp'], EgRef=module_parameters_IIIV['EgRef'], 
                                 irrad_ref=module_parameters_IIIV['irrad_ref'], temp_ref=module_parameters_IIIV['temp_ref'])
Curvas1=pvlib.pvsystem.singlediode(photocurrent=Five_parameters1[0], saturation_current=Five_parameters1[1],
                                  resistance_series=Five_parameters1[2],resistance_shunt=Five_parameters1[3], 
                                   nNsVth=Five_parameters1[4],ivcurve_pnts=100, method='lambertw')
plt.figure(figsize=(30,15))
plt.plot(primero_V,primero_I,'--',markersize=2,label='datos')
plt.plot(Curvas1['v'],Curvas1['i'],'--',markersize=2,label='Clculado')
plt.title('Comparación de las curvas IV obtenidas con los datos')
plt.xlabel('V[V]')
plt.ylabel('I[A]')
plt.legend()

segundo=pd.DataFrame(dataIV['2018-11-27 14:23']).iloc[2]
segundo_V=[segundo['Voc (V)'],segundo['Vmp (V)'],0.0]
segundo_I=[0.0, segundo['Imp (A)'],segundo['Isc (A)']]

#yyyy/mm/dd  	hh:mm	V_Viento	D_Viento	Temp_Air	Rad_Dir	  Ele_Sol	  Ori_Sol	Top     	Mid	     Bot	  Cal_Top	 Cal_Mid	Cal_Bot	 Pres_Aire
# 2018/11/27	14:23	1.069	   133.592	     12.629	   170.356	  20.281	  214.871	165.613	   179.141	 170.583	13.566	  13.892	9.752	  350.010
# 2018/11/27	14:24	1.035	   138.329	     12.611	   175.512	  20.172	  215.090	170.695	   185.036	 176.535	14.265	  14.630	10.280	  350.011

temp_cell1_2=pvlib.temperature.pvsyst_cell(poa_global=644, 
                                        temp_air=segundo['Tair (°C)'],
                                        wind_speed=1.069, 
                                        u_c=4.5, u_v=0.0, 
                                        eta_m=0.32, alpha_absorption=0.9)

Five_parameters1_2=pvlib.pvsystem.calcparams_pvsyst(644, temp_cell1_2, alpha_sc=module_parameters_IIIV['alpha_sc'],
                                 gamma_ref=module_parameters_IIIV['gamma_ref'], mu_gamma=module_parameters_IIIV['mu_gamma'],
                                 I_L_ref=module_parameters_IIIV['I_L_ref'], I_o_ref=module_parameters_IIIV['I_o_ref'],
                                 R_sh_ref=module_parameters_IIIV['R_sh_ref'], R_sh_0=module_parameters_IIIV['R_sh_0'], 
                                 R_s=module_parameters_IIIV['R_s'], cells_in_series=module_parameters_IIIV['cells_in_series'], 
                                 R_sh_exp=5.5, EgRef=3.91, irrad_ref=1000, temp_ref=25)

Curvas1_2=pvlib.pvsystem.singlediode(photocurrent=Five_parameters1_2[0], saturation_current=Five_parameters1_2[1],
                                  resistance_series=Five_parameters1_2[2],resistance_shunt=Five_parameters1_2[3], 
                                  nNsVth=Five_parameters1_2[4],ivcurve_pnts=100, method='lambertw')

plt.figure(figsize=(30,15))
plt.plot(segundo_V,segundo_I,'--',markersize=2,label='datos')
plt.plot(Curvas1_2['v'],Curvas1_2['i'],'--',markersize=2,label='calculado')
plt.title('Comparación de las curvas IV obtenidas con los datos')
plt.xlabel('V[V]')
plt.ylabel('I[A]')
plt.legend()

plt.figure(figsize=(30,15))
plt.plot(primero_V,primero_I,'--',markersize=2,label='Datos 2018/11/23 14:38')
plt.plot(Curvas1['v'],Curvas1['i'],'--',markersize=2,label='Calculado 2018/11/23 14:38')
plt.plot(segundo_V,segundo_I,'--',markersize=2,label='Datos 2018/11/27 14:23')
plt.plot(Curvas1_2['v'],Curvas1_2['i'],'--',markersize=2,label='Calculado 2018/11/27 14:23')
plt.title('Comparación de las curvas IV obtenidas de III-V con los datos',fontsize=30)
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.xlabel('V[V]',fontsize=30)
plt.ylabel('I[A]',fontsize=30)
plt.legend(fontsize=30,markerscale=3)

#%% BÚSQUEDA PARÁMETROS DE LA PARTE DE SILICIO
primera_iv=pd.read_excel('C://Users/juanj/OneDrive/Escritorio/TFG/Datos_Si.xlsx','I-V Inso_Si 23 11 2018 14h 38m ')
primera_iv=primera_iv[primera_iv['V[V]']>0]
primera_iv=primera_iv[primera_iv['I[A]']>0]
segunda_iv=pd.read_excel('C://Users/juanj/OneDrive/Escritorio/TFG/Datos_Si.xlsx','I-V Inso_Si 27 11 2018 14h 24m')
segunda_iv=segunda_iv[segunda_iv['V[V]']>0]
segunda_iv=segunda_iv[segunda_iv['I[A]']>0]
module_parameters_Si={'gamma_ref': 2.13, 'mu_gamma': 0.002, 'I_L_ref':2.355,
                'I_o_ref': 0.0000147,'R_sh_ref': 3000, 'R_sh_0':8000,
                'R_sh_exp': 5.5,'R_s': 0.35,'alpha_sc':0.0,'EgRef':1.121,
                'irrad_ref': 400,'temp_ref':25, 'cells_in_series':4,
                'eta_m':0.16, 'alpha_absorption':0.9}

#644,892
#950,1081
temp_cell=pvlib.temperature.pvsyst_cell(poa_global=950, 
                                        temp_air=primero['Tair (°C)'],
                                        wind_speed=1.191, 
                                        u_c=29.0, u_v=0.0, 
                                        eta_m=0.1, alpha_absorption=0.9)

temp_cell2=pvlib.temperature.pvsyst_cell(poa_global=1081, 
                                        temp_air=segundo['Tair (°C)'],
                                        wind_speed=1.191, 
                                        u_c=29.0, u_v=0.0, 
                                        eta_m=0.1, alpha_absorption=0.9)

Five_parameters1=pvlib.pvsystem.calcparams_pvsyst(306, temp_cell=temp_cell, alpha_sc=module_parameters_Si['alpha_sc'],
                                 gamma_ref=module_parameters_Si['gamma_ref'], mu_gamma=module_parameters_Si['mu_gamma'],
                                 I_L_ref=module_parameters_Si['I_L_ref'], I_o_ref=module_parameters_Si['I_o_ref'],
                                 R_sh_ref=module_parameters_Si['R_sh_ref'], R_sh_0=module_parameters_Si['R_sh_0'], 
                                 R_s=module_parameters_Si['R_s'], cells_in_series=module_parameters_Si['cells_in_series'], 
                                 R_sh_exp=module_parameters_Si['R_sh_exp'], EgRef=module_parameters_Si['EgRef'], 
                                 irrad_ref=module_parameters_Si['irrad_ref'], temp_ref=module_parameters_Si['temp_ref'])

Curvas1=pvlib.pvsystem.singlediode(photocurrent=Five_parameters1[0], saturation_current=Five_parameters1[1],
                                  resistance_series=Five_parameters1[2],resistance_shunt=Five_parameters1[3], 
                                  nNsVth=Five_parameters1[4],ivcurve_pnts=100, method='lambertw')


Five_parameters2=pvlib.pvsystem.calcparams_pvsyst(190, temp_cell=temp_cell2, alpha_sc=module_parameters_Si['alpha_sc'],
                                 gamma_ref=module_parameters_Si['gamma_ref'], mu_gamma=module_parameters_Si['mu_gamma'],
                                 I_L_ref=module_parameters_Si['I_L_ref'], I_o_ref=module_parameters_Si['I_o_ref'],
                                 R_sh_ref=module_parameters_Si['R_sh_ref'], R_sh_0=module_parameters_Si['R_sh_0'], 
                                 R_s=module_parameters_Si['R_s'], cells_in_series=module_parameters_Si['cells_in_series'], 
                                 R_sh_exp=module_parameters_Si['R_sh_exp'], EgRef=module_parameters_Si['EgRef'], 
                                 irrad_ref=module_parameters_Si['irrad_ref'], temp_ref=module_parameters_Si['temp_ref'])

Curvas2=pvlib.pvsystem.singlediode(photocurrent=Five_parameters2[0], saturation_current=Five_parameters2[1],
                                  resistance_series=Five_parameters2[2],resistance_shunt=Five_parameters2[3], 
                                  nNsVth=Five_parameters2[4],ivcurve_pnts=100, method='lambertw')

plt.figure(figsize=(30,15))
plt.plot(Curvas2['v'],Curvas2['i'],'--',markersize=2,label='Calculado 2018/11/27 14:23')
plt.plot(Curvas1['v'],Curvas1['i'],'--',markersize=2,label='Calculado 2018/11/23 14:38')
plt.plot(segunda_iv['V[V]'],segunda_iv['I[A]'],'--',markersize=2,label='Datos 2018/11/27 14:23')
plt.plot(primera_iv['V[V]'],primera_iv['I[A]'],'--',markersize=2,label='Datos 2018/11/23 14:38')
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.title('Comparación de las curvas obtenidas de Si con los datos',fontsize=30)
plt.xlabel('V[V]',fontsize=30)
plt.ylabel('I[A]',fontsize=30)
plt.legend(fontsize=30,markerscale=3)








