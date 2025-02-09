"""Function collection to calculate energy type co2 emissions"""

from typing import Union, Tuple
from co2calculator.constants import Unit
from co2calculator.data_handlers import ConversionFactors, EmissionFactors
from co2calculator.parameters import (
    ElectricityEmissionParameters,
    HeatingEmissionParameters,
)
from co2calculator._types import Kilogram

emission_factors = EmissionFactors()
conversion_factors = ConversionFactors()


def calc_co2_heating(
    consumption: float, options: Union[HeatingEmissionParameters, dict]
) -> Tuple[Kilogram, float, HeatingEmissionParameters]:
    """Function to compute heating emissions

    :param consumption: energy consumption
    :param options: parameters for heating emissions calculation
    :type consumption: float
    :type options: HeatingParameters | dict
    :return co2e: total emissions of heating energy consumption (kg)
    :return co2e_factor: heating emission factor
    :return params: parameters for heating emissions calculation
    :rtype: Tuple
    """
    # Validate parameters
    if options is None:
        options = {}

    # emission_params = HeatingEmissionParameters(**options)
    # params = HeatingParameters(
    #    heating_emission_parameters=emission_params, unit=options["unit"]
    # )
    params = HeatingEmissionParameters.parse_obj(options)

    if params.unit is not Unit.KWH:
        # Get the conversion factor
        conversion_factor = conversion_factors.get(
            fuel_type=params.fuel_type, unit=params.unit
        )

        consumption_kwh = consumption * conversion_factor
        params.unit = Unit.KWH
    else:
        consumption_kwh = consumption

    # Get the co2 factor
    co2e_factor = emission_factors.get(params.dict())
    co2e = consumption_kwh * co2e_factor * params.own_share

    return co2e, co2e_factor, params


def calc_co2_electricity(
    consumption: float, options: Union[ElectricityEmissionParameters, dict]
) -> Tuple[Kilogram, float, ElectricityEmissionParameters]:
    """Function to compute electricity emissions

    :param consumption: energy consumption
    :param options: parameters for electricity emissions calculation
    :type consumption: float
    :type options: ElectricityParameters | dict
    :return co2e: total emissions of electricity energy consumption (kg)
    :return co2e_factor: electricity emission factor
    :return params: parameters for electricity emissions calculation
    :rtype: Tuple
    """

    # Validate parameters
    if options is None:
        options = {}

    # emission_params = ElectricityEmissionParameters(**options)
    # params = ElectricityParameters(electricity_emission_parameters=emission_params)
    params = ElectricityEmissionParameters.parse_obj(options)
    # Get the co2 factor
    co2e_factor = emission_factors.get(params.dict())

    co2e = consumption * co2e_factor * params.own_share
    return co2e, co2e_factor, params
