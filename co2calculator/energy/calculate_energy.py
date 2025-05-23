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

    params = HeatingEmissionParameters.parse_obj(options)

    if params.in_kwh is not True:
        # Get the conversion factor
        conversion_factor = conversion_factors.get(fuel_type=params.fuel_type)

        consumption_kwh = consumption * conversion_factor
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

    params = ElectricityEmissionParameters.parse_obj(options)
    # Get the co2 factor
    co2e_factor = emission_factors.get(params.dict())

    co2e = consumption * co2e_factor * params.own_share
    return co2e, co2e_factor, params
