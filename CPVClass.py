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
import pandas as pd
from pvlib import (atmosphere, iam, irradiance)
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

def _combine_localized_attributes(pvsystem=None, location=None, **kwargs):
    """
    Get and combine attributes from the pvsystem and/or location
    with the rest of the kwargs.
    """
    if pvsystem is not None:
        pv_dict = pvsystem.__dict__
    else:
        pv_dict = {}

    if location is not None:
        loc_dict = location.__dict__
    else:
        loc_dict = {}

    new_kwargs = dict(
        list(pv_dict.items()) + list(loc_dict.items()) + list(kwargs.items())
    )
    return new_kwargs

class CPVSystem(object):
    
    
    def __init__(self,
                 surface_tilt=0, surface_azimuth=180,
                 albedo=None, surface_type=None,
                 module=None, module_type='glass_polymer',
                 module_parameters=None,
                 temperature_model_parameters=None,
                 modules_per_string=1, strings_per_inverter=1,
                 inverter=None, inverter_parameters=None,
                 racking_model='open_rack', losses_parameters=None, name=None,
                 iam_parameters=None, aoi_limit=55.0,**kwargs):
                 
                 

        self.surface_tilt = surface_tilt
        self.surface_azimuth = surface_azimuth
        self.surface_type = surface_type

        if albedo is None:
            self.albedo = irradiance.SURFACE_ALBEDOS.get(surface_type, 0.25)
        else:
            self.albedo = albedo

        self.module = module
        if module_parameters is None:
            self.module_parameters = {}
        else:
            self.module_parameters = module_parameters

        self.module_type = module_type
        self.racking_model = racking_model
        
        if temperature_model_parameters is None:
            self.temperature_model_parameters = \
                self._infer_temperature_model_params()
        else:
            self.temperature_model_parameters = temperature_model_parameters

        if not any(self.temperature_model_parameters):
            warnings.warn(
                'Required temperature_model_parameters is not specified '
                'and parameters are not inferred from racking_model and '
                'module_type. Reverting to deprecated default: SAPM cell '
                'temperature model parameters for a glass/glass module in '
                'open racking. In the future '
                'PVSystem.temperature_model_parameters will be required',
                pvlibDeprecationWarning)
            params = temperature._temperature_model_params(
                'sapm', 'open_rack_glass_glass')
            self.temperature_model_parameters = params

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
        if iam_parameters is None:
            self.iam_parameters = {}
        else:
            self.iam_parameters = iam_parameters

    def __repr__(self):
        attrs = ['name', 'surface_tilt', 'surface_azimuth', 'module',
                 'inverter', 'albedo', 'racking_model']
        return ('PVSystem: \n  ' + '\n  '.join(
            ('{}: {}'.format(attr, getattr(self, attr)) for attr in attrs)))
        
    def get_aoi(self, solar_zenith, solar_azimuth):
        """Get the angle of incidence on the system.

        Parameters
        ----------
        solar_zenith : float or Series.
            Solar zenith angle.
        solar_azimuth : float or Series.
            Solar azimuth angle.

        Returns
        -------
        aoi : Series
            The angle of incidence
        """

        aoi = irradiance.aoi(self.surface_tilt, self.surface_azimuth,
                             solar_zenith, solar_azimuth)
        return aoi
    def get_iam(self, aoi,iam_model='tercer grado'):
        
        aoi=np.array(aoi)
        model = iam_model.lower()
        if (model=='primer grado'):
            if (len(self.iam_parameters)==2):           
                return aoi*self.iam_parameters['a1']+self.iam_parameters['b']
            else:
                raise ValueError('the lenth of iam_parameters does not match with the chosen model')
                
        elif model=='segundo grado':
            if len(self.iam_parameters)==3:
       
                return aoi*self.iam_parameters['a2']**2+aoi*self.iam_parameters['a1']+self.iam_parameters['b']
            else:
                raise ValueError('the lenth of iam_parameters does not match with the chosen model')
        elif (model=='tercer grado'):
            if (len(self.iam_parameters)==4):
                return aoi*self.iam_parameters['a3']**3+aoi*self.iam_parameters['a2']**2+aoi*self.iam_parameters['a1']+self.iam_parameters['b']  
            else:
                raise ValueError('the lenth of iam_parameters does not match with the chosen model')
        elif model in ['ashrae', 'physical', 'martin_ruiz']:
            param_names =_IAM_MODEL_PARAMS[model]
            kwargs = _build_kwargs(param_names, self.module_parameters)
            func = getattr(iam, model)
            return func(aoi, **kwargs)
        elif model == 'sapm':
            return iam.sapm(aoi, self.module_parameters)
        elif model == 'interp':
            raise ValueError(model + ' is not implemented as an IAM model'
                             'option for PVSystem')
        else:
            raise ValueError(model + ' is not a valid IAM model')
    def generate_iam_parameters(self, aoi,values,grado=3):
        aoi=np.array(aoi)
        y_,RR,a_s,b=Error.regresion_polinomica(aoi,values,grado)
        if grado==3:
            self.iam_parameters={'a3':a_s[3]/b, 'a2':a_s[2]/b,
                                 'a1':a_s[1]/b,'b':b}
        elif grado==2:
            self.iam_parameters={'a2':a_s[2]/b,'a1':a_s[1]/b,'b':b}            
        elif grado==1:
            self.iam_parameters={'a2':a_s[2]/b,
                                 'a1':a_s[1]/b,'b':b} 
        print('iam_parameters have been generated with an RR of: '+str(RR))
        return a_s,b

    def get_total_irradiance(surface_tilt, surface_azimuth,
                             solar_zenith, solar_azimuth,
                             dni, ghi, dhi, dni_extra=None, airmass=None,
                             albedo=.25, surface_type=None,
                             model='isotropic',
                             model_perez='allsitescomposite1990', **kwargs):
        r"""
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
        poa_sky_diffuse = irradiance.get_sky_diffuse(
            surface_tilt, surface_azimuth, solar_zenith, solar_azimuth,
            dni, ghi, dhi, dni_extra=dni_extra, airmass=airmass, model=model,
            model_perez=model_perez)
    
        poa_ground_diffuse = irradiance.get_ground_diffuse(surface_tilt, ghi, albedo,
                                                surface_type)
        aoi_ = irradiance.aoi(surface_tilt, surface_azimuth, solar_zenith, solar_azimuth)
        irrads = irradiance.poa_components(aoi_, dni, poa_sky_diffuse, poa_ground_diffuse)
        return irrads

      
  
    def calcparams_pvsyst(self, effective_irradiance, temp_cell):
        """
        Use the :py:func:`calcparams_pvsyst` function, the input
        parameters and ``self.module_parameters`` to calculate the
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
                               self.module_parameters)

        return calcparams_pvsyst(effective_irradiance, temp_cell, **kwargs)
    
    
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
                               self.module_parameters)
        kwargs.update(_build_kwargs(['u_c', 'u_v'],
                                    self.temperature_model_parameters))
        return temperature.pvsyst_cell(poa_global, temp_air, wind_speed,
                                       **kwargs)

    def singlediode(self, photocurrent, saturation_current,
                    resistance_series, resistance_shunt, nNsVth,
                    ivcurve_pnts=None):
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
                           ivcurve_pnts=ivcurve_pnts)
    
    
class LocalizedCVSystem(CPVSystem, Location):
    """
    The LocalizedPVSystem class defines a standard set of installed PV
    system attributes and modeling functions. This class combines the
    attributes and methods of the PVSystem and Location classes.

    The LocalizedPVSystem may have bugs due to the difficulty of
    robustly implementing multiple inheritance. See
    :py:class:`~pvlib.modelchain.ModelChain` for an alternative paradigm
    for modeling PV systems at specific locations.
    """

    def __init__(self, pvsystem=None, location=None, **kwargs):

        new_kwargs = _combine_localized_attributes(
            pvsystem=pvsystem,
            location=location,
            **kwargs,
        )

        CPVSystem.__init__(self, **new_kwargs)
        Location.__init__(self, **new_kwargs)


    def __repr__(self):
        attrs = ['name', 'latitude', 'longitude', 'altitude', 'tz',
                 'surface_tilt', 'surface_azimuth', 'module', 'inverter',
                 'albedo', 'racking_model']
        return ('LocalizedPVSystem: \n  ' + '\n  '.join(
            ('{}: {}'.format(attr, getattr(self, attr)) for attr in attrs)))
    
    
    
    
    
    