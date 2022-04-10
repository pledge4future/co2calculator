#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Constant variables and enums"""

import enum

KWH_TO_TJ = 277777.77777778


class HeatingFuel(enum.Enum):
    """Enum for heating fuel types"""

    HEAT_PUMP_AIR = "Heat pump air"
    HEAT_PUMP_GROUND = "Heat pump ground"
    HEAT_PUMP_WATER = "Heat pump water"
    LIQUID_GAS = "Liquid gas"
    OIL = "Oil"
    PELLETS = "Pellets"
    SOLAR = "Solar"
    WOODCHIPS = "Woodchips"
    ELECTRICITY = "Electricity"
    GAS = "Gas"
    COAL = "Coal"
    DISTRICT_HEATING = "District heating"


class ElectricityFuel(enum.Enum):
    """Enum for electricity fuel types"""

    GERMAN_ENERGY_MIX = "German energy mix"
    SOLAR = "Solar"


class CarBusFuel(enum.Enum):
    """Enum for bus fuel types"""

    ELECTRIC = "Electric"
    HYBRID = "Hybrid"
    PLUGIN_HYBRID = "Plug-in hybrid"
    CNG = "CNG"
    GASOLINE = "Gasoline"
    DIESEL = "Diesel"
    AVERAGE = "Average"
    HYDROGEN = "Hydrogen"


class Size(enum.Enum):
    """Enum for car sizes"""

    SMALL = "Small"
    MEDIUM = "Medium"
    LARGE = "Large"
    AVERAGE = "Average"


class TrainFuel(enum.Enum):
    """Enum for train fuel types"""

    ELECTRIC = "Electric"
    DIESEL = "Diesel"
    AVERAGE = "Average"


class FlightClass(enum.Enum):
    """Enum for flight classes"""

    ECONOMY = "Economy class"
    PREMIUM_ECONOMY = "Premium economy class"
    BUSINESS = "Business class"
    FIRST = "First class"
    AVERAGE = "Average"


class FerryClass(enum.Enum):
    """Enum for ferry classes"""

    FOOT = "Foot passenger"
    CAR = "Car passenger"
    AVERAGE = "Average"


class FlightRange(enum.Enum):
    """Enum for flight ranges"""

    DOMESTIC = "Domestic"
    SHORT_HAUL = "Short-haul"
    LONG_HAUL = "Long-haul"


class BusTrainRange(enum.Enum):
    """Enum for bus and train ranges"""

    LOCAL = "Local"
    LONG_DISTANCE = "Long-distance"


class RangeCategory(enum.Enum):
    """Enum for range categories"""

    VERY_SHORT_HAUL = "very_short_haul"
    SHORT_HAUL = "short_haul"
    MEDIUM_HAUL = "medium_haul"
    LONG_HAUL = "long_haul"
