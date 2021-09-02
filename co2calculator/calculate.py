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


def calc_co2_car(passengers, size=None, fuel_type=None, distance=None, stops=None):
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
    :param stops: List of locations in the form 'address, locality, country';
                        can have intermediate stops
                        e.g. ["Im Neuenheimer Feld 348, Heidelberg, Germany", "Marienplatz, Stuttgart, Germany",
                         "Bahnhof Basel, Basel, Switzerland"]
                        alternatively param <distance> can be provided

    :return: Total emissions of trip in co2 equivalents
    """
    if distance is None and stops is None:
        print("Warning! Travel parameters missing. Please provide either the distance in km or a list of"
              "travelled locations in the form 'address, locality, country'")
    elif distance is None:
        coords = []
        for loc in stops:
            loc_name, loc_country, loc_coords = geocoding(loc)
            coords.append(loc_coords)
        distance = get_route(coords, "driving-car")
    co2e = emission_factor_df[(emission_factor_df["size_class"] == size) &
                              (emission_factor_df["fuel_type"] == fuel_type)]["co2e"].values[0]
    emissions = distance * co2e / passengers

    return emissions


def calc_co2_motorbike(size=None, distance=None, stops=None):
    """
    Function to compute the emissions of a car trip.
    :param size: size of motorbike
                        ["small", "medium", "large", "average"]
    :param distance: Distance travelled in km;
                        alternatively param <locations> can be provided
    :param stops: List of locations in the form 'address, locality, country';
                        can have intermediate stops
                        e.g. ["Marktplatz, Heidelberg, Germany", "Im Neuenheimer Feld 348, Heidelberg, Germany"]
                        alternatively param <distance> can be provided

    :return: Total emissions of trip in co2 equivalents
    """
    if distance is None and stops is None:
        print("Warning! Travel parameters missing. Please provide either the distance in km or a list of"
              "travelled locations in the form 'address, locality, country'")
    elif distance is None:
        coords = []
        for loc in stops:
            loc_name, loc_country, loc_coords = geocoding(loc)
            coords.append(loc_coords)
        distance = get_route(coords, "driving-car")
    co2e = emission_factor_df[(emission_factor_df["size_class"] == size)]["co2e"].values[0]
    emissions = distance * co2e

    return emissions


def calc_co2_bus(size=None, fuel_type=None, occupancy=50, vehicle_range=None, distance=None, stops=None):
    """
    Function to compute the emissions of a bus trip.
    :param size: size class of the bus;                 ["medium", "large", "average"]
    :param fuel_type: type of fuel the bus is using;    ["diesel"]
    :param occupancy: number of people on the bus       [20, 50, 80, 100]
    :param vehicle_range: range/haul of the vehicle     ["local", "long-distance"]
    :param distance: Distance travelled in km;
                        alternatively param <stops> can be provided
    :param stops: List of locations, ideally in the form 'address, locality, country';
                    alternatively param <distance> can be provided

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
    co2e = emission_factor_df[(emission_factor_df["size_class"] == size) &
                              (emission_factor_df["fuel_type"] == fuel_type) &
                              (emission_factor_df["occupancy"] == occupancy) &
                              (emission_factor_df["range"] == vehicle_range)]["co2e"].values[0]
    emissions = distance * co2e

    return emissions


def calc_co2_train(fuel_type=None, vehicle_range=None, distance=None, stops=None):
    """
    Function to compute the emissions of a train trip.
    :param fuel_type: type of fuel the train is using;    ["diesel", "electric", "average"]
    :param vehicle_range: range/haul of the vehicle       ["local", "long-distance"]
    :param distance: Distance travelled in km;
                        alternatively param <stops> can be provided
    :param stops: List of train stations, ideally in the form 'address, locality, country';
                    alternatively param <distance> can be provided

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
    co2e = emission_factor_df[(emission_factor_df["fuel_type"] == fuel_type)
                              & (emission_factor_df["range"] == vehicle_range)]["co2e"].values[0]
    emissions = distance * co2e

    return emissions


def calc_co2_plane(start, destination, seating_class="average"):
    """
    Function to compute emissions of a plane trip
    :param start: IATA code of start airport
    :param destination: IATA code of destination airport
    :param seating_class: Seating class in the airplane; Emission factors differ between seating classes because
                          business class or first class seats take up more space. An airplane with more such therefore
                          needs to have higher capacity to transport less people -> more co2
                          ["average", "Economy class", "Business class", "Premium economy class", "First class"]

    :return: Total emissions of flight in co2 equivalents
    """
    detour_constant = 95  # 95 km as used by MyClimate and ges 1point5, see also
    # Méthode pour la réalisation des bilans d’émissions de gaz à effet de serre conformément à l’article L. 229­25 du code de l’environnement – 2016 – Version 4
    # get geographic coordinates of airports
    _, geom_start, country_start = geocoding_airport(start)
    _, geom_dest, country_dest = geocoding_airport(destination)
    # compute great circle distance between airports
    distance = haversine(geom_start[1], geom_start[0], geom_dest[1], geom_dest[0])
    # add detour constant
    distance += detour_constant
    # retrieve whether airports are in the same country and/or if distance is below or above 3700 km
    if country_start == country_dest:
        flight_range = "domestic"
    elif distance <= 3700:
        flight_range = "short-haul"
    elif distance >= 3700:
        flight_range = "long-haul"
    # Todo: Error handling: What if no airplane with that range and seating class found
    co2e = emission_factor_df[(emission_factor_df["range"] == flight_range) &
                              (emission_factor_df["seating"] == seating_class)]["co2e"].values[0]
    # multiply emission factor with distance
    emissions = distance * co2e

    return emissions


def calc_co2_ferry(start, destination, seating_class="average"):
    """
    Function to compute emissions of a ferry trip
    :param start: city of start port in the form "<city>, <country>"
    :param destination: city of destination port in the form "<city>, <country>"
    :param seating_class: ["average", "Foot passenger", "Car passenger"]

    :return: Total emissions of sea travel in co2 equivalents
    """
    # todo: Do we have a way of checking if there even exists a ferry connection between the given cities (of if the
    #  cities even have a port?
    detour_coefficient = 1  # Todo
    # get geographic coordinates of ports
    _, _, geom_start = geocoding(start)
    _, _, geom_dest = geocoding(destination)
    # compute great circle distance between airports
    distance = haversine(geom_start[1], geom_start[0], geom_dest[1], geom_dest[0])
    # add detour constant
    distance *= detour_coefficient
    # get emission factor
    co2e = emission_factor_df[(emission_factor_df["seating"] == seating_class)]["co2e"].values[0]
    # multiply emission factor with distance
    emissions = distance * co2e

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


def calc_co2_heating(consumption, unit, fuel_type, area_share=None):
    """
    Function to compute heating emissions
    :param consumption: energy consumption
    :param unit: unit of energy consumption [kwh, kg, l, m^3]
    :param fuel_type: fuel type used for heating
    :param area_share: share of building area used by research group
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
    if area_share is not None:
        consumption_kwh = consumption_kwh*area_share

    co2e = emission_factor_df[(emission_factor_df["fuel_type"] == fuel_type)]["co2e"].values[0]
    # co2 equivalents for heating and electricity refer to a consumption of 1 TJ
    # so consumption needs to be converted to TJ
    emissions = consumption_kwh / KWH_TO_TJ * co2e

    return emissions


def calc_co2_businesstrip(transportation_mode, start=None, destination=None, distance=None, size="average",
                          fuel_type="average", occupancy=50, seating="average", passengers=1, roundtrip=False):
    """
    Function to compute emissions for business trips based on transportation mode and trip specifics
    :param transportation_mode: mode of transport [car, bus, train, plane]
    :param start: Start of the trip (alternatively, distance can be provided)
    :param destination: Destination of the trip (alternatively, distance can be provided)
    :param distance: Distance travelled in km (alternatively, start and destination can be provided)
    :param size: Size class of the vehicle [small, medium, large, average] - only used for car and bus
    :param fuel_type: Fuel type of the vehicle [diesel, gasoline, electricity, cng, hydrogen, average] - only used for
                                                car, bus and train
    :param occupancy: Occupancy of the vehicle in % [20, 50, 80, 100] - only used for bus
    :param seating: seating class ["average", "Economy class", "Premium economy class", "Business class", "First class"]
                    - only used for plane
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
        emissions = calc_co2_car(passengers, size=size, fuel_type=fuel_type, distance=distance, stops=stops)
    elif transportation_mode == "bus":
        emissions = calc_co2_bus(size=size, fuel_type=fuel_type, occupancy=occupancy, vehicle_range="long-distance",
                                 distance=distance, stops=stops)
    elif transportation_mode == "train":
        emissions = calc_co2_train(fuel_type=fuel_type, vehicle_range="long-distance", distance=distance, stops=stops)
    elif transportation_mode == "plane":
        emissions = calc_co2_plane(start, destination, seating_class=seating)
    elif transportation_mode == "ferry":
        emissions = calc_co2_ferry(start, destination, seating_class=seating)
    else:
        assert ValueError("No emission factor available for the specified mode of transport.")
    if roundtrip is True:
        emissions *= 2

    return emissions


def calc_co2_commuting(transportation_mode, weekly_distance=None,
                       size=None, fuel_type=None, occupancy=None, passengers=None, work_weeks=None):
    """
    Calculate co2 emissions for commuting per mode of transport
    :param transportation_mode: [car, bus, train, bicycle, pedelec, motorbike, tram]
    :param weekly_distance: distance in km per week
    :param size: size of car or bus if applicable: [small, medium, large, average]
    :param fuel_type: fuel type of car, bus or train if applicable
    :param occupancy: occupancy [%], if applicable/known (only for bus): [20, 50, 80, 100]
    :param passengers: number of passengers, if applicable (only for car)
    :param work_weeks: number of working weeks per year,
                i.e., 52 (weeks per year) - 4 (paid leave) - 2 (public holidays) = 42
                or number of working weeks per month
                i.e., 4 (or 4.4) (or only 2 if on leave etc.)
    :return: total emissions for the given number of weeks and the respective mode of transport
    """
    # get weekly co2e for respective mode of transport
    if transportation_mode == "car":
        weekly_co2e = calc_co2_car(passengers=passengers, size=size, fuel_type=fuel_type, distance=weekly_distance)
    elif transportation_mode == "motorbike":
        weekly_co2e = calc_co2_motorbike(size=size, distance=weekly_distance)
    elif transportation_mode == "bus":
        weekly_co2e = calc_co2_bus(size=size, fuel_type=fuel_type, occupancy=occupancy, vehicle_range="average",
                                   distance=weekly_distance)
    elif transportation_mode == "train":
        calc_co2_train(fuel_type=fuel_type, vehicle_range="local", distance=weekly_distance)
    elif transportation_mode == "tram":
        co2e = emission_factor_df[(emission_factor_df["name"] == "Strassen-Stadt-U-Bahn")]["co2e"].values[0]
        weekly_co2e = co2e * weekly_distance
    elif transportation_mode == "pedelec" or transportation_mode == "bicycle":
        co2e = emission_factor_df[(emission_factor_df["subcategory"] == transportation_mode)]["co2e"].values[0]
        weekly_co2e = co2e * weekly_distance

    # multiply with work_weeks to obtain total (e.g. annual/monthly) co2e
    total_co2e = weekly_co2e * work_weeks

    return total_co2e


def commuting_emissions_group(aggr_co2, n_participants, n_members):
    """
    Calculate the group's co2e emissions from commuting.
    Assumption: a representative sample of group members answered the questionnaire.
    :param aggr_co2: (Annual/monthly) co2e emissions from commuting, aggregated for all group members who answered the
                            questionnaire (can also be calculated for only one mode of transport)
    :param n_participants: Number of group members who answered the questionnaire
    :param n_members: Total number of members of the group
    :return:
    """
    group_co2e = aggr_co2 / n_participants * n_members

    return group_co2e

