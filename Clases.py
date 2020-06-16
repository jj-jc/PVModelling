# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 17:40:17 2020

@author: juanj
"""
"""
The ``HybridSystem`` module contains functions for modeling the output and
performance of PV modules and inverters.
"""


import numpy as np
import math
import pandas as pd

from pvlib import pvsystem
from pvlib import atmosphere, irradiance
from pvlib.tools import _build_kwargs
from pvlib.location import Location

class HybridSystem(object):
    """
    The HybridSystem class defines a standard set of hybrid system attributes
    and modeling functions. This class describes the collection and
    interactions of hybrid system components.

    It is typically used in combination with
    CPVSystems
    PVSystems
    objects.

    The class supports basic system topologies consisting of:

        * `N` total modules arranged in series
          (`modules_per_string=N`, `strings_per_inverter=1`).
        * `M` total modules arranged in parallel
          (`modules_per_string=1`, `strings_per_inverter=M`).
        * `NxM` total modules arranged in `M` strings of `N` modules each
          (`modules_per_string=N`, `strings_per_inverter=M`).

    The class is complementary to the module-level functions.

    The attributes should generally be things that don't change about
    the system, such the type of module and the inverter. The instance
    methods accept arguments for things that do change, such as
    irradiance and temperature.

    Parameters
    ----------

    
    surface_tilt: float or array-like, default 0
        Surface tilt angles in decimal degrees.
        The tilt angle is defined as degrees from horizontal
        (e.g. surface facing up = 0, surface facing horizon = 90)

    surface_azimuth: float or array-like, default 180
        Azimuth angle of the module surface.
        North=0, East=90, South=180, West=270.

    albedo : None or float, default None
        The ground albedo. If ``None``, will attempt to use
        ``surface_type`` and ``irradiance.SURFACE_ALBEDOS``
        to lookup albedo.

    surface_type : None or string, default None
        The ground surface type. See ``irradiance.SURFACE_ALBEDOS``
        for valid values.

    module : None or string, default None
        The model name of the modules.
        May be used to look up the module_parameters dictionary
        via some other method.

    module_type : None or string, default 'glass_polymer'
         Describes the module's construction. Valid strings are 'glass_polymer'
         and 'glass_glass'. Used for cell and module temperature calculations.

    module_parameters : None, dict or Series, default None
        Module parameters as defined by the SAPM, CEC, or other.

    temperature_model_parameters : None, dict or Series, default None.
        Temperature model parameters as defined by the SAPM, Pvsyst, or other.

    modules_per_string: int or float, default 1
        See system topology discussion above.

    strings_per_inverter: int or float, default 1
        See system topology discussion above.

    inverter : None or string, default None
        The model name of the inverters.
        May be used to look up the inverter_parameters dictionary
        via some other method.

    inverter_parameters : None, dict or Series, default None
        Inverter parameters as defined by the SAPM, CEC, or other.

    racking_model : None or string, default 'open_rack'
        Valid strings are 'open_rack', 'close_mount', and 'insulated_back'.
        Used to identify a parameter set for the SAPM cell temperature model.

    losses_parameters : None, dict or Series, default None
        Losses parameters as defined by PVWatts or other.

    name : None or string, default None

    **kwargs
        Arbitrary keyword arguments.
        Included for compatibility, but not used.

    See also
    --------
    pvlib.location.Location
    pvlib.tracking.SingleAxisTracker
    pvlib.pvsystem.LocalizedPVSystem
    """
    
    
class PVSystem(object):
    """
    The PVSystem class defines a standard set of PV system attributes
    and modeling functions. This class describes the collection and
    interactions of PV system components rather than an installed system
    on the ground. It is typically used in combination with
    :py:class:`~pvlib.location.Location` and
    :py:class:`~pvlib.modelchain.ModelChain`
    objects.

    See the :py:class:`LocalizedPVSystem` class for an object model that
    describes an installed PV system.

    The class supports basic system topologies consisting of:

        * `N` total modules arranged in series
          (`modules_per_string=N`, `strings_per_inverter=1`).
        * `M` total modules arranged in parallel
          (`modules_per_string=1`, `strings_per_inverter=M`).
        * `NxM` total modules arranged in `M` strings of `N` modules each
          (`modules_per_string=N`, `strings_per_inverter=M`).

    The class is complementary to the module-level functions.

    The attributes should generally be things that don't change about
    the system, such the type of module and the inverter. The instance
    methods accept arguments for things that do change, such as
    irradiance and temperature.

    Parameters
    ----------
    surface_tilt: float or array-like, default 0
        Surface tilt angles in decimal degrees.
        The tilt angle is defined as degrees from horizontal
        (e.g. surface facing up = 0, surface facing horizon = 90)

    surface_azimuth: float or array-like, default 180
        Azimuth angle of the module surface.
        North=0, East=90, South=180, West=270.

    albedo : None or float, default None
        The ground albedo. If ``None``, will attempt to use
        ``surface_type`` and ``irradiance.SURFACE_ALBEDOS``
        to lookup albedo.

    surface_type : None or string, default None
        The ground surface type. See ``irradiance.SURFACE_ALBEDOS``
        for valid values.

    module : None or string, default None
        The model name of the modules.
        May be used to look up the module_parameters dictionary
        via some other method.

    module_type : None or string, default 'glass_polymer'
         Describes the module's construction. Valid strings are 'glass_polymer'
         and 'glass_glass'. Used for cell and module temperature calculations.

    module_parameters : None, dict or Series, default None
        Module parameters as defined by the SAPM, CEC, or other.

    temperature_model_parameters : None, dict or Series, default None.
        Temperature model parameters as defined by the SAPM, Pvsyst, or other.

    modules_per_string: int or float, default 1
        See system topology discussion above.

    strings_per_inverter: int or float, default 1
        See system topology discussion above.

    inverter : None or string, default None
        The model name of the inverters.
        May be used to look up the inverter_parameters dictionary
        via some other method.

    inverter_parameters : None, dict or Series, default None
        Inverter parameters as defined by the SAPM, CEC, or other.

    racking_model : None or string, default 'open_rack'
        Valid strings are 'open_rack', 'close_mount', and 'insulated_back'.
        Used to identify a parameter set for the SAPM cell temperature model.

    losses_parameters : None, dict or Series, default None
        Losses parameters as defined by PVWatts or other.

    name : None or string, default None

    **kwargs
        Arbitrary keyword arguments.
        Included for compatibility, but not used.

    See also
    --------
    pvlib.location.Location
    pvlib.tracking.SingleAxisTracker
    pvlib.pvsystem.LocalizedPVSystem
    """


    def __init__(self,
                 surface_tilt=0, surface_azimuth=180,
                 albedo=None, surface_type=None,
                 module=None, module_type='glass_polymer',
                 module_parameters=None,
                 temperature_model_parameters=None,
                 modules_per_string=1, strings_per_inverter=1,
                 inverter=None, inverter_parameters=None,
                 racking_model='open_rack', losses_parameters=None, name=None,
                 **kwargs):

        self.surface_tilt = surface_tilt
        self.surface_azimuth = surface_azimuth

        # could tie these together with @property
        self.surface_type = surface_type
        if albedo is None:
            self.albedo = irradiance.SURFACE_ALBEDOS.get(surface_type, 0.25)
        else:
            self.albedo = albedo

        # could tie these together with @property
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
            # TODO: in v0.8 check if an empty dict is returned and raise error
        else:
            self.temperature_model_parameters = temperature_model_parameters

        # TODO: deprecated behavior if PVSystem.temperature_model_parameters
        # are not specified. Remove in v0.8
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


    def __repr__(self):
        attrs = ['name', 'surface_tilt', 'surface_azimuth', 'module',
                 'inverter', 'albedo', 'racking_model']
        return ('PVSystem: \n  ' + '\n  '.join(
            ('{}: {}'.format(attr, getattr(self, attr)) for attr in attrs)))

[docs]
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


[docs]
    def get_irradiance(self, solar_zenith, solar_azimuth, dni, ghi, dhi,
                       dni_extra=None, airmass=None, model='haydavies',
                       **kwargs):
        """
        Uses the :py:func:`irradiance.get_total_irradiance` function to
        calculate the plane of array irradiance components on a tilted
        surface defined by ``self.surface_tilt``,
        ``self.surface_azimuth``, and ``self.albedo``.

        Parameters
        ----------
        solar_zenith : float or Series.
            Solar zenith angle.
        solar_azimuth : float or Series.
            Solar azimuth angle.
        dni : float or Series
            Direct Normal Irradiance
        ghi : float or Series
            Global horizontal irradiance
        dhi : float or Series
            Diffuse horizontal irradiance
        dni_extra : None, float or Series, default None
            Extraterrestrial direct normal irradiance
        airmass : None, float or Series, default None
            Airmass
        model : String, default 'haydavies'
            Irradiance model.

        kwargs
            Extra parameters passed to :func:`irradiance.get_total_irradiance`.

        Returns
        -------
        poa_irradiance : DataFrame
            Column names are: ``total, beam, sky, ground``.
        """

        # not needed for all models, but this is easier
        if dni_extra is None:
            dni_extra = irradiance.get_extra_radiation(solar_zenith.index)

        if airmass is None:
            airmass = atmosphere.get_relative_airmass(solar_zenith)

        return irradiance.get_total_irradiance(self.surface_tilt,
                                               self.surface_azimuth,
                                               solar_zenith, solar_azimuth,
                                               dni, ghi, dhi,
                                               dni_extra=dni_extra,
                                               airmass=airmass,
                                               model=model,
                                               albedo=self.albedo,
                                               **kwargs)


    def get_iam(self, aoi, iam_model='physical'):
        """
        Determine the incidence angle modifier using the method specified by
        ``iam_model``.

        Parameters for the selected IAM model are expected to be in
        ``PVSystem.module_parameters``. Default parameters are available for
        the 'physical', 'ashrae' and 'martin_ruiz' models.

        Parameters
        ----------
        aoi : numeric
            The angle of incidence in degrees.

        aoi_model : string, default 'physical'
            The IAM model to be used. Valid strings are 'physical', 'ashrae',
            'martin_ruiz' and 'sapm'.

        Returns
        -------
        iam : numeric
            The AOI modifier.

        Raises
        ------
        ValueError if `iam_model` is not a valid model name.
        """
        model = iam_model.lower()
        if model in ['ashrae', 'physical', 'martin_ruiz']:
            param_names = iam._IAM_MODEL_PARAMS[model]
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

    def ashraeiam(self, aoi):
        """
        Deprecated. Use ``PVSystem.get_iam`` instead.
        """
        import warnings
        warnings.warn('PVSystem.ashraeiam is deprecated and will be removed in'
                      'v0.8, use PVSystem.get_iam instead',
                      pvlibDeprecationWarning)
        return PVSystem.get_iam(self, aoi, iam_model='ashrae')

    def physicaliam(self, aoi):
        """
        Deprecated. Use ``PVSystem.get_iam`` instead.
        """
        import warnings
        warnings.warn('PVSystem.physicaliam is deprecated and will be removed'
                      ' in v0.8, use PVSystem.get_iam instead',
                      pvlibDeprecationWarning)
        return PVSystem.get_iam(self, aoi, iam_model='physical')

    def calcparams_desoto(self, effective_irradiance, temp_cell, **kwargs):
        """
        Use the :py:func:`calcparams_desoto` function, the input
        parameters and ``self.module_parameters`` to calculate the
        module currents and resistances.

        Parameters
        ----------
        effective_irradiance : numeric
            The irradiance (W/m2) that is converted to photocurrent.

        temp_cell : float or Series
            The average cell temperature of cells within a module in C.

        **kwargs
            See pvsystem.calcparams_desoto for details

        Returns
        -------
        See pvsystem.calcparams_desoto for details
        """

        kwargs = _build_kwargs(['a_ref', 'I_L_ref', 'I_o_ref', 'R_sh_ref',
                                'R_s', 'alpha_sc', 'EgRef', 'dEgdT',
                                'irrad_ref', 'temp_ref'],
                               self.module_parameters)

        return calcparams_desoto(effective_irradiance, temp_cell, **kwargs)

    def calcparams_cec(self, effective_irradiance, temp_cell, **kwargs):
        """
        Use the :py:func:`calcparams_cec` function, the input
        parameters and ``self.module_parameters`` to calculate the
        module currents and resistances.

        Parameters
        ----------
        effective_irradiance : numeric
            The irradiance (W/m2) that is converted to photocurrent.

        temp_cell : float or Series
            The average cell temperature of cells within a module in C.

        **kwargs
            See pvsystem.calcparams_cec for details

        Returns
        -------
        See pvsystem.calcparams_cec for details
        """

        kwargs = _build_kwargs(['a_ref', 'I_L_ref', 'I_o_ref', 'R_sh_ref',
                                'R_s', 'alpha_sc', 'Adjust', 'EgRef', 'dEgdT',
                                'irrad_ref', 'temp_ref'],
                               self.module_parameters)

        return calcparams_cec(effective_irradiance, temp_cell, **kwargs)

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

    def sapm(self, effective_irradiance, temp_cell, **kwargs):
        """
        Use the :py:func:`sapm` function, the input parameters,
        and ``self.module_parameters`` to calculate
        Voc, Isc, Ix, Ixx, Vmp, and Imp.

        Parameters
        ----------
        effective_irradiance : numeric
            The irradiance (W/m2) that is converted to photocurrent.

        temp_cell : float or Series
            The average cell temperature of cells within a module in C.

        kwargs
            See pvsystem.sapm for details

        Returns
        -------
        See pvsystem.sapm for details
        """
        return sapm(effective_irradiance, temp_cell, self.module_parameters)

    def sapm_celltemp(self, poa_global, temp_air, wind_speed):
        """Uses :py:func:`temperature.sapm_cell` to calculate cell
        temperatures.

        Parameters
        ----------
        poa_global : numeric
            Total incident irradiance in W/m^2.

        temp_air : numeric
            Ambient dry bulb temperature in degrees C.

        wind_speed : numeric
            Wind speed in m/s at a height of 10 meters.

        Returns
        -------
        numeric, values in degrees C.
        """
        kwargs = _build_kwargs(['a', 'b', 'deltaT'],
                               self.temperature_model_parameters)
        return temperature.sapm_cell(poa_global, temp_air, wind_speed,
                                     **kwargs)

    def _infer_temperature_model_params(self):
        # try to infer temperature model parameters from from racking_model
        # and module_type
        param_set = self.racking_model + '_' + self.module_type
        if param_set in temperature.TEMPERATURE_MODEL_PARAMETERS['sapm']:
            return temperature._temperature_model_params('sapm', param_set)
        elif 'freestanding' in param_set:
            return temperature._temperature_model_params('pvsyst',
                                                         'freestanding')
        elif 'insulated' in param_set:  # after SAPM to avoid confusing keys
            return temperature._temperature_model_params('pvsyst',
                                                         'insulated')
        else:
            return {}

    def sapm_spectral_loss(self, airmass_relative):
        """
        Use the :py:func:`sapm_spectral_loss` function, the input
        parameters, and ``self.module_parameters`` to calculate F1.

        Parameters
        ----------
        airmass_relative : numeric
            Absolute airmass.

        Returns
        -------
        F1 : numeric
            The SAPM spectral loss coefficient.
        """
        return sapm_spectral_loss(, self.module_parameters)

    def sapm_aoi_loss(self, aoi):
        """
        Deprecated. Use ``PVSystem.get_iam`` instead.
        """
        import warnings
        warnings.warn('PVSystem.sapm_aoi_loss is deprecated and will be'
                      ' removed in v0.8, use PVSystem.get_iam instead',
                      pvlibDeprecationWarning)
        return PVSystem.get_iam(self, aoi, iam_model='sapm')

    def sapm_effective_irradiance(self, poa_direct, poa_diffuse,
                                  airmass_relative, aoi,
                                  reference_irradiance=1000):
        """
        Use the :py:func:`sapm_effective_irradiance` function, the input
        parameters, and ``self.module_parameters`` to calculate
        effective irradiance.

        Parameters
        ----------
        poa_direct : numeric
            The direct irradiance incident upon the module.  [W/m2]

        poa_diffuse : numeric
            The diffuse irradiance incident on module.  [W/m2]

        airmass_relative : numeric
            Absolute airmass. [unitless]

        aoi : numeric
            Angle of incidence. [degrees]

        Returns
        -------
        effective_irradiance : numeric
            The SAPM effective irradiance. [W/m2]
        """
        return sapm_effective_irradiance(
            poa_direct, poa_diffuse, airmass_relative, aoi,
            self.module_parameters)

    def pvsyst_celltemp(self, poa_global, temp_air, wind_speed=1.0):
        """Uses :py:func:`temperature.pvsyst_cell` to calculate cell
        temperature.

        Parameters
        ----------
        poa_global : numeric
            Total incident irradiance in W/m^2.

        temp_air : numeric
            Ambient dry bulb temperature in degrees C.

        wind_speed : numeric, default 1.0
            Wind speed in m/s measured at the same height for which the wind
            loss factor was determined.  The default value is 1.0, which is
            the wind speed at module height used to determine NOCT.

        Returns
        -------
        numeric, values in degrees C.
        """
        kwargs = _build_kwargs(['eta_m', 'alpha_absorption'],
                               self.module_parameters)
        kwargs.update(_build_kwargs(['u_c', 'u_v'],
                                    self.temperature_model_parameters))
        return temperature.pvsyst_cell(poa_global, temp_air, wind_speed,
                                       **kwargs)

    def faiman_celltemp(self, poa_global, temp_air, wind_speed=1.0):
        """
        Use :py:func:`temperature.faiman` to calculate cell temperature.

        Parameters
        ----------
        poa_global : numeric
            Total incident irradiance [W/m^2].

        temp_air : numeric
            Ambient dry bulb temperature [C].

        wind_speed : numeric, default 1.0
            Wind speed in m/s measured at the same height for which the wind
            loss factor was determined.  The default value 1.0 m/s is the wind
            speed at module height used to determine NOCT. [m/s]

        Returns
        -------
        numeric, values in degrees C.
        """
        kwargs = _build_kwargs(['u0', 'u1'],
                               self.temperature_model_parameters)
        return temperature.faiman(poa_global, temp_air, wind_speed,
                                  **kwargs)

    def first_solar_spectral_loss(self, pw, airmass_relative):

        """
        Use the :py:func:`first_solar_spectral_correction` function to
        calculate the spectral loss modifier. The model coefficients are
        specific to the module's cell type, and are determined by searching
        for one of the following keys in self.module_parameters (in order):
            'first_solar_spectral_coefficients' (user-supplied coefficients)
            'Technology' - a string describing the cell type, can be read from
            the CEC module parameter database
            'Material' - a string describing the cell type, can be read from
            the Sandia module database.

        Parameters
        ----------
        pw : array-like
            atmospheric precipitable water (cm).

        airmass_relative : array-like
            absolute (pressure corrected) airmass.

        Returns
        -------
        modifier: array-like
            spectral mismatch factor (unitless) which can be multiplied
            with broadband irradiance reaching a module's cells to estimate
            effective irradiance, i.e., the irradiance that is converted to
            electrical current.
        """

        if 'first_solar_spectral_coefficients' in \
                self.module_parameters.keys():
            coefficients = \
                   self.module_parameters['first_solar_spectral_coefficients']
            module_type = None
        else:
            module_type = self._infer_cell_type()
            coefficients = None

        return atmosphere.first_solar_spectral_correction(pw,
                                                          airmass_relative,
                                                          module_type,
                                                          coefficients)

    def _infer_cell_type(self):

        """
        Examines module_parameters and maps the Technology key for the CEC
        database and the Material key for the Sandia database to a common
        list of strings for cell type.

        Returns
        -------
        cell_type: str

        """

        _cell_type_dict = {'Multi-c-Si': 'multisi',
                           'Mono-c-Si': 'monosi',
                           'Thin Film': 'cigs',
                           'a-Si/nc': 'asi',
                           'CIS': 'cigs',
                           'CIGS': 'cigs',
                           '1-a-Si': 'asi',
                           'CdTe': 'cdte',
                           'a-Si': 'asi',
                           '2-a-Si': None,
                           '3-a-Si': None,
                           'HIT-Si': 'monosi',
                           'mc-Si': 'multisi',
                           'c-Si': 'multisi',
                           'Si-Film': 'asi',
                           'EFG mc-Si': 'multisi',
                           'GaAs': None,
                           'a-Si / mono-Si': 'monosi'}

        if 'Technology' in self.module_parameters.keys():
            # CEC module parameter set
            cell_type = _cell_type_dict[self.module_parameters['Technology']]
        elif 'Material' in self.module_parameters.keys():
            # Sandia module parameter set
            cell_type = _cell_type_dict[self.module_parameters['Material']]
        else:
            cell_type = None

        return cell_type

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
        return singlediode(photocurrent, saturation_current,
                           resistance_series, resistance_shunt, nNsVth,
                           ivcurve_pnts=ivcurve_pnts)

    def i_from_v(self, resistance_shunt, resistance_series, nNsVth, voltage,
                 saturation_current, photocurrent):
        """Wrapper around the :py:func:`i_from_v` function.

        Parameters
        ----------
        See pvsystem.i_from_v for details

        Returns
        -------
        See pvsystem.i_from_v for details
        """
        return i_from_v(resistance_shunt, resistance_series, nNsVth, voltage,
                        saturation_current, photocurrent)

    # inverter now specified by self.inverter_parameters
    def snlinverter(self, v_dc, p_dc):
        """Uses :func:`snlinverter` to calculate AC power based on
        ``self.inverter_parameters`` and the input parameters.

        Parameters
        ----------
        See pvsystem.snlinverter for details

        Returns
        -------
        See pvsystem.snlinverter for details
        """
        return snlinverter(v_dc, p_dc, self.inverter_parameters)

    def adrinverter(self, v_dc, p_dc):
        return adrinverter(v_dc, p_dc, self.inverter_parameters)

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

        return scale_voltage_current_power(data,
                                           voltage=self.modules_per_string,
                                           current=self.strings_per_inverter)

    def pvwatts_dc(self, g_poa_effective, temp_cell):
        """
        Calcuates DC power according to the PVWatts model using
        :py:func:`pvwatts_dc`, `self.module_parameters['pdc0']`, and
        `self.module_parameters['gamma_pdc']`.

        See :py:func:`pvwatts_dc` for details.
        """
        kwargs = _build_kwargs(['temp_ref'], self.module_parameters)

        return pvwatts_dc(g_poa_effective, temp_cell,
                          self.module_parameters['pdc0'],
                          self.module_parameters['gamma_pdc'],
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
        return pvwatts_losses(**kwargs)

    def pvwatts_ac(self, pdc):
        """
        Calculates AC power according to the PVWatts model using
        :py:func:`pvwatts_ac`, `self.module_parameters['pdc0']`, and
        `eta_inv_nom=self.inverter_parameters['eta_inv_nom']`.

        See :py:func:`pvwatts_ac` for details.
        """
        kwargs = _build_kwargs(['eta_inv_nom', 'eta_inv_ref'],
                               self.inverter_parameters)

        return pvwatts_ac(pdc, self.inverter_parameters['pdc0'], **kwargs)

    def localize(self, location=None, latitude=None, longitude=None,
                 **kwargs):
        """Creates a LocalizedPVSystem object using this object
        and location data. Must supply either location object or
        latitude, longitude, and any location kwargs

        Parameters
        ----------
        location : None or Location, default None
        latitude : None or float, default None
        longitude : None or float, default None
        **kwargs : see Location

        Returns
        -------
        localized_system : LocalizedPVSystem
        """

        if location is None:
            location = Location(latitude, longitude, **kwargs)

        return LocalizedPVSystem(pvsystem=self, location=location
                                 
class LocalizedPVSystem(PVSystem, Location):
    """
    The LocalizedPVSystem class defines a standard set of installed PV
    system attributes and modeling functions. This class combines the
    attributes and methods of the PVSystem and Location classes.

    The LocalizedPVSystem may have bugs due to the difficulty of
    robustly implementing multiple inheritance. See
    :py:class:`~pvlib.modelchain.ModelChain` for an alternative paradigm
    for modeling PV systems at specific locations.
    """
[docs]
    def __init__(self, pvsystem=None, location=None, **kwargs):

        new_kwargs = _combine_localized_attributes(
            pvsystem=pvsystem,
            location=location,
            **kwargs,
        )

        PVSystem.__init__(self, **new_kwargs)
        Location.__init__(self, **new_kwargs)


    def __repr__(self):
        attrs = ['name', 'latitude', 'longitude', 'altitude', 'tz',
                 'surface_tilt', 'surface_azimuth', 'module', 'inverter',
                 'albedo', 'racking_model']
        return ('LocalizedPVSystem: \n  ' + '\n  '.join(
            ('{}: {}'.format(attr, getattr(self, attr)) for attr in attrs)))