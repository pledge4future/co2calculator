"""Function colleciton to calculate energy type co2 emissions"""

from ctypes import Union
from co2calculator.constants import KWH_TO_TJ, Unit
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
    consumption: float,
    options: Union[HeatingParameters, dict] = None,
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
    emission_params = HeatingEmissionParameters(**params.heating_emission_parameters)

    # Get the co2 factor
    co2e = emission_factors.get(params.dict())

    if params.unit is not Unit.KWH:
        # Get the conversion factor
        conversion_factor = ConversionFactors.get(
            fuel_type=emission_params.fuel_type, unit=params.unit
        )

        consumption_kwh = consumption * conversion_factor
    else:
        consumption_kwh = consumption

    # co2 equivalents for heating and electricity refer to a consumption of 1 TJ
    # so consumption needs to be converted to TJ
    return consumption_kwh * params.area_share / KWH_TO_TJ * co2e


def calc_co2_electricity(
    consumption: float, options: Union[ElectricityParameters, dict] = None
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
    emission_params = ElectricityEmissionParameters(**params)

    # Get the co2 factor
    co2e = emission_factors.get(params.dict())

    # co2 equivalents for heating and electricity refer to a consumption of 1 TJ
    # so consumption needs to be converted to TJ
    return consumption * emission_params.energy_share / KWH_TO_TJ * co2e
