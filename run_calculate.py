#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
description
"""


import os
import pandas as pd
import numpy as np
import glob
from co2calculator import calc_co2_businesstrip, calc_co2_heating, calc_co2_electricity
from co2calculator.distances import geocoding_structured

script_path = os.path.dirname(os.path.realpath(__file__))


if __name__ == "__main__":

    """# test with dummy data
    business_trip_data = glob.glob(f"{script_path}/data/test_data_users/business_trips*.csv")

    print("Computing business trip emissions...")
    for f in business_trip_data:
        user_data = pd.read_csv(f, sep=";")
        for i in range(user_data.shape[0]):
            if "_car" in f:
                distance = user_data["distance_km"].values[i]
                size_class = user_data["car_size"].values[i]
                fuel_type = user_data["car_fuel"].values[i]
                passengers = user_data["passengers"].values[i]
                if np.isnan(distance):
                    distance = None
                    start = str(user_data["stops"].values[i]).split("-")[0]
                    dest = str(user_data["stops"].values[i]).split("-")[1]
                else:
                    start = None
                    dest = None
                roundtrip = bool(user_data["roundtrip"].values[i])
                total_co2e = calc_co2_businesstrip("car", passengers=passengers, size=size_class,
                                                   fuel_type=fuel_type, distance=distance, start=start,
                                                   destination=dest, roundtrip=roundtrip)
                user_data.loc[i, "co2e_kg"] = total_co2e
            elif "_bus" in f:
                distance = user_data["distance_km"].values[i]
                size_class = user_data["bus_size"].values[i]
                fuel_type = user_data["bus_fuel"].values[i]
                occupancy = user_data["occupancy"].values[i]
                roundtrip = bool(user_data["roundtrip"].values[i])
                if np.isnan(distance):
                    distance = None
                    start = str(user_data["stops"].values[i]).split("-")[0]
                    dest = str(user_data["stops"].values[i]).split("-")[1]
                else:
                    start = None
                    dest = None
                total_co2e = calc_co2_businesstrip("bus", size=size_class, fuel_type=fuel_type, occupancy=occupancy,
                                                   distance=distance, start=start,
                                                   destination=dest, roundtrip=roundtrip)
                user_data.loc[i, "co2e_kg"] = total_co2e
            elif "_train" in f:
                distance = user_data["distance_km"].values[i]
                fuel_type = user_data["train_fuel"].values[i]
                roundtrip = bool(user_data["roundtrip"].values[i])
                if np.isnan(distance):
                    distance = None
                    start = str(user_data["stops"].values[i]).split("-")[0]
                    dest = str(user_data["stops"].values[i]).split("-")[1]
                else:
                    start = None
                    dest = None
                total_co2e = calc_co2_businesstrip("train", fuel_type=fuel_type, distance=distance, start=start,
                                                   destination=dest, roundtrip=roundtrip)
                user_data.loc[i, "co2e_kg"] = total_co2e
            elif "_plane" in f:
                iata_start = user_data["IATA_start"].values[i]
                iata_dest = user_data["IATA_destination"].values[i]
                flight_class = user_data["flight_class"].values[i]
                roundtrip = bool(user_data["roundtrip"].values[i])
                total_co2e = calc_co2_businesstrip("plane", start=iata_start, destination=iata_dest,
                                                   roundtrip=roundtrip, seating=flight_class)
                user_data.loc[i, "co2e_kg"] = total_co2e
            elif "_ferry" in f:
                start = user_data["start"].values[i]
                dest = user_data["destination"].values[i]
                seating = user_data["seating_class"].values[i]
                roundtrip = bool(user_data["roundtrip"].values[i])
                total_co2e = calc_co2_businesstrip("ferry", start=start, destination=dest,
                                                   roundtrip=roundtrip, seating=seating)
                user_data.loc[i, "co2e_kg"] = total_co2e

            print("Writing file: %s" % f.replace(".csv", "_calc.csv"))
            # user_data.to_csv(f.replace(".csv", "_calc.csv"), sep=";", index=False)

    electricity_data = glob.glob(f"{script_path}/data/test_data_users/electricity.csv")

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

    heating_data = glob.glob(f"{script_path}/data/test_data_users/heating.csv")

    print("Computing heating emissions...")
    for f in heating_data:
        user_data = pd.read_csv(f, sep=";")
        for i in range(user_data.shape[0]):
            consumption = user_data["consumption"].values[i]
            unit = user_data["energy_unit"].values[i]
            fuel_type = user_data["fuel_type"].values[i]
            total_co2e = calc_co2_heating(consumption, unit, fuel_type)
            user_data.loc[i, "co2e_kg"] = total_co2e

            print("Writing file: %s" % f.replace(".csv", "_calc.csv"))
            # user_data.to_csv(f.replace(".csv", "_calc.csv"), sep=";", index=False)"""

    name, country, coords, res = geocoding_structured(postalcode="69181")
    print(name, country, coords)
    print(res)