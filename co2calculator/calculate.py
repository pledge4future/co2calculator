#!/usr/bin/env python

"""Functions to calculate co2 emissions"""

import os
import pandas as pd
import glob
import requests


KWH_TO_TJ = 277777.77777778
script_path = os.path.dirname(os.path.realpath(__file__))


def query_co2e_car(car_size, car_fuel):
    data = pd.read_csv("../data/emission_factors_car.csv")
    co2e = data[(data["size_class"] == car_size) & (data["fuel_type"] == car_fuel)]["co2e_kg"].values[0]

    return co2e


def query_co2e_train(train_fuel):
    data = pd.read_csv("../data/emission_factors_train.csv")
    co2e = data[(data["fuel_type"] == train_fuel)]["co2e_kg"].values[0]

    return co2e


def query_co2e_bus(bus_size, bus_fuel, occupancy):
    data = pd.read_csv("../data/emission_factors_bus.csv")
    index = (data["size_class"] == bus_size) & (data["fuel_type"] == bus_fuel) & (data["occupancy"] == occupancy)
    co2e = data[index]["co2e_kg"].values[0]

    return co2e

def query_co2e_heating(fuel_type):
    data = pd.read_csv("../data/emission_factors_heating.csv")
    co2e = data[(data["type"] == fuel_type)]["co2e_kg"].values[0]

    return co2e

def query_co2e_electricity(fuel_type):
    data = pd.read_csv("../data/emission_factors_electricity.csv")
    co2e = data[(data["type"] == fuel_type)]["co2e_kg"].values[0]

    return co2e



def calc_co2_car(distance, passengers, co2e):
    emissions = distance * co2e / passengers

    return emissions


def calc_co2_public_transport(distance, co2e):
    emissions = distance * co2e

    return emissions


def calc_co2_electricity(consumption, fuel_type):
    co2e = query_co2e_electricity(fuel_type)
    #co2 equivalents for heating and electricity refer to a consumption of 1 TJ
    #so consumption needs to be converted to TJ
    emissions = consumption/KWH_TO_TJ * co2e

    return emissions


def calc_co2_heating(consumption, fuel_type):
    co2e = query_co2e_heating(fuel_type)
    #co2 equivalents for heating and electricity refer to a consumption of 1 TJ
    #so consumption needs to be converted to TJ
    emissions = consumption/KWH_TO_TJ * co2e

    return emissions


def calc_co2_plane(start, destination, flight_class, roundtrip=False):
    #flight classes: economy, premium_economy, business, first
    key = ("API_key_here", "")
    parameters = {
      "segments[0][origin]": start,
      "segments[0][destination]": destination,
      "cabin_class": flight_class
    }
    if roundtrip == True:
        parameters["segments[1][origin]"] = destination
        parameters["segments[1][destination]"] = start
    response = requests.get("https://api.goclimate.com/v1/flight_footprint", auth=key, params=parameters)
    if response:
        print("success")
    else:
        print(response.status_code)

    return int(response.json()["footprint"])


if __name__ == "__main__":

    # test with dummy data
    business_trip_data = glob.glob("../data/test_data_users/business_trips*.csv")

    print("Computing business trip emissions...")
    for f in business_trip_data:
        user_data = pd.read_csv(f)
        for i in range(user_data.shape[0]):
            if "_car" in f:
                distance = user_data["distance_km"].values[i]
                size_class = user_data["car_size"].values[i]
                fuel_type = user_data["car_fuel"].values[i]
                passengers = user_data["passengers"].values[i]
                co2e = query_co2e_car(size_class, fuel_type)
                total_co2e = calc_co2_car(distance, passengers, co2e)
                user_data.loc[i, "co2e_kg"] = total_co2e
            elif "_bus" in f:
                distance = user_data["distance_km"].values[i]
                size_class = user_data["bus_size"].values[i]
                fuel_type = user_data["bus_fuel"].values[i]
                occupancy = user_data["occupancy"].values[i]
                co2e = query_co2e_bus(size_class, fuel_type, occupancy)
                total_co2e = calc_co2_public_transport(distance, co2e)
                user_data.loc[i, "co2e_kg"] = total_co2e
            elif "_train" in f:
                distance = user_data["distance_km"].values[i]
                fuel_type = user_data["train_fuel"].values[i]
                co2e = query_co2e_train(fuel_type)
                total_co2e = calc_co2_public_transport(distance, co2e)
                user_data.loc[i, "co2e_kg"] = total_co2e
            elif "_plane" in f:
                iata_start = user_data["IATA_start"].values[i]
                iata_dest = user_data["IATA_destination"].values[i]
                flight_class = user_data["flight_class"].values[i]
                roundtrip = bool(user_data["roundtrip"].values[i])
                total_co2e = calc_co2_plane(iata_start, iata_dest, flight_class, roundtrip)
                user_data.loc[i, "co2e_kg"] = total_co2e

            print("Writing file: %s" % f.replace(".csv", "_calc.csv"))
            #user_data.to_csv(f.replace(".csv", "_calc.csv"))


    electricity_data = glob.glob("../data/test_data_users/electricity.csv")

    print("Computing electricity emissions...")
    for f in electricity_data:
        user_data = pd.read_csv(f)
        for i in range(user_data.shape[0]):
            consumption = user_data["consumption_kwh"].values[i]
            fuel_type = user_data["fuel_type"].values[i]
            co2e = query_co2e_electricity(fuel_type)
            total_co2e = calc_co2_building(consumption, co2e)
            user_data.loc[i, "co2e_kg"] = total_co2e

            print("Writing file: %s" % f.replace(".csv", "_calc.csv"))
            #user_data.to_csv(f.replace(".csv", "_calc.csv"))

    heating_data = glob.glob("../data/test_data_users/heating.csv")

    print("Computing heating emissions...")
    for f in heating_data:
        user_data = pd.read_csv(f)
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
            co2e = query_co2e_heating(fuel_type)
            if consumption_kwh > 0:
                total_co2e = calc_co2_building(consumption_kwh, co2e)
            elif consumption_l > 0:
                if fuel_type == "oil":
                    total_co2e = calc_co2_building(consumption_l, co2e)*10
                elif fuel_type == "liquid_gas":
                    total_co2e = calc_co2_building(consumption_l, co2e)*6.6
            elif consumption_kg > 0:
                if fuel_type == "coal":
                    total_co2e = calc_co2_building(consumption_kg, co2e)*4.17
                elif fuel_type == "pellet":
                    total_co2e = calc_co2_building(consumption_kg, co2e)*5
                elif fuel_type == "woodchips":
                    total_co2e = calc_co2_building(consumption_kg, co2e)*4
            user_data.loc[i, "co2e_kg"] = total_co2e

            print("Writing file: %s" % f.replace(".csv", "_calc.csv"))
            #user_data.to_csv(f.replace(".csv", "_calc.csv"))