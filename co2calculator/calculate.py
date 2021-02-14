#!/usr/bin/env python

"""Functions to calculate co2 emissions"""

import os
import pandas as pd
import glob


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


def calc_co2_building(consumption, co2e):
    #co2 equivalents for heating and electricity refer to a consumption of 1 TJ
    #so consumption needs to be converted to TJ
    emissions = consumption/277777.77777778 * co2e

    return emissions


"""def calc_co2_plane(start, destination, flight_class, roundtrip=False):
    json = {
      "from": start,
      "to": destination,
      "roundtrip": roundtrip,
      "flight_class": flight_class
    }
    response = requests.post("https://api.myclimate.org/v1/flight_calculators.json")
    print(response)
    if response:
        print("success")
    else:
        print("meh")
    response = requests.post("https://api.myclimate.org/v1/flight_calculators.json", json=json)
    if response:
        print("success")
    else:
        print("meh")"""


# test with dummy data
business_trip_data = glob.glob("../data/test_data_users/business_trips*.csv")

print("Computing business trip emissions...")
for f in business_trip_data:
    user_data = pd.read_csv(f)
    for i in range(user_data.shape[0]):
        distance = user_data["distance_km"].values[i]
        if "_car" in f:
            size_class = user_data["car_size"].values[i]
            fuel_type = user_data["car_fuel"].values[i]
            passengers = user_data["passengers"].values[i]
            co2e = query_co2e_car(size_class, fuel_type)
            total_co2e = calc_co2_car(distance, passengers, co2e)
            user_data.loc[i, "co2e_kg"] = total_co2e
        elif "_bus" in f:
            size_class = user_data["bus_size"].values[i]
            fuel_type = user_data["bus_fuel"].values[i]
            occupancy = user_data["occupancy"].values[i]
            co2e = query_co2e_bus(size_class, fuel_type, occupancy)
            total_co2e = calc_co2_public_transport(distance, co2e)
            user_data.loc[i, "co2e_kg"] = total_co2e
        elif "_train" in f:
            fuel_type = user_data["train_fuel"].values[i]
            co2e = query_co2e_train(fuel_type)
            total_co2e = calc_co2_public_transport(distance, co2e)
            user_data.loc[i, "co2e_kg"] = total_co2e

        print("Writing file: %s" % f.replace(".csv", "_calc.csv"))
        user_data.to_csv(f.replace(".csv", "_calc.csv"))


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
        user_data.to_csv(f.replace(".csv", "_calc.csv"))

heating_data = glob.glob("../data/test_data_users/heating.csv")

print("Computing heating emissions...")
for f in heating_data:
    user_data = pd.read_csv(f)
    for i in range(user_data.shape[0]):
        consumption = user_data["consumption_kwh"].values[i]
        fuel_type = user_data["fuel_type"].values[i]
        co2e = query_co2e_heating(fuel_type)
        total_co2e = calc_co2_building(consumption, co2e)
        user_data.loc[i, "co2e_kg"] = total_co2e

        print("Writing file: %s" % f.replace(".csv", "_calc.csv"))
        user_data.to_csv(f.replace(".csv", "_calc.csv"))