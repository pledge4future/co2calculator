#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Constant variables and enums"""

import enum

KWH_TO_TJ = 277777.77777778


class CommutingTransportationMode(enum.Enum):
    CAR = 'Car'
    BUS = 'Bus'
    TRAIN = 'Train'
    BICYCLE = 'Bicycle'
    EBIKE = 'E-bike'
    MOTORBIKE = 'Motorbike'
    TRAM = 'Tram'


class HeatingFuel(enum.Enum):
    """Enum for heating fuel types"""

    HEAT_PUMP_AIR = "heat_pump_air"
    HEAT_PUMP_GROUND = "heat_pump_ground"
    HEAT_PUMP_WATER = "heat_pump_water"
    LIQUID_GAS = "liquid_gas"
    OIL = "oil"
    PELLETS = "pellets"
    SOLAR = "solar"
    WOODCHIPS = "woodchips"
    ELECTRICITY = "electricity"
    GAS = "gas"
    COAL = "coal"
    DISTRICT_HEATING = "district_heating"


@enum.unique
class ElectricityFuel(str, enum.Enum):
    """Enum for electricity fuel types"""

    GERMAN_ENERGY_MIX = "german_energy_mix"
    SOLAR = "solar"


@enum.unique
class CarBusFuel(str, enum.Enum):
    """Enum for bus fuel types"""

    ELECTRIC = "electric"
    HYBRID = "hybrid"
    PLUGIN_HYBRID = "plug-in hybrid"
    CNG = "cng"
    GASOLINE = "gasoline"
    DIESEL = "diesel"
    AVERAGE = "average"
    HYDROGEN = "hydrogen"


@enum.unique
class Size(str, enum.Enum):
    """Enum for car sizes"""

    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    AVERAGE = "average"


@enum.unique
class TrainFuel(str, enum.Enum):
    """Enum for train fuel types"""

    ELECTRIC = "electric"
    DIESEL = "diesel"
    AVERAGE = "average"


@enum.unique
class FlightClass(str, enum.Enum):
    """Enum for flight classes"""

    ECONOMY = "economy_class"
    PREMIUM_ECONOMY = "premium_economy_class"
    BUSINESS = "business_class"
    FIRST = "first_class"
    AVERAGE = "average"


@enum.unique
class FerryClass(str, enum.Enum):
    """Enum for ferry classes"""

    FOOT = "foot_passenger"
    CAR = "car_passenger"
    AVERAGE = "average"


@enum.unique
class FlightRange(str, enum.Enum):
    """Enum for flight ranges"""

    DOMESTIC = "domestic"
    SHORT_HAUL = "short-haul"
    LONG_HAUL = "long-haul"


@enum.unique
class BusTrainRange(str, enum.Enum):
    """Enum for bus and train ranges"""

    LOCAL = "local"
    LONG_DISTANCE = "long-distance"


@enum.unique
class RangeCategory(str, enum.Enum):
    """Enum for range categories"""

    VERY_SHORT_HAUL = "very_short_haul"
    SHORT_HAUL = "short_haul"
    MEDIUM_HAUL = "medium_haul"
    LONG_HAUL = "long_haul"


@enum.unique
class TransportationMode(str, enum.Enum):
    CAR = "car"
    MOTORBIKE = "motorbike"
    BUS = "bus"
    TRAIN = "train"
    PLANE = "plane"
    FERRY = "ferry"
    TRAM = "tram"
    BICYCLE = "bicycle"
    PEDELEC = "pedelec"
