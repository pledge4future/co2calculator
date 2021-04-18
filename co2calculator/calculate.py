#!/usr/bin/env python

"""Functions to calculate co2 emissions"""

import os
import pandas as pd
import glob
import numpy as np
from co2calculator.distances import *

KWH_TO_TJ = 277777.77777778
script_path = os.path.dirname(os.path.realpath(__file__))
data = pd.read_csv(f"{script_path}/../data/emission_factors.csv")


def calc_co2_car(passengers, size, fuel_type, distance=None, locations=None, roundtrip=False):
    """
    Function to compute the emissions of a car trip.
    :param passengers: Number of passengers in the car (including the person answering the questionnaire),
                        [1, 9]
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

    :return: Total emissions of trip
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
    co2e = data[(data["size_class"] == size) & (data["fuel_type"] == fuel_type)]["co2e_kg"].values[0]
    if roundtrip is True:
        distance *= 2
    emissions = distance * co2e / passengers

    return emissions


def calc_co2_bus(size="average", fuel_type="average", occupancy=50, distance=None, stops=None, roundtrip=False):
    """
    Function to compute the emissions of a bus trip.
    :param size: size class of the bus;                 ["medium", "large", "average"]
    :param fuel_type: type of fuel the bus is using;    ["diesel"]
    :param occupancy: number of people on the bus       [20, 50, 80, 100]          Todo: 50 as default?
    :param distance: Distance travelled in km;
                        alternatively param <stops> can be provided
    :param stops: List of locations, ideally in the form 'address, locality, country';
                    alternatively param <distance> can be provided
    :param roundtrip: Whether this trip is a roundtrip or not; Boolean [True, False]
    :return: Total emissions of trip
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
        for i in range(len(coords) - 1):
            # compute great circle distance between locations
            distance += haversine(coords[i][1], coords[i][0], coords[i + 1][1], coords[i + 1][0])
        distance *= detour_coefficient
    if roundtrip is True:
        distance *= 2
    co2e = data[(data["size_class"] == size) & (data["fuel_type"] == fuel_type) & [data["occupancy"] == occupancy]]["co2e_kg"].values[0]
    emissions = distance * co2e

    return emissions


def calc_co2_train(fuel_type="average", distance=None, train_stations=None, roundtrip=False):
    """
    Function to compute the emissions of a bus trip.
    :param fuel_type: type of fuel the train is using;    ["diesel", "electric", "average"]
    :param distance: Distance travelled in km;
                        alternatively param <stops> can be provided
    :param train_stations: List of train stations, ideally in the form 'address, locality, country';
                    alternatively param <distance> can be provided
    :param roundtrip: Whether this trip is a roundtrip or not; Boolean [True, False]
    :return: Total emissions of trip
    """
    detour_coefficient = 1.2
    if distance is None and train_stations is None:
        print("Warning! Travel parameters missing. Please provide either the distance in km or a list of"
              "travelled train stations in the form 'address, locality, country'")
    elif distance is None: #and train_stations is not None:
        distance = 0
        coords = []
        for loc in train_stations:
            loc_name, loc_country, loc_coords = geocoding(loc)
            coords.append(loc_coords)
        for i in range(len(coords)-1):
            # compute great circle distance between locations
            distance += haversine(coords[i][1], coords[i][0], coords[i+1][1], coords[i+1][0])
        distance *= detour_coefficient
    if roundtrip is True:
        distance *= 2
    co2e = data[(data["fuel_type"] == fuel_type)]["co2e_kg"].values[0]
    emissions = distance * co2e

    return emissions


def calc_co2_plane(start, destination, roundtrip):
    """
    Function to compute emissions of a train trip
    :param start: IATA code of start airport
    :param destination: IATA code of destination airport
    :param roundtrip: Whether this trip is a roundtrip or not; Boolean [True, False]
    :return: Total emissions of flight
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
        co2e = data[(data["range"] == "inland")]["co2e_kg"].values[0]
    else:
        co2e = data[(data["range"] == "international")]["co2e_kg"].values[0]
    # multiply emission factor with distance and by 2 if roundtrip
    emissions = distance * co2e
    if roundtrip is True:
        emissions *= 2

    return emissions


def calc_co2_electricity(consumption, fuel_type):
    co2e = data[(data["type"] == fuel_type)]["co2e_kg"].values[0]
    # co2 equivalents for heating and electricity refer to a consumption of 1 TJ
    # so consumption needs to be converted to TJ
    emissions = consumption/KWH_TO_TJ * co2e

    return emissions


def calc_co2_heating(consumption, fuel_type):
    co2e = data[(data["type"] == fuel_type)]["co2e_kg"].values[0]
    # co2 equivalents for heating and electricity refer to a consumption of 1 TJ
    # so consumption needs to be converted to TJ
    emissions = consumption/KWH_TO_TJ * co2e

    return emissions


if __name__ == "__main__":

    # test with dummy data
    business_trip_data = glob.glob(f"{script_path}/../data/test_data_users/business_trips*.csv")

    print("Computing business trip emissions...")
    for f in business_trip_data:
        user_data = pd.read_csv(f, sep=";")
        for i in range(user_data.shape[0]):
            if "_car" in f:
                distance = user_data["distance_km"].values[i]
                size_class = user_data["car_size"].values[i]
                fuel_type = user_data["car_fuel"].values[i]
                passengers = user_data["passengers"].values[i]
                stops = str(user_data["stops"].values[i]).split("-")
                if np.isnan(distance):
                    distance = None
                if stops is np.nan:
                    stops = None
                roundtrip = bool(user_data["roundtrip"].values[i])
                total_co2e = calc_co2_car(passengers, size_class, fuel_type, distance, stops, roundtrip)
                user_data.loc[i, "co2e_kg"] = total_co2e
            elif "_bus" in f:
                distance = user_data["distance_km"].values[i]
                size_class = user_data["bus_size"].values[i]
                fuel_type = user_data["bus_fuel"].values[i]
                occupancy = user_data["occupancy"].values[i]
                stops = str(user_data["stops"].values[i]).split("-")
                roundtrip = bool(user_data["roundtrip"].values[i])
                if np.isnan(distance):
                    distance = None
                if stops is np.nan:
                    stops = None
                total_co2e = calc_co2_bus(size_class, fuel_type, occupancy, distance, stops, roundtrip)
                user_data.loc[i, "co2e_kg"] = total_co2e
            elif "_train" in f:
                distance = user_data["distance_km"].values[i]
                fuel_type = user_data["train_fuel"].values[i]
                roundtrip = bool(user_data["roundtrip"].values[i])
                stops = str(user_data["stops"].values[i]).split("-")
                if np.isnan(distance):
                    distance = None
                if stops is np.nan:
                    stops = None
                total_co2e = calc_co2_train(fuel_type, distance, stops, roundtrip)
                user_data.loc[i, "co2e_kg"] = total_co2e
            elif "_plane" in f:
                iata_start = user_data["IATA_start"].values[i]
                iata_dest = user_data["IATA_destination"].values[i]
                # flight_class = user_data["flight_class"].values[i]
                roundtrip = bool(user_data["roundtrip"].values[i])
                total_co2e = calc_co2_plane(iata_start, iata_dest, roundtrip)
                user_data.loc[i, "co2e_kg"] = total_co2e

            print("Writing file: %s" % f.replace(".csv", "_calc.csv"))
            # user_data.to_csv(f.replace(".csv", "_calc.csv"), sep=";", index=False)


    electricity_data = glob.glob(f"{script_path}/../data/test_data_users/electricity.csv")

    print("Computing electricity emissions...")
    for f in electricity_data:
        user_data = pd.read_csv(f, sep=";")
        for i in range(user_data.shape[0]):
            consumption = user_data["consumption_kwh"].values[i]
            fuel_type = user_data["fuel_type"].values[i]
            total_co2e = calc_co2_electricity(consumption, fuel_type)
            user_data.loc[i, "co2e_kg"] = total_co2e

            print("Writing file: %s" % f.replace(".csv", "_calc.csv"))
            # user_data.to_csv(f.replace(".csv", "_calc.csv"), sep=";")

    heating_data = glob.glob(f"{script_path}/../data/test_data_users/heating.csv")

    print("Computing heating emissions...")
    for f in heating_data:
        user_data = pd.read_csv(f, sep=";")
        for i in range(user_data.shape[0]):
            if user_data["consumption_kwh"].values[i] > 0:
                consumption_kwh = user_data["consumption_kwh"].values[i]
            elif user_data["consumption_l"].values[i] > 0:
                consumption_l = user_data["consumption_l"].values[i]
                consumption_kwh = 0
                consumption_kg = 0
            elif user_data["consumption_kg"].values[i] > 0:
                consumption_kg = user_data["consumption_kg"].values[i]
                consumption_kwh = 0
                consumption_l = 0

            fuel_type = user_data["fuel_type"].values[i]
            if consumption_kwh > 0:
                total_co2e = calc_co2_heating(consumption_kwh, fuel_type)
            elif consumption_l > 0:
                if fuel_type == "oil":
                    total_co2e = calc_co2_heating(consumption_l, fuel_type)*10
                elif fuel_type == "liquid_gas":
                    total_co2e = calc_co2_heating(consumption_l, fuel_type)*6.6
            elif consumption_kg > 0:
                if fuel_type == "coal":
                    total_co2e = calc_co2_heating(consumption_kg, fuel_type)*4.17
                elif fuel_type == "pellet":
                    total_co2e = calc_co2_heating(consumption_kg, fuel_type)*5
                elif fuel_type == "woodchips":
                    total_co2e = calc_co2_heating(consumption_kg, fuel_type)*4
            user_data.loc[i, "co2e_kg"] = total_co2e

            print("Writing file: %s" % f.replace(".csv", "_calc.csv"))
            # user_data.to_csv(f.replace(".csv", "_calc.csv"), sep=";", index=False)
