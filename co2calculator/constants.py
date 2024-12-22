#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Constant variables and enums"""

import enum

import iso3166
from co2calculator.data_handlers import Airports


class HeatingFuel(enum.Enum):
    """Enum for heating fuel types"""

    OIL = "oil"
    COAL = "coal"
    GAS = "gas"
    WOOD_PELLETS = "wood pellets"
    WOOD_CHIPS = "wood chips"
    LPG = "liquid gas"


@enum.unique
class ElectricityFuel(str, enum.Enum):
    """Enum for electricity fuel types"""

    PRODUCTION_FUEL_MIX = "production fuel mix"
    RESIDUAL_FUEL_MIX = "residual fuel mix"


@enum.unique
class CarFuel(str, enum.Enum):
    """Enum for car fuel types"""

    ELECTRIC = "electric"
    HYBRID = "hybrid"
    PLUGIN_HYBRID = "plug-in_hybrid"
    CNG = "cng"
    GASOLINE = "gasoline"
    DIESEL = "diesel"
    AVERAGE = "average"


@enum.unique
class BusFuel(str, enum.Enum):
    """Enum for bus fuel types"""

    ELECTRIC = "electric"
    DIESEL = "diesel"
    AVERAGE = "average"
    HYDROGEN = "hydrogen"
    CNG = "cng"


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

    SHORT_HAUL = "short-haul"
    LONG_HAUL = "long-haul"
    AVERAGE = "average"


@enum.unique
class BusTrainRange(str, enum.Enum):
    """Enum for bus and train ranges"""

    LOCAL = "local"
    LONG_DISTANCE = "long-distance"
    AVERAGE = "average"


@enum.unique
class RangeCategory(str, enum.Enum):
    """Enum for range categories"""

    VERY_SHORT_HAUL = "very_short_haul"
    SHORT_HAUL = "short_haul"
    MEDIUM_HAUL = "medium_haul"
    LONG_HAUL = "long_haul"


class DetourCoefficient(float, enum.Enum):
    BUS = 1.5
    TRAIN = 1.2
    PLANE = 1.0


class DetourConstant(float, enum.Enum):
    BUS = 0.0
    TRAIN = 0.0
    PLANE = 95


@enum.unique
class TransportationMode(str, enum.Enum):
    """Enum for transportation modes"""

    CAR = "car"
    MOTORBIKE = "motorbike"
    BUS = "bus"
    TRAIN = "train"
    PLANE = "plane"
    FERRY = "ferry"
    TRAM = "tram"
    BICYCLE = "bicycle"
    PEDELEC = "pedelec"


@enum.unique
class Unit(str, enum.Enum):
    KWH = "kwh"
    KG = "kg"
    L = "l"
    M3 = "m^3"


@enum.unique
class EmissionCategory(str, enum.Enum):
    HEATING = "heating"
    ELECTRICITY = "electricity"
    TRANSPORT = "transport"


@enum.unique
class RoutingProfile(str, enum.Enum):
    CAR = "driving-car"
    CYCLING = "cycling-regular"
    WALK = "foot-walking"


class CountryCode2(str):
    """Class for 2-letter country codes (ISO 3166-1 alpha-2)"""

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_country_code

    @classmethod
    def validate_country_code(cls, country_code: str) -> str:
        if country_code in list(iso3166.countries_by_alpha2.keys()):
            return country_code
        else:
            raise ValueError(f"{country_code} is not a valid country code")


class CountryCode3(str):
    """Class for 3-letter country codes (ISO 3166-1 alpha-3)"""

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_country_code

    @classmethod
    def validate_country_code(cls, country_code: str) -> str:
        if country_code in list(iso3166.countries_by_alpha3.keys()):
            return country_code
        else:
            raise ValueError(f"{country_code} is not a valid country code")


class CountryName(str):
    """Class for country names (ISO 3166)"""

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_country_name

    @classmethod
    def validate_country_name(cls, country_name: str) -> str:
        if country_name.upper() in list(iso3166.countries_by_name.keys()):
            return country_name
        else:
            raise ValueError(f"{country_name} is not a valid country name")


class IataAirportCode(str):
    """Class for 3-letter IATA airport codes"""

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_iata_code

    @classmethod
    def validate_iata_code(cls, iata_code: str) -> str:
        if iata_code in Airports().airports["iata_code"].values:
            return iata_code
        else:
            raise ValueError(f"{iata_code} was not found in airport database")
