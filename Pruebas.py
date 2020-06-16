# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 11:03:31 2020

@author: juanj
"""


# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 20:46:37 2020

@author: juanj
"""
import CPVClass
import pandas as pd
# AOILIMIT=55.0
# df=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/Datos_filtrados_IIIV.csv',encoding='utf-8')





# filt_df2=df[(df['aoi']<AOILIMIT)]
# filt_x=filt_df2['aoi'].values
# filt_y=filt_df2['ISC_IIIV/DII (A m2/W)'].values

Mi_CPV=CPVClass.CPVSystem(surface_tilt=0, surface_azimuth=180,
                 albedo=None, surface_type=None,
                 module=None, module_type='glass_polymer',
                 module_parameters=None,
                 temperature_model_parameters='open_rack_glass_glass',
                 modules_per_string=1, strings_per_inverter=1,
                 inverter=None, inverter_parameters=None,
                 racking_model='open_rack', losses_parameters=None, name=None,
                 iam_parameters=None)


Mi_CPV.iam_parameters={'a3':-8.315977512579898e-06,'a2':0.00039212250547851236,
                       'a1':-0.006006260890940105,'b':1.0}


Mi_CPV.generate_iam_parameters(filt_regresion['aoi'].values,filt_regresion['ISC_IIIV/DII (A m2/W)'].values)                        
hola=Mi_CPV.get_iam(aoi=[0.0,2.0,10.0,50.0,70.0],iam_model='tercer grado')

# hola=Mi_CPV.get_iam(aoi=[0.0,2.0,10.0,50.0,70.0],iam_model='segundo grado')
