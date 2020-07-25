# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 20:23:03 2020

@author: juanj
"""

# from pvlib import pvsystem
import Error
from pvlib import atmosphere, irradiance
from pvlib.tools import _build_kwargs
from pvlib.location import Location
import numpy as np
from pvlib import (atmosphere, iam, irradiance,temperature)
from pvlib._deprecation import pvlibDeprecationWarning            
from pvlib import pvsystem
import warnings

# a dict of required parameter names for each IAM model
# keys are the function names for the IAM models
_IAM_MODEL_PARAMS = {
    'ashrae': set(['b']),
    'physical': set(['n', 'K', 'L']),
    'martin_ruiz': set(['a_r']),
    'sapm': set(['B0', 'B1', 'B2', 'B3', 'B4', 'B5']),
    'interp': set([])
}

def _combine_attributes(cpvsystem=None, second_object=None, **kwargs):
    """
    Get and combine attributes from two different objects
    with the rest of the kwargs.
    """
    
    if cpvsystem is not None:    
        cpv_dict = cpvsystem.__dict__
    else:
        cpv_dict = {}
        
    if second_object is not None:
        second_object_dict = second_object.__dict__
    else:
        second_object = {}
        
    new_kwargs = dict(
        list(cpv_dict.items()) + list(second_object_dict.items()) + list(kwargs.items())
    )     
    return new_kwargs
       
class CPVSystem(object):    
    def __init__(self,
                 surface_tilt=0, surface_azimuth=180, 
                 albedo=None, surface_type=None,
                 module=None, 
                 module_CPV_parameters=None,
                 temperature_model_CPV_parameters=None,
                 modules_per_string=1, strings_per_inverter=1,
                 inverter=None, inverter_parameters=None,
                 losses_parameters=None, name=None,
                 iam_CPV_parameters=None, uf_parameters=None,**kwargs):
                 

        self.surface_tilt = surface_tilt
        self.surface_azimuth = surface_azimuth
        self.surface_type=surface_type
        if albedo is None:
            self.albedo = irradiance.SURFACE_ALBEDOS.get(surface_type, 0.25)
        else:
            self.albedo = albedo

        self.module = module
        if module_CPV_parameters is None:
            self.module_CPV_parameters = {}
        else:
            self.module_CPV_parameters = module_CPV_parameters
        if temperature_model_CPV_parameters is None:
            self.temperature_model_CPV_parameters = {}
        else: 
            self.temperature_model_CPV_parameters = temperature_model_CPV_parameters

        self.modules_per_string = modules_per_string
        self.strings_per_inverter = strings_per_inverter

        self.inverter = inverter
        if inverter_parameters is None:
            self.inverter_parameters = {}
        else:
            self.inverter_parameters = inverter_parameters

        if losses_parameters is None:
            self.losses_parameters = {}
        else:
            self.losses_parameters = losses_parameters

        self.name = name
        
        if iam_CPV_parameters is None:
            self.iam_CPV_parameters = {'a3':0,'a2': 0,
                                       'a1':0,'valor_norm':0}
        else:
            self.iam_CPV_parameters = iam_CPV_parameters
            
        if uf_parameters is None:
            self.uf_parameters = {'m1_am':0, 'thld_am':0 ,'m2_am':0,
                                  'm_temp':0, 'thld_temp':0,
                                  'w_am':0,'w_temp': 0}
        else:
            self.uf_parameters = uf_parameters
    def __repr__(self):
        attrs = ['name', 'AOILIMIT', 'surface_tilt', 'surface_azimuth', 'module',
                 'inverter', 'albedo', 'racking_model']
        return ('CPVSystem: \n  ' + '\n  '.join(
            ('{}: {}'.format(attr, getattr(self, attr)) for attr in attrs)))        
    
    
    def get_iam(self, aoi,iam_model='third degree'):
        '''Get the incidence angle modifier from the 
        parameters given and the model type
        
        Parameters
        ----------
        aoi : Series.
            The angle of incidence.
        iam_model : str.
            The model to obtain the iam.

        Returns
        -------
        iam : Series
            The incidence angle modifier
    
        '''
        
        model = iam_model.lower()
        if (model=='first degree'):
            if (len(self.iam_CPV_parameters)==2):           
                return aoi*self.iam_CPV_parameters['a1']+1
            else:
                raise ValueError('the lenth of iam_CPV_parameters does not match with the chosen model')
                
        elif model=='second degree':
            if len(self.iam_CPV_parameters)==3:
       
                return (aoi**2)*self.iam_CPV_parameters['a2']+aoi*self.iam_CPV_parameters['a1']+1
            else:
                raise ValueError('the lenth of iam_CPV_parameters does not match with the chosen model')
        elif (model=='third degree'):
            if (len(self.iam_CPV_parameters)==4):
                return (aoi**3)*self.iam_CPV_parameters['a3']+(aoi**2)*self.iam_CPV_parameters['a2']+aoi*self.iam_CPV_parameters['a1']+1 
            else:
                raise ValueError('the lenth of iam_CPV_parameters does not match with the chosen model')
        elif model in ['ashrae', 'physical', 'martin_ruiz']:
            param_names =_IAM_MODEL_PARAMS[model]
            kwargs = _build_kwargs(param_names, self.module_CPV_parameters)
            func = getattr(iam, model)
            return func(aoi, **kwargs)
        elif model == 'sapm':
            return iam.sapm(aoi, self.module_CPV_parameters)
        elif model == 'interp':
            raise ValueError(model + ' is not implemented as an IAM model'
                             'option for PVSystem')
        else:
            raise ValueError(model + ' is not a valid IAM model')
    
    def generate_iam_parameters(self, aoi,values,grado=3):
        
        '''Get and write the parameters for iam from the 
        values given
        
        Parameters
        ----------
        aoi : Series.
            The angle of incidence.
        values : Series.
            Filtered values to obtain the iam parameters.

        Returns
        -------
        iam : Series
            The incidence angle modifier
    
        '''
               
        aoi=np.array(aoi)
        y_,RR,a_s,b=Error.regresion_polinomica(aoi,values,grado)
        if grado==3:
            self.iam_CPV_parameters={'a3':a_s[3]/b, 'a2':a_s[2]/b,
                                 'a1':a_s[1]/b,'valor_norm':b}
        elif grado==2:
            self.iam_CPV_parameters={'a2':a_s[2]/b,'a1':a_s[1]/b,'valor_norm':b}            
        elif grado==1:
            self.iam_CPV_parameters={'a2':a_s[2]/b,
                                 'a1':a_s[1]/b,'valor_norm':b} 
        # print('iam_CPV_parameters have been generated with an RR of: '+str(RR))
		
        return a_s,b
    
    def get_total_irradiance(self, surface_tilt, surface_azimuth,
                             solar_zenith, solar_azimuth,
                             dni, ghi, dhi, dni_extra=None, airmass=None,
                             albedo=.25, surface_type=None,
                             model='isotropic',
                             model_perez='allsitescomposite1990', **kwargs):
        """
        Determine total in-plane irradiance and its beam, sky diffuse and ground
        reflected components, using the specified sky diffuse irradiance model.   
        .. math::
    
           I_{tot} = I_{beam} + I_{sky diffuse} + I_{ground}
    
        Sky diffuse models include:
            * isotropic (default)
            * klucher
            * haydavies
            * reindl
            * king
            * perez
    
        Parameters
        ----------
        surface_tilt : numeric
            Panel tilt from horizontal.
        surface_azimuth : numeric
            Panel azimuth from north.
        solar_zenith : numeric
            Solar zenith angle.
        solar_azimuth : numeric
            Solar azimuth angle.
        dni : numeric
            Direct Normal Irradiance
        ghi : numeric
            Global horizontal irradiance
        dhi : numeric
            Diffuse horizontal irradiance
        dni_extra : None or numeric, default None
            Extraterrestrial direct normal irradiance
        airmass : None or numeric, default None
            Airmass
        albedo : numeric, default 0.25
            Surface albedo
        surface_type : None or String, default None
            Surface type. See grounddiffuse.
        model : String, default 'isotropic'
            Irradiance model.
        model_perez : String, default 'allsitescomposite1990'
            Used only if model='perez'. See :py:func:`perez`.
    
        Returns
        -------
        total_irrad : OrderedDict or DataFrame
            Contains keys/columns ``'poa_global', 'poa_direct', 'poa_diffuse',
            'poa_sky_diffuse', 'poa_ground_diffuse'``.
        """        
        poa_sky_diffuse = irradiance.get_sky_diffuse(surface_tilt, surface_azimuth, 
                                                     solar_zenith, solar_azimuth, 
                                                     dni, 
                                                     ghi, dhi, dni_extra=dni_extra, 
                                                     airmass=airmass, model=model, model_perez=model_perez)
    
        poa_ground_diffuse = irradiance.get_ground_diffuse(surface_tilt, 
                                                           ghi, albedo,
                                                           surface_type)
        aoi_ = irradiance.aoi(surface_tilt, surface_azimuth,
                              solar_zenith, solar_azimuth)
        irrads = irradiance.poa_components(aoi_, dni, poa_sky_diffuse, poa_ground_diffuse)
        return irrads
    def calcparams_cpvsyst(self, effective_irradiance, temp_cell):
        """
        Use the :py:func:`calcparams_pvsyst` function, the input
        parameters and ``self.module_CPV_parameters`` to calculate the
        module currents and resistances.

        Parameters
        ----------
        effective_irradiance : numeric
            The irradiance (W/m2) that is converted to photocurrent.

        temp_cell : float or Series
            The average cell temperature of cells within a module in C.

        Returns
        -------
        See pvsystem.calcparams_pvsyst for details
        """

        kwargs = _build_kwargs(['gamma_ref', 'mu_gamma', 'I_L_ref', 'I_o_ref',
                                'R_sh_ref', 'R_sh_0', 'R_sh_exp',
                                'R_s', 'alpha_sc', 'EgRef',
                                'irrad_ref', 'temp_ref',
                                'cells_in_series'],
                               self.module_CPV_parameters)

        return pvsystem.calcparams_pvsyst(effective_irradiance, temp_cell, **kwargs)
    def pvsyst_celltemp(self, poa_global, temp_air, wind_speed=1.0):
        """
        Uses :py:func:`pvsystem.pvsyst_celltemp` to calculate module
        temperatures based on ``self.racking_model`` and the input parameters.

        Parameters
        ----------
        See pvsystem.pvsyst_celltemp for details

        Returns
        -------
        See pvsystem.pvsyst_celltemp for details
        """

        kwargs = _build_kwargs(['eta_m', 'alpha_absorption'],
                               self.module_CPV_parameters)
        kwargs.update(_build_kwargs(['u_c', 'u_v'],
                                    self.temperature_model_CPV_parameters))
        return temperature.pvsyst_cell(poa_global, temp_air, wind_speed,
                                       **kwargs)
    def singlediode(self, photocurrent, saturation_current,
                    resistance_series, resistance_shunt, nNsVth,
                    ivcurve_pnts=None,method='lambertw'):
        """Wrapper around the :py:func:`singlediode` function.

        Parameters
        ----------
        See pvsystem.singlediode for details

        Returns
        -------
        See pvsystem.singlediode for details
        """
        return pvsystem.singlediode(photocurrent, saturation_current,
                           resistance_series, resistance_shunt, nNsVth,
                           ivcurve_pnts=ivcurve_pnts,method=method)

    def get_uf(self, airmass, temperature):
        '''Get the utilization factors from the params given
        
        Parameters
        ----------
        arimass: Series.
        In order to obtain the airmass utilization factor.
        temperature: Series.
        In order to obtain the temperature utilization factor.

        Returns
        -------
        UF: Series.
        The result of aplying the utilization factors model 
        '''
        if (len(airmass)==len(temperature)):
            UF_am=np.array(self.get_uf_am(airmass))
            UF_temp=np.array(self.get_uf_temp(temperature))
            UF=np.array(UF_am+UF_temp)
            return (UF)
        else: 
            raise ValueError('The lenth of the values do not match')

    def get_uf_am(self,airmass):
        '''Get the airmass utilization factors from the params given
        
        Parameters
        ----------
        arimass: Series.
        In order to obtain the airmass utilization factor.

        Returns
        -------
        UF_am: Series.
        The result of aplying the airmass utilization factor model.
        '''
        thld_am=self.uf_parameters['thld_am']
        a_am_low=self.uf_parameters['m1_am']
        a_am_high=self.uf_parameters['m2_am']
        w_am=self.uf_parameters['w_am']
        UF_am=[]
        for i in range(len(airmass)):
            if airmass[i]<=thld_am:
                aux=(1 + ( airmass[i]- thld_am) * (a_am_low))
                if aux>1:                    
                    UF_am.append(1)
                else: 
                    UF_am.append(aux)
            else:
                UF_am.append(1 + ( airmass[i]- thld_am) * (a_am_high))
        UF_am=np.array(UF_am)
        UF_am=UF_am*w_am
        return UF_am
    
    def get_uf_temp(self, temperature):
        '''Get the temperature utilization factors from the params given
        
        Parameters
        ----------
        temperature: Series.
        In order to obtain the temperature utilization factor.

        Returns
        -------
        UF_temp: Series.
        The result of aplying the temperature utilization factor model.
        '''
        a_temp=self.uf_parameters['m_temp']
        thld_temp=self.uf_parameters['thld_temp']
        w_temp=self.uf_parameters['w_temp']
        UF_temp=w_temp*(1 + (temperature - thld_temp) * (a_temp))
        return UF_temp
         
    def generate_uf_am_parameters(self,airmass,values):
        '''Note: It is absolutely necessary that iam_CPV_parameters['valor_norm'] 
        has a value, in order to be able to normalize the values given this value 
        can be produced by generate_iam_parameters and the model choosen
        
        Generate the params for the airmas utilization factor model 
        from the values given.
        
        Parameters
        ----------
        airmass: Series.
        In order to obtain the airmass utilization factor.
        values: Series.
        Values used to obtain the parameters for the airmass utilization factors
        
        Returns
        -------
        No returns.
        '''       
    
        RR_max=-1
        thlds=np.arange(airmass.min(),airmass.max(),0.001)       
        for j in thlds:
            RR_max_high=-1
            airmass_low=airmass[airmass<=j]
            values_low=(values[airmass<=j])/(self.iam_CPV_parameters['valor_norm'])
            
            airmass_high=airmass[airmass>j]
            values_high=values[airmass>j]/(self.iam_CPV_parameters['valor_norm'])
                      
            yr_low, RR_low, a_s_low, b_low=Error.regresion_polinomica(airmass_low, values_low, 1)
            y_max=float(yr_low[np.where(yr_low==yr_low.max())])
            

            x_desplazado=airmass_high-j
            
            #y_regresion=mx+b donde la b=y_max
            m=np.arange(-1,-0.001,0.001)
            # yr_high=pd.DataFrame({'x_desplazado': x_desplazado})
            for i in range(len(m)):
                yr_high=x_desplazado*m[i]+y_max                
                RR_high=Error.Determination_coefficient(values_high,yr_high)  
               
                if RR_max_high < RR_high:
                    RR_max_high=RR_high           
                    y=np.concatenate((values_low,values_high))
                    y_regre=np.concatenate((yr_low,yr_high))
                    RR=Error.Determination_coefficient(y,y_regre)
                    if RR_max < RR:
                        RR_max=RR
                        self.uf_parameters['m1_am']=a_s_low[1]
                        self.uf_parameters['m2_am']=m[i]
                        self.uf_parameters['thld_am']=j
                
    def generate_uf_temp_parameters(self,temperature,values): 
        '''Note: It is absolutely necessary that iam_CPV_parameters['valor_norm'] 
        has a value, in order to be able to normalize the values given this value 
        can be produced by generate_iam_parameters and the model choosen
        
        Generate the params for the airmas utilization factor model 
        from the values given.
        
        Parameters
        ----------
        temperature: Series.
        In order to obtain the temperature utilization factor.
        values: Series.
        Values used to obtain the parameters for the temperature utilization factors.
        
        Returns
        -------
        No returns.
        '''             
        values=values/self.iam_CPV_parameters['valor_norm']
        y1_regre,RR_temp,a_s,b=Error.regresion_polinomica(temperature,values,1)
        self.uf_parameters['m_temp']=a_s[1]
        self.uf_parameters['thld_temp']=temperature[np.where(y1_regre==y1_regre.max())][0]
        
    def generate_uf_parameters(self, airmass, values_airmass, temperature, values_temperature):
        '''Note: It is absolutely necessary that iam_CPV_parameters['valor_norm'] 
        has a value, in order to be able to normalize the values given this value 
        can be produced by generate_iam_parameters and the model choosen.
        
        Generate the params for the utilization factor model 
        from the values given.
        
        Parameters
        ----------
        airmass: Series.
        In order to obtain the airmass utilization factor.
        values_airmass: Series.
        Values used to obtain the parameters for the airmass utilization factors
        temperature: Series.
        In order to obtain the temperature utilization factor.
        values_temperature: Series.
        Values used to obtain the parameters for the temperature utilization factors.
        
        Returns
        -------
        No returns.
        '''          
        self.generate_uf_am_parameters(airmass, values_airmass)
        self.generate_uf_temp_parameters(temperature, values_temperature)

    def calculate_uf(self, airmass, temperature, PMP_calculated=None, PMP=None):  
        '''Choose the best weights from the values of PMP given for the utilization factor model.
        
        Parameters
        ----------
        airmass: Series.
        temperature: Series.
        PMP_calculated: Series.
        Estimation of the PMP values.
        PMP: Series.
        The values of Maximum Power Point used to choose the weights for the utilization factor model.      
        
        Returns
        -------
        Series.
        The utilization factor calculated.
        '''
        UF_am=[]
        for i in range(len(airmass)):
            if airmass[i]<=self.uf_parameters['thld_am']:
                aux=1 + ( airmass[i]- self.uf_parameters['thld_am']) * (self.uf_parameters['m1_am'])
                if (aux>1):
                    UF_am.append(1)
                else:
                    UF_am.append(aux)
            else:
                UF_am.append(1 + ( airmass[i]- self.uf_parameters['thld_am']) * (self.uf_parameters['m2_am']))
        UF_am=np.array(UF_am)
        
        
        UF_temp=[]
        for i in range(len(temperature)):
            if temperature[i]>self.uf_parameters['thld_temp']:
                UF_temp.append(1 + ( temperature[i]- self.uf_parameters['thld_temp']) * (self.uf_parameters['m_temp']))
            else:
                UF_temp.append(1)
        UF_temp=np.array(UF_temp)
        
        if ((self.uf_parameters['w_am']==0) & (self.uf_parameters['w_temp']==0)):
            w_am=np.arange(0,1,0.001)
            w_temp=np.arange(0,1,0.001)       
            best_RMSE=1000
            best_w_am=0
            best_w_temp=0
            for i in w_am:
                for j in w_temp:
                    if ((i+j)<=1):
                        UF_total=i*UF_am+j*UF_temp 
                        estimacion=PMP_calculated*UF_total
                        RMSE=Error.RMSE(PMP,estimacion) 
                        if (best_RMSE>=RMSE):
                            best_RMSE=RMSE		                             				             
                            best_w_am=i
                            best_w_temp=j
            print('the weights have been calculated with an error of: '+str(best_RMSE) )
            self.uf_parameters['w_temp']=best_w_temp
            self.uf_parameters['w_am']=best_w_am 
        return (self.uf_parameters['w_am']*UF_am+self.uf_parameters['w_temp']*UF_temp)          
    
    def scale_voltage_current_power(self, data):
        """
        Scales the voltage, current, and power of the DataFrames
        returned by :py:func:`singlediode` and :py:func:`sapm`
        by `self.modules_per_string` and `self.strings_per_inverter`.

        Parameters
        ----------
        data: DataFrame
            Must contain columns `'v_mp', 'v_oc', 'i_mp' ,'i_x', 'i_xx',
            'i_sc', 'p_mp'`.

        Returns
        -------
        scaled_data: DataFrame
            A scaled copy of the input data.
        """

        return pvsystem.scale_voltage_current_power(data,
                                           voltage=self.modules_per_string,
                                           current=self.strings_per_inverter)
    
    def pvwatts_dc(self, g_poa_effective, temp_cell):
        """
        Calcuates DC power according to the PVWatts model using
        :py:func:`pvwatts_dc`, `self.module_CPV_parameters['pdc0']`, and
        `self.module_CPV_parameters['gamma_pdc']`.

        See :py:func:`pvwatts_dc` for details.
        """
        kwargs = _build_kwargs(['temp_ref'], self.module_CPV_parameters)

        return pvsystem.pvwatts_dc(g_poa_effective, temp_cell,
                          self.module_CPV_parameters['pdc0'],
                          self.module_CPV_parameters['gamma_pdc'],
                          **kwargs)

    def pvwatts_losses(self):
        """
        Calculates DC power losses according the PVwatts model using
        :py:func:`pvwatts_losses` and ``self.losses_parameters``.`

        See :py:func:`pvwatts_losses` for details.
        """
        kwargs = _build_kwargs(['soiling', 'shading', 'snow', 'mismatch',
                                'wiring', 'connections', 'lid',
                                'nameplate_rating', 'age', 'availability'],
                               self.losses_parameters)
        return pvsystem.pvwatts_losses(**kwargs)

    def pvwatts_ac(self, pdc):
        """
        Calculates AC power according to the PVWatts model using
        :py:func:`pvwatts_ac`, `self.module_CPV_parameters['pdc0']`, and
        `eta_inv_nom=self.inverter_parameters['eta_inv_nom']`.

        See :py:func:`pvwatts_ac` for details.
        """
        kwargs = _build_kwargs(['eta_inv_nom', 'eta_inv_ref'],
                               self.inverter_parameters)

        return pvsystem.pvwatts_ac(pdc, self.inverter_parameters['pdc0'], **kwargs)


class LocalizedCPVSystem(CPVSystem, Location):
    '''
    The LocalizedCPVSystem class defines a standard set of installed CPV
    system attributes and modeling functions. This class combines the
    attributes and methods of the CPVSystem and Location classes.
    '''
    def __init__(self, cpvsystem=None, second_object=None, **kwargs):

        new_kwargs = _combine_attributes(
            cpvsystem=cpvsystem,
            second_object=second_object,
            **kwargs,
        )

        CPVSystem.__init__(self, **new_kwargs)
        Location.__init__(self, **new_kwargs)


    def __repr__(self):
        attrs = ['name','AOILIMIT' ,'latitude', 'longitude', 'altitude', 'tz',
                 'surface_tilt', 'surface_azimuth', 'module', 'inverter',
                 'albedo', 'racking_model']
        return ('LocalizedCPVSystem: \n  ' + '\n  '.join(
            ('{}: {}'.format(attr, getattr(self, attr)) for attr in attrs)))

class Flat_CPVSystem (object):
    def __init__(self,
                 surface_tilt=0, surface_azimuth=180, 
                 albedo=None, surface_type=None,
                 module=None, 
                 module_Flat_parameters=None,
                 temperature_model_Flat_parameters=None,
                 modules_per_string=1, strings_per_inverter=1,
                 inverter=None, inverter_parameters=None, 
                 losses_parameters=None, name=None,
                 iam_Flat_parameters=None, uf_parameters=None,**kwargs):
                 
        self.surface_tilt = surface_tilt
        self.surface_azimuth = surface_azimuth
        self.surface_type=surface_type,
        if albedo is None:
            self.albedo = irradiance.SURFACE_ALBEDOS.get(surface_type, 0.25)
        else:
            self.albedo = albedo

        self.module = module
        if module_Flat_parameters is None:
            self.module_Flat_parameters = {}
        else:
            self.module_Flat_parameters = module_Flat_parameters

        if temperature_model_Flat_parameters is None:
            self.temperature_model_Flat_parameters = {}
        else: 
            self.temperature_model_Flat_parameters = temperature_model_Flat_parameters

        self.modules_per_string = modules_per_string
        self.strings_per_inverter = strings_per_inverter

        self.inverter = inverter
        if inverter_parameters is None:
            self.inverter_parameters = {}
        else:
            self.inverter_parameters = inverter_parameters

        if losses_parameters is None:
            self.losses_parameters = {}
        else:
            self.losses_parameters = losses_parameters

        self.name = name
        
        if iam_Flat_parameters is None:
            self.iam_Flat_parameters = {}
        else:
            self.iam_Flat_parameters = iam_Flat_parameters
        
    def __repr__(self):
        attrs = ['name', 'AOILIMIT', 'surface_tilt', 'surface_azimuth', 'module',
                  'inverter', 'albedo' ]
        # ''', 'racking_model''']
        return ('Si_CPVSystem: \n  ' + '\n  '.join(
            ('{}: {}'.format(attr, getattr(self, attr)) for attr in attrs)))
    
    def calcparams_pvsyst(self, effective_irradiance, temp_cell):
        """
        Use the :py:func:`calcparams_pvsyst` function, the input
        parameters and ``self.module_Flat_parameters`` to calculate the
        module currents and resistances.
    
        Parameters
        ----------
        effective_irradiance : numeric
            The irradiance (W/m2) that is converted to photocurrent.
    
        temp_cell : float or Series
            The average cell temperature of cells within a module in C.
    
        Returns
        -------
        See pvsystem.calcparams_pvsyst for details
        """
    
        kwargs = _build_kwargs(['gamma_ref', 'mu_gamma', 'I_L_ref', 'I_o_ref',
                                'R_sh_ref', 'R_sh_0', 'R_sh_exp',
                                'R_s', 'alpha_sc', 'EgRef',
                                'irrad_ref', 'temp_ref',
                                'cells_in_series'],
                                self.module_Flat_parameters)
    
        return pvsystem.calcparams_pvsyst(effective_irradiance, temp_cell, **kwargs)
   
        
    def get_iam(self, aoi,iam_model='third degree'):
        '''Get the incidence angle modifier from the 
        parameters given and the model type
        
        Parameters
        ----------
        aoi : Series.
            The angle of incidence.
        iam_model : str.
            The model to obtain the iam.

        Returns
        -------
        iam : Series
            The incidence angle modifier
    
        '''       
        model = iam_model.lower()
        if (model=='first degree'):
            if (len(self.iam_Flat_parameters)==3):           
                return aoi*self.iam_Flat_parameters['a1']+self.iam_Flat_parameters['b']
            else:
                raise ValueError('the lenth of iam_Flat_parameters does not match with the chosen model')
                
        elif model=='second degree':
            if len(self.iam_Flat_parameters)==4:
       
                return (aoi**2)*self.iam_Flat_parameters['a2']+aoi*self.iam_Flat_parameters['a1']+self.iam_Flat_parameters['b']
            else:
                raise ValueError('the lenth of iam_Flat_parameters does not match with the chosen model')
        elif (model=='third degree'):
            if (len(self.iam_Flat_parameters)==5):
                return (aoi**3)*self.iam_Flat_parameters['a3']+(aoi**2)*self.iam_Flat_parameters['a2']+aoi*self.iam_Flat_parameters['a1']+self.iam_Flat_parameters['b']
            else:
                raise ValueError('the lenth of iam_Flat_parameters does not match with the chosen model')
                #Estas sentencias evaluavan los tres procedimientos actuales para obtener el iam, pero la parte de Silicio del sistema que queremos modelar
                #no se comporta como definen estas funciones, salvo la physical que sería capaz de modelarlo.
        # elif model in ['ashrae', 'physical', 'martin_ruiz']:
        #     param_names =_IAM_MODEL_PARAMS[model]
        #     kwargs = _build_kwargs(param_names, self.module_Flat_parameters)
        #     func = getattr(iam, model)
        #     return func(aoi, **kwargs)
        # elif model == 'sapm':
        #     return iam.sapm(aoi, self.module_Flat_parameters)
        # elif model == 'interp':
        #     raise ValueError(model + ' is not implemented as an IAM model'
        #                      'option for PVSystem')
        else:
            raise ValueError(model + ' is not a valid IAM model')
        

           
    def generate_iam_parameters(self, aoi_smaller,aoi_greater,values_smaller, values_greater,grado=3):
        
        '''Get and write the parameters for iam from the 
        values given
        
        Parameters
        ----------
        aoi_smaller : Series.
            The angle of incidence values under AOILIMIT
        aoi_greater : Series.
            The angle of incidence values greater than AOILIMIT
            
        values : Series.
            Filtered values to obtain the iam parameters.

        Returns
        -------
        iam : Series
            The incidence angle modifier
    
        '''
        aoi_smaller=np.array(aoi_smaller)
        aoi_greater=np.array(aoi_greater)
        y_,RR,a_s,b=Error.regresion_polinomica(aoi_smaller,values_smaller,grado)
        y__,RR__,a_s__,b_=Error.regresion_polinomica(aoi_greater,values_greater,2)

        if grado==3:
            self.iam_Flat_parameters={'a3':a_s[3]/b_, 'a2':a_s[2]/b_,
                                  'a1':a_s[1]/b_,'valor_norm':b/b_}
        elif grado==2:
            self.iam_Flat_parameters={'a2':a_s[2]/b_,'a1':a_s[1]/b_,'valor_norm':b/b_}            
        elif grado==1:
            self.iam_Flat_parameters={'a2':a_s[2]/b,
                                  'a1':a_s[1]/b,'valor_norm':b} 
        print('iam_Flat_parameters have been generated with an RR of: '+str(RR))
        return a_s,b


        
    def pvsyst_celltemp(self, poa_global, temp_air, wind_speed=1.0):
        """
        Uses :py:func:`pvsystem.pvsyst_celltemp` to calculate module
        temperatures based on ``self.racking_model`` and the input parameters.

        Parameters
        ----------
        See pvsystem.pvsyst_celltemp for details

        Returns
        -------
        See pvsystem.pvsyst_celltemp for details
        """

        kwargs = _build_kwargs(['eta_m', 'alpha_absorption'],
                                self.module_Flat_parameters)
        kwargs.update(_build_kwargs(['u_c', 'u_v'],
                                    self.temperature_model_Flat_parameters))
        return temperature.pvsyst_cell(poa_global, temp_air, wind_speed,
                                        **kwargs)
    def singlediode(self, photocurrent, saturation_current,
                    resistance_series, resistance_shunt, nNsVth,
                    ivcurve_pnts=None,method='lambertw'):
        """Wrapper around the :py:func:`singlediode` function.

        Parameters
        ----------
        See pvsystem.singlediode for details

        Returns
        -------
        See pvsystem.singlediode for details
        """
        return pvsystem.singlediode(photocurrent, saturation_current,
                            resistance_series, resistance_shunt, nNsVth,
                            ivcurve_pnts=ivcurve_pnts,method=method)
    def scale_voltage_current_power(self, data):
        """
        Scales the voltage, current, and power of the DataFrames
        returned by :py:func:`singlediode` and :py:func:`sapm`
        by `self.modules_per_string` and `self.strings_per_inverter`.

        Parameters
        ----------
        data: DataFrame
            Must contain columns `'v_mp', 'v_oc', 'i_mp' ,'i_x', 'i_xx',
            'i_sc', 'p_mp'`.

        Returns
        -------
        scaled_data: DataFrame
            A scaled copy of the input data.
        """

        return pvsystem.scale_voltage_current_power(data,
                                           voltage=self.modules_per_string,
                                           current=self.strings_per_inverter)
    
    def pvwatts_dc(self, g_poa_effective, temp_cell):
        """
        Calcuates DC power according to the PVWatts model using
        :py:func:`pvwatts_dc`, `self.module_CPV_parameters['pdc0']`, and
        `self.module_CPV_parameters['gamma_pdc']`.

        See :py:func:`pvwatts_dc` for details.
        """
        kwargs = _build_kwargs(['temp_ref'], self.module_CPV_parameters)

        return pvsystem.pvwatts_dc(g_poa_effective, temp_cell,
                          self.module_CPV_parameters['pdc0'],
                          self.module_CPV_parameters['gamma_pdc'],
                          **kwargs)

    def pvwatts_losses(self):
        """
        Calculates DC power losses according the PVwatts model using
        :py:func:`pvwatts_losses` and ``self.losses_parameters``.`

        See :py:func:`pvwatts_losses` for details.
        """
        kwargs = _build_kwargs(['soiling', 'shading', 'snow', 'mismatch',
                                'wiring', 'connections', 'lid',
                                'nameplate_rating', 'age', 'availability'],
                               self.losses_parameters)
        return pvsystem.pvwatts_losses(**kwargs)

    def pvwatts_ac(self, pdc):
        """
        Calculates AC power according to the PVWatts model using
        :py:func:`pvwatts_ac`, `self.module_CPV_parameters['pdc0']`, and
        `eta_inv_nom=self.inverter_parameters['eta_inv_nom']`.

        See :py:func:`pvwatts_ac` for details.
        """
        kwargs = _build_kwargs(['eta_inv_nom', 'eta_inv_ref'],
                               self.inverter_parameters)

        return pvsystem.pvwatts_ac(pdc, self.inverter_parameters['pdc0'], **kwargs)



class LocalizedFlat_CPVSystem(Flat_CPVSystem, Location):
    """
    The LocalizedFlatSystem class defines a standard set of installed Flat
    system attributes and modeling functions. This class combines the
    attributes and methods of the PVSystem and Location classes.

    The LocalizedPVSystem may have bugs due to the difficulty of
    robustly implementing multiple inheritance. See
    :py:class:`~pvlib.modelchain.ModelChain` for an alternative paradigm
    for modeling PV systems at specific locations.
    """

    def __init__(self, cpvsystem=None, second_object=None, **kwargs):

        new_kwargs = _combine_attributes(
            cpvsystem=cpvsystem,
            second_object=second_object,
            **kwargs,
        )

        Flat_CPVSystem.__init__(self, **new_kwargs)
        Location.__init__(self, **new_kwargs)


    def __repr__(self):
        attrs = ['name','AOILIMIT' ,'latitude', 'longitude', 'altitude', 'tz',
                 'surface_tilt', 'surface_azimuth', 'module', 'inverter',
                 'albedo']
        return ('LocalizedCPVSystem: \n  ' + '\n  '.join(
            ('{}: {}'.format(attr, getattr(self, attr)) for attr in attrs)))




class HybridSystem(CPVSystem,Flat_CPVSystem):
    '''It represents 
    '''
    
    
    
    def __init__(self, cpvsystem=None, second_object=None,AOILIMIT=55.0, **kwargs):
        if (AOILIMIT <=0.0 or AOILIMIT >90.0):
            self.AOILIMIT=55.0              
        else:
            self.AOILIMIT=AOILIMIT

        new_kwargs = _combine_attributes(
            cpvsystem=cpvsystem,
            second_object=second_object,
            **kwargs,
        )
        CPVSystem.__init__(self, **new_kwargs)
        Flat_CPVSystem.__init__(self, **new_kwargs)

    def __repr__(self):
        attrs = ['name', 'AOILIMIT', 'surface_tilt', 'surface_azimuth', 'module',
                  'inverter', 'albedo' ]
        # ''', 'racking_model''']
        return ('HybridSystem: \n  ' + '\n  '.join(
            ('{}: {}'.format(attr, getattr(self, attr)) for attr in attrs)))
    
    def get_iam(self, aoi,iam_model='third degree'):
        
        iam=[]
        for i in range(len(aoi)):
            if aoi[i]>self.AOILIMIT:
                iam.append(Flat_CPVSystem.get_iam(aoi[i], iam_model))
            else:
                iam.append(CPVSystem.get_iam(aoi[i], iam_model))
        return iam
    
    def get_iam(self, aoi,iam_model='third degree'):
        iam=[]
        for i in range(len(aoi)):
            if aoi[i]>self.AOILIMIT:
                iam.append(Flat_CPVSystem.get_iam(aoi[i], iam_model))
            else:
                iam.append(CPVSystem.get_iam(aoi[i], iam_model))
        return iam
    
    
    def generate_iam_parameters(self, aoi,values_CPV,values_falt,grado=3):
        aoi_smaller=[]
        values_CPV_smaller=[]
        values_Flat_smaller=[]

        aoi_greater=[]
        values_Flat_greater=[]
        for i in range(len(aoi)):
            if aoi[i]>self.AOILIMIT:
                aoi_greater.append(aoi[i])
                values_Flat_greater.append(values_falt[i])
            else:
                aoi_smaller.append(aoi[i])
                values_CPV_smaller.append(values_CPV[i])
                values_Flat_smaller.append(values_falt[i])
                
        Flat_CPVSystem.generate_iam_parameters(self,aoi_smaller,aoi_greater,values_Flat_smaller,values_Flat_greater,grado=grado)
        CPVSystem.generate_iam_parameters(self, aoi_smaller,values_CPV_smaller,grado=grado)
                
        
        
    
    
class LocalizedHybridSystem(HybridSystem, Location):
    
   
    '''
    The LocalizedHybridSystem class defines a standard set of installed Hybrid
    system attributes and modeling functions. This class combines the
    attributes and methods of the HybridSystem and Location classes.
    '''


    def __init__(self, cpvsystem=None, second_object=None, **kwargs):

        new_kwargs = _combine_attributes(
            cpvsystem=cpvsystem,
            second_object=second_object,
            **kwargs,
        )

        HybridSystem.__init__(self, **new_kwargs)
        Location.__init__(self, **new_kwargs)
        


    def __repr__(self):
        attrs = ['name','AOILIMIT' ,'latitude', 'longitude', 'altitude', 'tz',
                 'surface_tilt', 'surface_azimuth', 'module', 'inverter',
                 'albedo']
        return ('LocalizedHybridSystem: \n  ' + '\n  '.join(
            ('{}: {}'.format(attr, getattr(self, attr)) for attr in attrs)))  
    
    
    
    
    
    
    
    
    
    