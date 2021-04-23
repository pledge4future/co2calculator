#!/usr/bin/env python

"""Functions to calculate co2 emissions"""

import os
import pandas as pd
import glob
import numpy as np
from .distances import haversine, geocoding_airport, geocoding, get_route
from .constants import KWH_TO_TJ
import sys


script_path = os.path.dirname(os.path.realpath(__file__))
emission_factor_df = pd.read_csv(f"{script_path}/../data/emission_factors.csv")
conversion_factor_df = pd.read_csv(f"{script_path}/../data/conversion_factors_heating.csv")


def calc_co2_car(passengers, size=None, fuel_type=None, distance=None, locations=None, roundtrip=False):
    """
    Function to compute the emissions of a car trip.
    :param passengers: Number of passengers in the car (including the person answering the questionnaire),
                        [1, 2, 3, 4, 5, 6, 7, 8, 9]
    :param size: size of car
                        ["small", "medium", "large", "average"]
    :param fuel_type: type of fuel the car is using
                        ["diesel", "gasoline", "cng", "electric", "average"]
    :param distance: Distance travelled in km;
                        alternatively param <locations> can be provided
    :param locations: List of locations in the form 'address, locality, country';
                        can have intermediate stops
                        e.g. ["Im Neuenheimer Feld 348, Heidelberg, Germany", "Marienplatz, Stuttgart, Germany",
                         "Bahnhof Basel, Basel, Switzerland"]
                        alternatively param <distance> can be provided
    :param roundtrip: Whether this trip is a roundtrip or not; Boolean [True, False]

    :return: Total emissions of trip in co2 equivalents
    """
    if distance is None and locations is None:
        print("Warning! Travel parameters missing. Please provide either the distance in km or a list of"
              "travelled locations in the form 'address, locality, country'")
    elif distance is None:
        coords = []
        for loc in locations:
            loc_name, loc_country, loc_coords = geocoding(loc)
            coords.append(loc_coords)
        distance = get_route(coords, "driving-car")
    co2e = emission_factor_df[(emission_factor_df["size_class"] == size) &
                              (emission_factor_df["fuel_type"] == fuel_type)]["co2e"].values[0]
    if roundtrip is True:
        distance *= 2
    emissions = distance * co2e / passengers

    return emissions


def calc_co2_bus(size=None, fuel_type=None, occupancy=50, vehicle_range=None, distance=None, stops=None, roundtrip=False):
    """
    Function to compute the emissions of a bus trip.
    :param size: size class of the bus;                 ["medium", "large", "average"]
    :param fuel_type: type of fuel the bus is using;    ["diesel"]
    :param occupancy: number of people on the bus       [20, 50, 80, 100]
    :param distance: Distance travelled in km;
                        alternatively param <stops> can be provided
    :param stops: List of locations, ideally in the form 'address, locality, country';
                    alternatively param <distance> can be provided
    :param roundtrip: Whether this trip is a roundtrip or not; Boolean [True, False]
    :return: Total emissions of trip in co2 equivalents
    """
    detour_coefficient = 1.5
    if distance is None and stops is None:
        print("Warning! Travel parameters missing. Please provide either the distance in km or a list of"
              "travelled train stations in the form 'address, locality, country'")
    elif distance is None and stops is not None:
        distance = 0
        coords = []
        for loc in stops:
            loc_name, loc_country, loc_coords = geocoding(loc)
            coords.append(loc_coords)
        for i in range(0, len(coords) - 1):
            # compute great circle distance between locations
            distance += haversine(coords[i][1], coords[i][0], coords[i + 1][1], coords[i + 1][0])
        distance *= detour_coefficient
    if roundtrip is True:
        distance *= 2
    co2e = emission_factor_df[(emission_factor_df["size_class"] == size) &
                              (emission_factor_df["fuel_type"] == fuel_type) &
                              (emission_factor_df["occupancy"] == occupancy) &
                              (emission_factor_df["range"] == vehicle_range)]["co2e"].values[0]
    emissions = distance * co2e

    return emissions


def calc_co2_train(fuel_type=None, vehicle_range=None, distance=None, stops=None, roundtrip=False):
    """
    Function to compute the emissions of a bus trip.
    :param fuel_type: type of fuel the train is using;    ["diesel", "electric", "average"]
    :param distance: Distance travelled in km;
                        alternatively param <stops> can be provided
    :param stops: List of train stations, ideally in the form 'address, locality, country';
                    alternatively param <distance> can be provided
    :param roundtrip: Whether this trip is a roundtrip or not; Boolean [True, False]
    :return: Total emissions of trip in co2 equivalents
    """
    detour_coefficient = 1.2
    if distance is None and stops is None:
        print("Warning! Travel parameters missing. Please provide either the distance in km or a list of"
              "travelled train stations in the form 'address, locality, country'")
    elif distance is None:
        distance = 0
        coords = []
        for loc in stops:
            loc_name, loc_country, loc_coords = geocoding(loc)
            coords.append(loc_coords)
        for i in range(len(coords) - 1):
            # compute great circle distance between locations
            distance += haversine(coords[i][1], coords[i][0], coords[i+1][1], coords[i+1][0])
        distance *= detour_coefficient
    if roundtrip is True:
        distance *= 2
    co2e = emission_factor_df[(emission_factor_df["fuel_type"] == fuel_type)
                              & (emission_factor_df["range"] == vehicle_range)]["co2e"].values[0]
    emissions = distance * co2e

    return emissions


def calc_co2_plane(start, destination, roundtrip=False):
    """
    Function to compute emissions of a train trip
    :param start: IATA code of start airport
    :param destination: IATA code of destination airport
    :param roundtrip: Whether this trip is a roundtrip or not; Boolean [True, False]
    :return: Total emissions of flight in co2 equivalents
    """
    detour_constant = 95 # 95 km as used by MyClimate and ges 1point5, see also
    # Méthode pour la réalisation des bilans d’émissions de gaz à effet de serre conformément à l’article L. 229­25 du code de l’environnement – 2016 – Version 4
    # get geographic coordinates of airports
    _, geom_start, country_start = geocoding_airport(start)
    _, geom_dest, country_dest = geocoding_airport(destination)
    # compute great circle distance between airports
    distance = haversine(geom_start[1], geom_start[0], geom_dest[1], geom_dest[0])
    # add detour constant
    distance += detour_constant
    # retrieve whether airports are in the same country and query emission factor
    if country_start == country_dest:
        co2e = emission_factor_df[(emission_factor_df["range"] == "inland")]["co2e"].values[0]
    else:
        co2e = emission_factor_df[(emission_factor_df["range"] == "international")]["co2e"].values[0]
    # multiply emission factor with distance and by 2 if roundtrip
    emissions = distance * co2e
    if roundtrip is True:
        emissions *= 2

    return emissions


def calc_co2_electricity(consumption, fuel_type):
    """
    Function to compute electricity emissions
    :param consumption: energy consumption
    :param fuel_type: energy (mix) used for electricity [german_energy_mix, solar]
    :return: total emissions of electricity energy consumption
    """
    co2e = emission_factor_df[(emission_factor_df["fuel_type"] == fuel_type)]["co2e"].values[0]
    # co2 equivalents for heating and electricity refer to a consumption of 1 TJ
    # so consumption needs to be converted to TJ
    emissions = consumption/KWH_TO_TJ * co2e

    return emissions


def calc_co2_heating(consumption, unit, fuel_type):
    """
    Function to compute heating emissions
    :param consumption: energy consumption
    :param unit: unit of energy consumption [kwh, kg, l, m^3]
    :param fuel_type: fuel type used for heating
    :return: total emissions of heating energy consumption
    """
    valid_unit_choices = ["kWh", "l", "kg", "m^3"]
    assert unit in valid_unit_choices, f"unit={unit} is invalid. Valid choices are {', '.join(valid_unit_choices)}"
    if unit != "kWh":
        try:
            conversion_factor = conversion_factor_df[
                (conversion_factor_df["fuel"] == fuel_type)
                & (conversion_factor_df["unit"] == unit)
                ]["conversion_value"].values[0]
        except KeyError:
            print(
                "No conversion data is available for this fuel type. Conversion is only supported for the following"
                "fuel types and units. Alternatively, provide consumption in the unit kWh.\n")
            print(conversion_factor_df[["fuel", "unit"]])
            raise ValueError("No conversion data is available for this fuel type. Provide consumption in a "
                             "different unit.")

        consumption_kwh = consumption * conversion_factor
    else:
        consumption_kwh = consumption

    co2e = emission_factor_df[(emission_factor_df["fuel_type"] == fuel_type)]["co2e"].values[0]
    # co2 equivalents for heating and electricity refer to a consumption of 1 TJ
    # so consumption needs to be converted to TJ
    emissions = consumption_kwh / KWH_TO_TJ * co2e

    return emissions


def calc_co2_businesstrip(transportation_mode, start=None, destination=None, distance=None, size=None, fuel_type=None,
                          occupancy=50, passengers=None, roundtrip=False):
    """
    Function to compute emissions for business trips based on transportation mode and trip specifics
    :param transportation_mode: mode of transport [car, bus, train, plane]
    :param start: Start of the trip (alternatively, distance can be provided)
    :param destination: Destination of the trip (alternatively, distance can be provided)
    :param distance: Distance travelled in km (alternatively, start and destination can be provided)
    :param size: Size class of the vehicle [small, medium, large, average] - only used for car and bus
    :param fuel_type: Fuel type of the vehicle [diesel, gasoline, electricity, cng, hydrogen, average] - only used for
                                                car, bus and train
    :param occupancy: Occupancy of the vehicle [20, 50, 80, 100] - only used for bus
    :param passengers: Number of passengers in the vehicle (including the participant), number from 1 to 9
                                                - only used for car
    :param roundtrip: whether the trip is a roundtrip or not [True, False]
    :return: Emissions of the business trip in co2 equivalents
    """
    if distance is None and (start is None or destination is None):
        assert ValueError("Either start and destination or distance must be provided.")
    elif distance is not None and (start is not None or destination is not None):
        print("Warning! Both distance and start/stop location were provided. Only distance will be used for emission "
              "calculation.")
    elif start is None and destination is None and distance is not None:
        stops = None
    elif start is not None and destination is not None and distance is None:
        stops = [start, destination]
    if transportation_mode == "car":
        emissions = calc_co2_car(passengers, size=size, fuel_type=fuel_type, distance=distance, locations=stops,
                                 roundtrip=roundtrip)
    elif transportation_mode == "bus":
        emissions = calc_co2_bus(size=size, fuel_type=fuel_type, occupancy=occupancy, vehicle_range="long-distance",
                                 distance=distance, locations=stops, roundtrip=roundtrip)
    elif transportation_mode == "train":
        emissions = calc_co2_train(fuel_type=fuel_type, vehicle_range="long-distance", distance=distance, stops=stops,
                                   roundtrip=roundtrip)
    elif transportation_mode == "plane":
        emissions = calc_co2_plane(start, destination, roundtrip=False)

    return emissions
