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


def calc_co2_car(distance, passengers, co2e):
    emissions = distance * co2e / passengers

    return emissions


def calc_co2_public_transport(distance, co2e):
    emissions = distance * co2e

    return emissions

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