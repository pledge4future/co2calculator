#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Enums holding parameter choices derived from data set"""

__author__ = "Christina Ludwig, GIScience Research Group, Heidelberg University"
__email__ = "christina.ludwig@uni-heidelberg.de"

from enum import Enum
import pandas as pd
from pathlib import Path
import numpy as np

script_path = str(Path(__file__).parent)


class EnumCreator:

    def __init__(self):
        self.df = pd.read_csv(f"{script_path}/../data/emission_factors.csv")

    def create_enum(self, mode, column, name):
        df = self.df[self.df["subcategory"] == mode]
        if df[column].dtype == np.float64:
            data = df[column].map(lambda x: "c_{:.0f}".format(x)).astype("str")
            return Enum(name, {x: float(x[2:]) for x in data}, type=str)
        else:
            data = df[column].fillna("nan").unique()
            return Enum(name, {x.capitalize().replace("-", "_"): x for x in data}, type=str)

    def create_enum_transport(self, column, name):
        data = self.df[column].fillna("nan").astype("str").unique()
        return Enum(name, {x.capitalize(): x for x in data}, type=str)


enum_creator = EnumCreator()
TransportationMode = enum_creator.create_enum_transport("subcategory", "TransportationMode")

# Fuel types ------------------------------------------------------

TrainFuelType = enum_creator.create_enum(TransportationMode.Train,
                            "fuel_type",
                            "TrainFuelType")
CarFuelType = enum_creator.create_enum(TransportationMode.Car,
                            "fuel_type",
                          "CarFuelType")
BusFuelType = enum_creator.create_enum(TransportationMode.Bus,
                            "fuel_type",
                          "BusFuelType")
TramFuelType = enum_creator.create_enum(TransportationMode.Tram,
                            "fuel_type", "TramFuelType")
PlaneFuelType = enum_creator.create_enum(TransportationMode.Plane,
                            "fuel_type",
                            "PlaneFuelType")
FerryFuelType = enum_creator.create_enum(TransportationMode.Ferry,
                            "fuel_type",
                            "FerryFuelType")
BicycleFuelType = enum_creator.create_enum(TransportationMode.Bicycle,
                            "fuel_type",
                              "BicycleFuelType")
PedelecFuelType = enum_creator.create_enum(TransportationMode.Pedelec,
                            "fuel_type",
                              "PedelecFuelType")

# Size
TrainSize = enum_creator.create_enum(TransportationMode.Train,
                            "size",
                            "TrainSize")
CarSize = enum_creator.create_enum(TransportationMode.Car,
                            "size",
                          "CarSize")
BusSize = enum_creator.create_enum(TransportationMode.Bus,
                            "size",
                          "BusSize")
MotorbikeSize = enum_creator.create_enum(TransportationMode.Motorbike,
                            "size",
                          "MotorbikeSize")
TramSize = enum_creator.create_enum(TransportationMode.Tram,
                            "size",
                            "TramSize")

# Vehicle range
TrainRange = enum_creator.create_enum(TransportationMode.Train,
                            "range",
                            "TrainRange")
BusRange = enum_creator.create_enum(TransportationMode.Bus,
                            "range",
                          "BusRange")

PlaneRange = enum_creator.create_enum(TransportationMode.Plane,
                            "range",
                          "PlaneRange")

# Seating class
PlaneSeatingClass = enum_creator.create_enum(TransportationMode.Plane,
                            "seating",
                            "PlaneSeatingClass")
FerrySeatingClass = enum_creator.create_enum(TransportationMode.Ferry,
                            "seating",
                          "FerrySeatingClass")

# Occupancy
TrainOccupancy = enum_creator.create_enum(TransportationMode.Train,
                            "occupancy",
                            "TrainOccupancy")
BusOccupancy = enum_creator.create_enum( TransportationMode.Bus,
                            "occupancy",
                            "BusOccupancy")