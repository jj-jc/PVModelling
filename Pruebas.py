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
import numpy as np
# AOILIMIT=55.0
# df=pd.read_csv('C://Users/juanj/OneDrive/Escritorio/TFG/Datos_filtrados_IIIV.csv',encoding='utf-8')

w_am=np.arange(0,1,0.01)
w_temp=np.arange(0,1,0.01)
eleccion=pd.DataFrame(columns=w_am, index=w_temp)


