#!/usr/bin/env python
# coding: utf-8
"""Functions to calculate co2 emissions"""
from pathlib import Path
from typing import Tuple, Union

import pandas as pd

from co2calculator.mobility.calculate_mobility import (
    calc_co2_bicycle,
    calc_co2_bus,
    calc_co2_car,
    calc_co2_ferry,
    calc_co2_motorbike,
    calc_co2_pedelec,
    calc_co2_plane,
    calc_co2_train,
    calc_co2_tram,
)
from co2calculator.util import get_calc_function_from_transport_mode

from ._types import Kilogram, Kilometer
from .constants import (
    Size,
    CarFuel,
    BusFuel,
    TrainFuel,
    ElectricityFuel,
    HeatingFuel,
    Unit,
    TransportationMode,
    CountryCode2,
)
from .data_handlers import EmissionFactors, ConversionFactors
from .parameters import (
    ElectricityEmissionParameters,
    HeatingEmissionParameters,
)

script_path = str(Path(__file__).parent)

emission_factors = EmissionFactors()
conversion_factors = ConversionFactors()


def calc_co2_electricity(
    consumption: float,
    own_share: float = 1.0,
    options: Union[ElectricityEmissionParameters, dict] = None,
) -> Kilogram:
    """Function to compute electricity emissions

    :param consumption: energy consumption
    :param own_share: the research group's approximate share of the total electricity energy consumption
    :param options: options for the electricity consumption
    :type consumption: float
    :type own_share: float
    :type options: dict
    :return: total emissions of electricity energy consumption
    :rtype: Kilogram
    """
    # Validate parameters
    assert 0 < own_share <= 1

    if options is None:
        options = {}
    # Validate parameters
    params = ElectricityEmissionParameters.parse_obj(options)

    # Get the co2 factor
    co2e_factor = emission_factors.get(params.dict())

    # Calculate emissions
    co2e = consumption * co2e_factor * own_share

    return co2e, co2e_factor, params


def calc_co2_heating(
    consumption: float,
    own_share: float = 1.0,
    unit: Unit = None,
    options: Union[HeatingEmissionParameters, dict] = None,
) -> Kilogram:
    """Function to compute heating emissions

    :param consumption: energy consumption
    :param own_share: the research group's approximate share of the total heating energy consumption
    :param unit: unit of energy consumption
    :param options: options for the heating consumption
    :type consumption: float
    :type own_share: float
    :type unit: str

    :return: total emissions of heating energy consumption
    :rtype: Kilogram
    """
    # Validate parameters
    assert 0 < own_share <= 1

    if options is None:
        options = {}
    # Validate parameters
    params = HeatingEmissionParameters.parse_obj(options)

    # Get the co2 factor
    co2e_factor = emission_factors.get(params.dict())

    if unit is not Unit.KWH:
        # Get the conversion factor
        conversion_factor = conversion_factors.get(
            fuel_type=params.fuel_type, unit=unit
        )
        consumption_kwh = consumption * conversion_factor
    else:
        consumption_kwh = consumption
    co2e = consumption_kwh * co2e_factor * own_share

    return co2e, co2e_factor, params


def calc_co2_trip(
    distance: Kilometer | None,
    transportation_mode: TransportationMode,
    custom_emission_factor: Kilogram | None = None,
    options: dict = None,
) -> Kilogram:
    """Function to compute emissions for a trip based on distance

    :param distance: Distance travelled in km
    :param transportation_mode: mode of transport. For options, see TransportationMode enum.
    :param custom_emission_factor: custom emission factor in kg/km. If provided, this will be used instead of the included emission factors.
    :param options: options for the trip. Type must match transportation mode.

    :return:    Emissions of the business trip in co2 equivalents.
    """
    if custom_emission_factor is not None:
        print("Ignoring transportation mode as custom emission factor is set")
        return distance * custom_emission_factor, custom_emission_factor, options
    else:
        # check for invalid transportation mode
        assert transportation_mode.lower() in (
            item.value for item in TransportationMode
        )
        # pass the distance and options to the respective function
        calc_function = get_calc_function_from_transport_mode(transportation_mode)
        return calc_function(distance, options)


def calc_co2_commuting(
    transportation_mode: TransportationMode,
    weekly_distance: Kilometer,
    size: Size = None,
    fuel_type: BusFuel | CarFuel | TrainFuel = None,
    passengers: int = None,
) -> Kilogram:
    """Calculate co2 emissions for commuting per mode of transport

    :param transportation_mode: [car, bus, train, bicycle, pedelec, motorbike, tram]
    :param weekly_distance: distance in km per week
    :param size: size of car or bus if applicable: [small, medium, large, average]
    :param fuel_type: fuel type of car, bus or train if applicable
    :param passengers: number of passengers, if applicable (only for car)
    :type transportation_mode: str
    :type weekly_distance: Kilometer
    :type size: str
    :type fuel_type: str
    :type passengers: int
    :return: total weekly emissions for the respective mode of transport
    :rtype: Kilogram
    """

    # get weekly co2e for respective mode of transport
    if transportation_mode == TransportationMode.CAR:
        weekly_co2e = calc_co2_car(
            distance=weekly_distance,
            options={},
        )

    elif transportation_mode == TransportationMode.MOTORBIKE:
        weekly_co2e = calc_co2_motorbike(options={}, distance=weekly_distance)
    elif transportation_mode == TransportationMode.BUS:
        weekly_co2e = calc_co2_bus(
            distance=weekly_distance,
            options={},
        )

    elif transportation_mode == TransportationMode.TRAIN:
        weekly_co2e = calc_co2_train(
            distance=weekly_distance,
            options={},
        )

    elif transportation_mode == TransportationMode.PEDELEC:
        weekly_co2e = calc_co2_pedelec(weekly_distance)
    elif transportation_mode == TransportationMode.BICYCLE:
        weekly_co2e = calc_co2_bicycle(weekly_distance)
    elif transportation_mode == TransportationMode.TRAM:
        weekly_co2e = calc_co2_tram(weekly_distance)
    else:
        raise ValueError(
            f"Transportation mode {transportation_mode} not found in database"
        )

    # multiply with work_weeks to obtain total (e.g. annual/monthly) co2e
    # total_co2e = weekly_co2e #* work_weeks

    return weekly_co2e
