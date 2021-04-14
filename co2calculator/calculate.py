#!/usr/bin/env python

"""Functions to calculate co2 emissions"""

import os
import pandas as pd
import glob
import numpy as np
import openrouteservice
from openrouteservice.directions import directions
from openrouteservice.geocode import pelias_search, pelias_autocomplete, pelias_structured

KWH_TO_TJ = 277777.77777778
script_path = os.path.dirname(os.path.realpath(__file__))
key_file = f"{script_path}/../key.txt"
with open(key_file) as f:
    api_key = f.read().strip()


def query_co2e_car(car_size, car_fuel):
    data = pd.read_csv(f"{script_path}/../data/emission_factors_car.csv")
    co2e = data[(data["size_class"] == car_size) & (data["fuel_type"] == car_fuel)]["co2e_kg"].values[0]

    return co2e


def query_co2e_train(train_fuel):
    data = pd.read_csv(f"{script_path}/../data/emission_factors_train.csv")
    co2e = data[(data["fuel_type"] == train_fuel)]["co2e_kg"].values[0]

    return co2e


def query_co2e_bus(bus_size, bus_fuel, occupancy):
    data = pd.read_csv(f"{script_path}/../data/emission_factors_bus.csv")
    index = (data["size_class"] == bus_size) & (data["fuel_type"] == bus_fuel) & (data["occupancy"] == occupancy)
    co2e = data[index]["co2e_kg"].values[0]

    return co2e


def query_co2e_heating(fuel_type):
    data = pd.read_csv(f"{script_path}/../data/emission_factors_heating.csv")
    co2e = data[(data["type"] == fuel_type)]["co2e_kg"].values[0]

    return co2e


def query_co2e_electricity(fuel_type):
    data = pd.read_csv(f"{script_path}/../data/emission_factors_electricity.csv")
    co2e = data[(data["type"] == fuel_type)]["co2e_kg"].values[0]

    return co2e


def query_co2e_plane(inland):  # inland is a boolean
    data = pd.read_csv(f"{script_path}/../data/emission_factors_plane.csv")
    if inland is True:
        co2e = data[(data["type"] == "plane inland")]["co2e_kg"].values[0]
    elif inland is False:
        co2e = data[(data["type"] == "plane international")]["co2e_kg"].values[0]

    return co2e


def great_circle_distance(lat_start, long_start, lat_dest, long_dest):
    # convert angles from degree to radians
    lat_start, long_start, lat_dest, long_dest = np.deg2rad([lat_start, long_start, lat_dest, long_dest])
    # compute zeta
    zeta = np.arccos(
        np.sin(lat_start) * np.sin(lat_dest) + np.cos(lat_start) * np.cos(lat_dest) * np.cos(long_dest-long_start)
    )
    r = 6371  # earth radius in km

    return zeta * r  # distance in km


def haversine(lat_start, long_start, lat_dest, long_dest):
    """
    Function to compute the distance as the crown flies between given locations
    :param lat_start: latitude of Start
    :param long_start: Longitude of Start
    :param lat_dest: Latitude of Destination
    :param long_dest: Longitude of Destination
    :return: Distance in km
    """
    # convert angles from degree to radians
    lat_start, long_start, lat_dest, long_dest = np.deg2rad([lat_start, long_start, lat_dest, long_dest])
    # compute zeta
    a = np.sin((lat_dest - lat_start)/2)**2 + np.cos(lat_start) * np.cos(lat_dest) * np.sin((long_dest - long_start)/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    r = 6371

    return c * r  # distance in km


def calc_co2_car(passengers, size, fuel_type, distance=None, locations=None, roundtrip=False):
    """
    Function to compute the emissions of a car trip.
    :param passengers: Number of passengers in the car (including the person answering the questionnaire),
                        [1, 9]
    :param size: size of car
                        ["small", "medium", "large"]
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
    elif distance is None: # and locations is not None:
        coords = []
        for loc in locations:
            loc_name, loc_country, loc_coords = geocoding(loc)
            coords.append(loc_coords)
        distance = get_route(coords, "driving-car")
    co2e = query_co2e_car(size, fuel_type)
    if roundtrip is True:
        distance *= 2
    emissions = distance * co2e / passengers

    return emissions


def calc_co2_bus(size, fuel_type, occupancy, distance=None, stops=None, roundtrip=False):
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
    co2e = query_co2e_bus(size, fuel_type, occupancy)
    emissions = distance * co2e

    return emissions


def calc_co2_train(fuel_type, distance=None, train_stations=None, roundtrip=False):
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
    co2e = query_co2e_train(fuel_type)
    emissions = distance * co2e

    return emissions


def calc_co2_electricity(consumption, fuel_type):
    co2e = query_co2e_electricity(fuel_type)
    # co2 equivalents for heating and electricity refer to a consumption of 1 TJ
    # so consumption needs to be converted to TJ
    emissions = consumption/KWH_TO_TJ * co2e

    return emissions


def calc_co2_heating(consumption, fuel_type):
    co2e = query_co2e_heating(fuel_type)
    # co2 equivalents for heating and electricity refer to a consumption of 1 TJ
    # so consumption needs to be converted to TJ
    emissions = consumption/KWH_TO_TJ * co2e

    return emissions


def geocoding_airport(iata):
    """
    Function to obtain the coordinates of an airport by the IATA code
    :param iata: IATA airport code
    :return: name, coordinates and country of the found airport
    """
    clnt = openrouteservice.Client(key=api_key)

    call = pelias_search(clnt, "%s Airport" % iata)

    for feature in call["features"]:
        if feature["properties"]["addendum"]["osm"]["iata"] == iata:
            name = feature["properties"]["name"]
            geom = feature["geometry"]["coordinates"]
            country = feature["properties"]["country"]
            break

    return name, geom, country


def geocoding(address):
    """
    Function to obtain coordinates for a given address
    :param address: Location/Address to be searched
            user should give address in the form:
            <adress>, <locality>, <country>
            e.g. Hauptbahnhof, Heidelberg, Germany
            e.g. Im Neuenheimer Feld 348, Heidelberg, Germany
            e.g. Heidelberg, Germany
    :return: Name, country and coordinates of the found location
    """
    # alternatively: structured geocoding, user has several input fields: country, locality, postalcode, address
    clnt = openrouteservice.Client(key=api_key)

    call = pelias_search(clnt, address)
    for feature in call["features"]:
        name = feature["properties"]["name"]
        country = feature["properties"]["country"]
        coords = feature["geometry"]["coordinates"]
        break

    return name, country, coords


def geocoding(address):
    """
    Function to obtain coordinates for a given address
    :param address: Location/Address to be searched
            user should give address in the form:
            <adress>, <locality>, <country>
            e.g. Hauptbahnhof, Heidelberg, Germany
            e.g. Im Neuenheimer Feld 348, Heidelberg, Germany
            e.g. Heidelberg, Germany
    :return: Name, country and coordinates of the found location
    """
    # alternatively: structured geocoding, user has several input fields: country, locality, postalcode, address
    clnt = openrouteservice.Client(key=api_key)

    call = pelias_search(clnt, address)
    for feature in call["features"]:
        name = feature["properties"]["name"]
        country = feature["properties"]["country"]
        coords = feature["geometry"]["coordinates"]
        break

    return name, country, coords


def get_route(coords, profile=None):
    """
    Obtain the distance of a route between given waypoints using a given profile
    :param coords: list of [lat,long] coordinate-lists
    :param profile: driving-car, cycling-regular
    :return: distance of the route
    """
    # coords: list of [lat,long] lists
    # profile may be: driving-car, cycling-regular
    clnt = openrouteservice.Client(key=api_key)

    allowed_profiles = ["driving-car", "cycling-regular"]
    if profile not in allowed_profiles or profile is None:
        print("Warning! Specified profile not available or no profile passed.\n"
              "Profile set to 'driving-car' by default.")
        profile = "driving-car"
    route = directions(clnt, coords, profile=profile)
    dist = route["routes"][0]["summary"]["distance"]

    return dist


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
    # retrieve whether airports are in the same country
    if country_start == country_dest:
        is_inland_flight = True
    else:
        is_inland_flight = False
    # query emission factor (based on inland or international flight)
    co2e = query_co2e_plane(is_inland_flight)
    # multiply emission factor with distance and by 2 if roundtrip
    emissions = distance * co2e
    if roundtrip is True:
        emissions *= 2

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
            user_data.to_csv(f.replace(".csv", "_calc.csv"), sep=";", index=False)


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
            user_data.to_csv(f.replace(".csv", "_calc.csv"), sep=";")

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
            user_data.to_csv(f.replace(".csv", "_calc.csv"), sep=";", index=False)
