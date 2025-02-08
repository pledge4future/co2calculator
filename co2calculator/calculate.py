#!/usr/bin/env python
# coding: utf-8
"""Functions to calculate co2 emissions"""
from pathlib import Path
from typing import Tuple

import pandas as pd

from co2calculator.mobility.calculate_mobility import (
    calc_co2_bicycle,
    calc_co2_bus,
    calc_co2_car,
    calc_co2_motorbike,
    calc_co2_pedelec,
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
    TransportationMode,
)
from .data_handlers import EmissionFactors, ConversionFactors
from .distances import create_distance_request, get_distance, range_categories

script_path = str(Path(__file__).parent)

emission_factors = EmissionFactors()
conversion_factors = ConversionFactors()


def calc_co2_commuting(
    transportation_mode: TransportationMode,
    weekly_distance: Kilometer,
    size: Size = None,
    fuel_type: BusFuel | CarFuel | TrainFuel = None,
    occupancy: int = None,
    passengers: int = None,
) -> Kilogram:
    """Calculate co2 emissions for commuting per mode of transport

    :param transportation_mode: [car, bus, train, bicycle, pedelec, motorbike, tram]
    :param weekly_distance: distance in km per week
    :param size: size of car or bus if applicable: [small, medium, large, average]
    :param fuel_type: fuel type of car, bus or train if applicable
    :param occupancy: occupancy [%], if applicable/known (only for bus): [20, 50, 80, 100]
    :param passengers: number of passengers, if applicable (only for car)
    :type transportation_mode: str
    :type weekly_distance: Kilometer
    :type size: str
    :type fuel_type: str
    :type occupancy: int
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
