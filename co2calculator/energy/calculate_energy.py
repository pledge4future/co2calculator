"""Function colleciton to calculate energy type co2 emissions"""

from typing import Union, Tuple
from co2calculator.constants import Unit
from co2calculator.data_handlers import ConversionFactors, EmissionFactors
from co2calculator.parameters import (
    ElectricityEmissionParameters,
    ElectricityParameters,
    HeatingEmissionParameters,
    HeatingParameters,
)
from co2calculator._types import Kilogram

emission_factors = EmissionFactors()
conversion_factors = ConversionFactors()


def calc_co2_heating(
    consumption: float, options: Union[HeatingParameters, dict]
) -> Kilogram:
    """Function to compute heating emissions

    :param consumption: energy consumption
    :param options: parameters for heating emissions calculation
    :type consumption: float
    :type options: HeatingParameters | dict
    :return: total emissions of heating energy consumption
    :rtype: Kilogram
    """
    # Validate parameters
    if options is None:
        options = {}

    emission_params = HeatingEmissionParameters(**options)
    params = HeatingParameters(
        heating_emission_parameters=emission_params, unit=options["unit"]
    )

    # Get the co2 factor
    co2e_factor = emission_factors.get(emission_params.dict())

    if params.unit is not Unit.KWH:
        print(emission_params.fuel_type, params.unit)
        # Get the conversion factor
        conversion_factor = conversion_factors.get(
            fuel_type=emission_params.fuel_type, unit=params.unit
        )

        consumption_kwh = consumption * conversion_factor
    else:
        consumption_kwh = consumption
    co2e = consumption_kwh * co2e_factor * params.area_share

    return co2e, co2e_factor, params


def calc_co2_electricity(
    consumption: float, options: Union[ElectricityParameters, dict]
) -> Kilogram:
    """Function to compute electricity emissions

    :param consumption: energy consumption
    :param fuel_type: energy (mix) used for electricity [german_energy_mix, solar]
    :param energy_share: the research group's approximate share of the total electricity energy consumption
    :type consumption: float
    :type fuel_type: str
    :type energy_share: float
    :return: total emissions of electricity energy consumption
    :rtype: Kilogram
    """

    # Validate parameters
    if options is None:
        options = {}

    emission_params = ElectricityEmissionParameters(**options)
    params = ElectricityParameters(electricity_emission_parameters=emission_params)

    # Get the co2 factor
    co2e_factor = emission_factors.get(emission_params.dict())

    co2e = consumption * co2e_factor * params.energy_share
    return co2e, co2e_factor, params
