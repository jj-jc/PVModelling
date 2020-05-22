# -*- coding: utf-8 -*-
"""
Created on Fri May 22 20:09:07 2020

@author: juanj
"""

import pvlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from cpvtopvlib import cpvsystem
import Error as E


df=pd.read_excel('C://Users/juanj/OneDrive/Escritorio/TFG/Curva_IV_Silicio/I-V.csv',encoding='utf-8')

