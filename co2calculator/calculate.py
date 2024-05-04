#!/usr/bin/env python
# coding: utf-8
"""Functions to calculate co2 emissions"""

import warnings
from pathlib import Path
from typing import Tuple

import pandas as pd

from ._types import Kilogram, Kilometer
from .constants import (
    KWH_TO_TJ,
    Size,
    CarFuel,
    BusFuel,
    TrainFuel,
    BusTrainRange,
    FlightClass,
    FlightRange,
    FerryClass,
    ElectricityFuel,
    HeatingFuel,
    Unit,
    TransportationMode,
    EmissionCategory,
)
from .data_handlers import EmissionFactors
from .distances import create_distance_request, get_distance, range_categories
from .parameters import (
    CarEmissionParameters,
    MotorbikeEmissionParameters,
    BusEmissionParameters,
    TrainEmissionParameters,
    PlaneEmissionParameters,
    FerryEmissionParameters,
    ElectricityEmissionParameters,
    HeatingEmissionParameters,
)

script_path = str(Path(__file__).parent)

emission_factors = EmissionFactors()
conversion_factor_df = pd.read_csv(
    f"{script_path}/../data/conversion_factors_heating.csv"
)


def calc_co2_car(
    distance: Kilometer,
    passengers: int = None,
    size: Size = None,
    fuel_type: CarFuel = None,
) -> Kilogram:
    """
    Function to compute the emissions of a car trip.
    :param distance: Distance travelled by car;
    :param passengers: Number of passengers in the car (including the person answering the questionnaire),
                        [1, 2, 3, 4, 5, 6, 7, 8, 9]                             default: 1
    :param size: size of car
                        ["small", "medium", "large", "average"]                 default: "average"
    :param fuel_type: type of fuel the car is using
                        ["diesel", "gasoline", "cng", "electric", "hybrid", "plug-in_hybrid", "average"]
                        default: "average"
    :type distance: Kilometer
    :type passengers: int
    :type size: str
    :type fuel_type: str
    :return: Total emissions of trip in co2 equivalents
    :rtype: Kilogram
    """
    # Validate parameters
    params_extracted = {k: v for k, v in locals().items() if v is not None}
    params = CarEmissionParameters(**params_extracted)
    # Get the co2 factor
    co2e = emission_factors.get(params.dict())
    # Calculate emissions
    return distance * co2e / params.passengers


def calc_co2_motorbike(distance: Kilometer = None, size: Size = None) -> Kilogram:
    """
    Function to compute the emissions of a motorbike trip.
    :param distance: Distance travelled by motorbike;
                        alternatively param <locations> can be provided
    :param size: size of motorbike
                        ["small", "medium", "large", "average"]
    :type distance: Kilometer
    :type size: str
    :return: Total emissions of trip in co2 equivalents
    :rtype: Kilogram
    """
    # Validate parameters
    params_extracted = {k: v for k, v in locals().items() if v is not None}
    params = MotorbikeEmissionParameters(**params_extracted)
    # Get the co2 factor
    co2e = emission_factors.get(params.dict())
    # Calculate emissions
    return distance * co2e


def calc_co2_bus(
    distance: Kilometer,
    size: Size = None,
    fuel_type: BusFuel = None,
    occupancy: int = None,
    vehicle_range: BusTrainRange = None,
) -> Kilogram:
    """
    Function to compute the emissions of a bus trip.
    :param distance: Distance travelled by bus;
    :param size: size class of the bus;                 ["medium", "large", "average"]
    :param fuel_type: type of fuel the bus is using;    ["diesel", "cng", "hydrogen"]
    :param occupancy: number of people on the bus       [20, 50, 80, 100]
    :param vehicle_range: range/haul of the vehicle     ["local", "long-distance"]
    :type distance: Kilometer
    :type size: str
    :type fuel_type: str
    :type occupancy: int
    :type vehicle_range: str
    :return: Total emissions of trip in co2 equivalents
    :rtype: Kilogram
    """
    # Validate parameters
    params_extracted = {k: v for k, v in locals().items() if v is not None}
    params = BusEmissionParameters(**params_extracted)
    # Get the co2 factor
    co2e = emission_factors.get(params.dict())
    return distance * co2e


def calc_co2_train(
    distance: Kilometer,
    fuel_type: TrainFuel = None,
    vehicle_range: BusTrainRange = None,
) -> Kilogram:
    """
    Function to compute the emissions of a train trip.
    :param distance: Distance travelled by train;
    :param fuel_type: type of fuel the train is using;    ["diesel", "electric", "average"]
    :param vehicle_range: range/haul of the vehicle       ["local", "long-distance"]
    :type distance: Kilometer
    :type fuel_type: float
    :type vehicle_range: str
    :return: Total emissions of trip in co2 equivalents
    :rtype: Kilogram
    """

    # Validate parameters
    params_extracted = {k: v for k, v in locals().items() if v is not None}
    params = TrainEmissionParameters(**params_extracted)
    # Get the co2 factor
    co2e = emission_factors.get(params.dict())
    return distance * co2e


def calc_co2_plane(distance: Kilometer, seating: FlightClass = None) -> Kilogram:
    """
    Function to compute emissions of a plane trip
    :param distance: Distance of plane flight
    :param seating: Seating class in the airplane; Emission factors differ between seating classes because
                          business class or first class seats take up more space. An airplane with more such therefore
                          needs to have higher capacity to transport less people -> more co2
                          ["average", "economy_class", "business_class", "premium_economy_class", "first_class"]
    :type distance: Kilometer
    :type seating: str
    :return: Total emissions of flight in co2 equivalents
    :rtype: Kilogram
    """

    # Retrieve whether distance is <= 700, > 700 and <= 3700 or above 3700 km
    # todo: move to PlaneEmissionParameters
    if distance <= 700:
        range = FlightRange.DOMESTIC
    elif 700 < distance <= 3700:
        range = FlightRange.SHORT_HAUL
    elif distance > 3700:
        range = FlightRange.LONG_HAUL

    # Validate parameters
    params_extracted = {k: v for k, v in locals().items() if v is not None}
    params = PlaneEmissionParameters(**params_extracted)
    # Get the co2 factor
    co2e = emission_factors.get(params.dict())
    return distance * co2e


def calc_co2_ferry(distance: Kilometer, seating: FerryClass = None) -> Kilogram:
    """
    Function to compute emissions of a ferry trip
    :param distance: Distance of ferry trip
    :param seating: ["average", "Foot passenger", "Car passenger"]
    :type distance: Kilometer
    :type seating: str
    :return: Total emissions of sea travel in co2 equivalents
    :rtype: Kilogram
    """

    # Validate parameters
    params_extracted = {k: v for k, v in locals().items() if v is not None}
    params = FerryEmissionParameters(**params_extracted)
    # Get the co2 factor
    co2e = emission_factors.get(params.dict())
    return distance * co2e


def calc_co2_bicycle(weekly_distance):
    """Calculate co2 emissions for commuting by bicycle

    :param weekly_distance: distance in km per week
    """
    co2e = emission_factors.get(
        {
            "category": EmissionCategory.TRANSPORT,
            "subcategory": TransportationMode.BICYCLE,
        }
    )
    return co2e * weekly_distance


def calc_co2_pedelec(weekly_distance):
    """Calculate co2 emissions for commuting by pedelec

    :param weekly_distance: distance in km per week
    """
    co2e = emission_factors.get(
        {
            "category": EmissionCategory.TRANSPORT,
            "subcategory": TransportationMode.PEDELEC,
        }
    )
    return co2e * weekly_distance


def calc_co2_tram(weekly_distance):
    """Calculate co2 emissions for commuting by pedelec

    :param weekly_distance: distance in km per week
    """
    co2e = emission_factors.get(
        {
            "category": EmissionCategory.TRANSPORT,
            "subcategory": TransportationMode.TRAM,
        }
    )
    return co2e * weekly_distance


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

    # co2 equivalents for heating and electricity refer to a consumption of 1 TJ
    # so consumption needs to be converted to TJ
    return consumption * energy_share / KWH_TO_TJ * co2e


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
    params_extracted = {k: v for k, v in locals().items() if v is not None}
    params = HeatingEmissionParameters(**params_extracted)

    # Get the co2 factor
    co2e = emission_factors.get(params.dict())

    if params.unit is not Unit.KWH:
        conversion_factor = get_conversion_factor(
            fuel_type=params.fuel_type, unit=params.unit
        )
        consumption_kwh = consumption * conversion_factor
    else:
        consumption_kwh = consumption

    # co2 equivalents for heating and electricity refer to a consumption of 1 TJ
    # so consumption needs to be converted to TJ
    return consumption_kwh * area_share / KWH_TO_TJ * co2e


def calc_co2_businesstrip(
    transportation_mode: TransportationMode,
    start=None,
    destination=None,
    distance: Kilometer = None,
    size: Size = None,
    fuel_type: CarFuel | BusFuel | TrainFuel = None,
    occupancy: int = None,
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
    :param occupancy: Occupancy of the vehicle in % [20, 50, 80, 100] - only used for bus
    :param seating: seating class ["average", "Economy class", "Premium economy class", "Business class", "First class"]
                    - only used for plane
    :param passengers: Number of passengers in the vehicle (including the participant), number from 1 to 9
                                                - only used for car
    :param roundtrip: whether the trip is a round trip or not [True, False]
    :type transportation_mode: str
    :type distance: Kilometer
    :type size: str
    :type fuel_type: str
    :type occupancy: int
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
            passengers=passengers,
            size=size,
            fuel_type=fuel_type,
        )

    elif transportation_mode == TransportationMode.BUS:
        emissions = calc_co2_bus(
            distance=distance,
            size=size,
            fuel_type=fuel_type,
            occupancy=occupancy,
            vehicle_range=BusTrainRange.LONG_DISTANCE,
        )

    elif transportation_mode == TransportationMode.TRAIN:
        emissions = calc_co2_train(
            distance=distance,
            fuel_type=fuel_type,
            vehicle_range=BusTrainRange.LONG_DISTANCE,
        )

    elif transportation_mode == TransportationMode.PLANE:
        emissions = calc_co2_plane(distance, seating=seating)

    elif transportation_mode == TransportationMode.FERRY:
        emissions = calc_co2_ferry(distance, seating=seating)

    else:
        raise ValueError(
            f"No emission factor available for the specified mode of transport '{transportation_mode}'."
        )
    if roundtrip is True:
        emissions *= 2

    # categorize according to distance (range)
    range_category, range_description = range_categories(distance)

    return emissions, distance, range_category, range_description


def get_conversion_factor(fuel_type: HeatingFuel, unit: Unit) -> float:
    """
    Function to retrieve conversion factor for converting consumption for certain fuel types (and units) to kWh
    :param fuel_type: :param fuel_type: fuel type used for heating
        [coal, district_heating, electricity, gas, heat_pump_air,
        heat_pump_ground, liquid_gas, oil, pellet, solar, woodchips]
    :param unit: unit of energy consumption [kwh, kg, l, m^3]
    :return: conversion factor
    """
    try:
        conversion_factor = conversion_factor_df[
            (conversion_factor_df["fuel"] == fuel_type)
            & (conversion_factor_df["unit"] == unit)
        ]["conversion_value"].values[0]
    except (KeyError, IndexError):
        print(
            "No conversion data is available for this fuel type. Conversion is only supported for the following"
            "fuel types and units. Alternatively, provide consumption in the unit kWh.\n"
        )
        print(conversion_factor_df[["fuel", "unit"]])
        raise ValueError(
            "No conversion data is available for this fuel type. Provide consumption in a "
            "different unit."
        )
    return conversion_factor


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
            passengers=passengers,
            size=size,
            fuel_type=fuel_type,
            distance=weekly_distance,
        )

    elif transportation_mode == TransportationMode.MOTORBIKE:
        weekly_co2e = calc_co2_motorbike(size=size, distance=weekly_distance)
    elif transportation_mode == TransportationMode.BUS:
        weekly_co2e = calc_co2_bus(
            size=size,
            fuel_type=fuel_type,
            occupancy=occupancy,
            vehicle_range=BusTrainRange.LOCAL,
            distance=weekly_distance,
        )

    elif transportation_mode == TransportationMode.TRAIN:
        weekly_co2e = calc_co2_train(
            fuel_type=fuel_type,
            vehicle_range=BusTrainRange.LOCAL,
            distance=weekly_distance,
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
