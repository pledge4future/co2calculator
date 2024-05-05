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
    calc_co2_ferry,
    calc_co2_motorbike,
    calc_co2_pedelec,
    calc_co2_plane,
    calc_co2_train,
    calc_co2_tram,
)

from ._types import Kilogram, Kilometer
from .constants import (
    Size,
    CarFuel,
    BusFuel,
    TrainFuel,
    BusTrainRange,
    FlightClass,
    FerryClass,
    ElectricityFuel,
    HeatingFuel,
    Unit,
    TransportationMode,
)
from .data_handlers import EmissionFactors, ConversionFactors
from .distances import create_distance_request, get_distance, range_categories
from .parameters import (
    ElectricityEmissionParameters,
    HeatingEmissionParameters,
)

script_path = str(Path(__file__).parent)

emission_factors = EmissionFactors()
conversion_factors = ConversionFactors()


def calc_co2_electricity(
    consumption: float, fuel_type: ElectricityFuel = None, energy_share: float = 1
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
    params_extracted = {k: v for k, v in locals().items() if v is not None}
    params = ElectricityEmissionParameters(**params_extracted)

    # Get the co2 factor
    co2e = emission_factors.get(params.dict())

    return consumption * energy_share * co2e


def calc_co2_heating(
    consumption: float,
    fuel_type: HeatingFuel,
    unit: Unit = None,
    area_share: float = 1.0,
) -> Kilogram:
    """Function to compute heating emissions

    :param consumption: energy consumption
    :param fuel_type: fuel type used for heating
        [coal, district_heating, electricity, gas, heat_pump_air,
        heat_pump_ground, liquid_gas, oil, pellet, solar, woodchips]
    :param unit: unit of energy consumption [kwh, kg, l, m^3]
    :param area_share: share of building area used by research group
    :type consumption: float
    :type fuel_type: str
    :type unit: str
    :type area_share: float
    :return: total emissions of heating energy consumption
    :rtype: Kilogram
    """
    # Validate parameters
    assert 0 < area_share <= 1
    params_extracted = {k: v for k, v in locals().items() if v is not None}
    params = HeatingEmissionParameters(**params_extracted)

    # Get the co2 factor
    co2e = emission_factors.get(params.dict())

    if unit is not Unit.KWH:
        # Get the conversion factor
        conversion_factor = conversion_factors.get(fuel_type=fuel_type, unit=unit)

        consumption_kwh = consumption * conversion_factor
    else:
        consumption_kwh = consumption

    return consumption_kwh * area_share / co2e


def calc_co2_businesstrip(
    transportation_mode: TransportationMode,
    start=None,
    destination=None,
    distance: Kilometer = None,
    size: Size = None,
    fuel_type: CarFuel | BusFuel | TrainFuel = None,
    seating: FlightClass | FerryClass = None,
    passengers: int = None,
    roundtrip: bool = False,
) -> Tuple[Kilogram, Kilometer, str, str]:
    """Function to compute emissions for business trips based on transportation mode and trip specifics

    :param transportation_mode: mode of transport [car, bus, train, plane, ferry]
    :param start: Start of the trip (alternatively, distance can be provided)
    :param destination: Destination of the trip (alternatively, distance can be provided)
    :param distance: Distance travelled in km (alternatively, start and destination can be provided)
    :param size: Size class of the vehicle [small, medium, large, average] - only used for car and bus
    :param fuel_type: Fuel type of the vehicle
        [average, cng, diesel, electric, gasoline, hybrid, hydrogen, plug-in_hybrid]
        - only used for car, bus and train
    :param seating: seating class ["average", "Economy class", "Premium economy class", "Business class", "First class"]
                    - only used for plane
    :param passengers: Number of passengers in the vehicle (including the participant), number from 1 to 9
                                                - only used for car
    :param roundtrip: whether the trip is a round trip or not [True, False]
    :type transportation_mode: str
    :type distance: Kilometer
    :type size: str
    :type fuel_type: str
    :type seating: str
    :type passengers: int
    :type roundtrip: bool
    :return:    Emissions of the business trip in co2 equivalents,
                Distance of the business trip,
                Range category of the business trip [very short haul, short haul, medium haul, long haul]
                Range description (i.e., what range of distances does to category correspond to)
    :rtype: tuple[Kilogram, Kilometer, str, str]
    """

    # Evaluate if distance- or stop-based request.
    # Rules:
    # - `distance` is dominant;
    # - if distance not provided, take stops;
    # - if stops not available, raise error;
    # In general:
    # - If stop-based, calculate distance first, then continue only distance-based

    if not distance:
        request = create_distance_request(start, destination, transportation_mode)
        distance = get_distance(request)

    if transportation_mode == TransportationMode.CAR:
        emissions = calc_co2_car(
            distance=distance,
            options={},
        )
    elif transportation_mode == TransportationMode.BUS:
        emissions = calc_co2_bus(
            distance=distance,
            options={},
        )

    elif transportation_mode == TransportationMode.TRAIN:
        emissions = calc_co2_train(
            distance=distance,
            options={},
        )

    elif transportation_mode == TransportationMode.PLANE:
        emissions = calc_co2_plane(distance, options={})

    elif transportation_mode == TransportationMode.FERRY:
        emissions = calc_co2_ferry(distance, options={})

    else:
        raise ValueError(
            f"No emission factor available for the specified mode of transport '{transportation_mode}'."
        )
    if roundtrip is True:
        emissions *= 2

    # categorize according to distance (range)
    range_category, range_description = range_categories(distance)

    return emissions, distance, range_category, range_description


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
