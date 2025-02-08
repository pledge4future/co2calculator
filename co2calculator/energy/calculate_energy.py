"""Function colleciton to calculate energy type co2 emissions"""

from typing import Union
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
    params = HeatingParameters(**options)
    emission_params = HeatingEmissionParameters(
        **params.heating_emission_parameters.dict()
    )

    # Get the co2 factor
    co2e = emission_factors.get(emission_params.dict())

    if params.unit is not Unit.KWH:
        print(emission_params.fuel_type, params.unit)
        # Get the conversion factor
        conversion_factor = conversion_factors.get(
            fuel_type=emission_params.fuel_type, unit=params.unit
        )

        consumption_kwh = consumption * conversion_factor
    else:
        consumption_kwh = consumption

    return consumption_kwh * params.area_share * co2e


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
    params = ElectricityParameters(**options)
    emission_params = ElectricityEmissionParameters(
        **params.electricity_emission_parameters.dict()
    )

    # Get the co2 factor
    co2e = emission_factors.get(emission_params.dict())

    return consumption * params.energy_share * co2e
