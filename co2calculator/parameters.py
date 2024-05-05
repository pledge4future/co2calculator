#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Base classes to handle and validate parameters for emission calculations"""

from pydantic import BaseModel, validator
from .constants import (
    TransportationMode,
    Size,
    CarFuel,
    BusFuel,
    BusTrainRange,
    FlightRange,
    FlightClass,
    FerryClass,
    ElectricityFuel,
    HeatingFuel,
    EmissionCategory,
    CountryCode2,
)
from typing import Union


class TrainEmissionParameters(BaseModel):

    category: EmissionCategory = EmissionCategory.TRANSPORT
    subcategory: TransportationMode = TransportationMode.TRAIN
    range: Union[BusTrainRange, str] = BusTrainRange.LONG_DISTANCE
    country_code: str = "global"

    @validator("range", allow_reuse=True)
    def check_range(cls, v):
        if isinstance(v, str):
            assert v.lower() in (item.value for item in BusTrainRange)
            v = v.lower()
        return BusTrainRange(v)


class TramEmissionParameters(BaseModel):

    category: EmissionCategory = EmissionCategory.TRANSPORT
    subcategory: TransportationMode = TransportationMode.TRAM
    size: Union[Size, str] = Size.AVERAGE

    @validator("size", allow_reuse=True)
    def check_size(cls, v):
        if isinstance(v, str):
            assert v.lower() in (item.value for item in Size)
            v = v.lower()
        return Size(v)


class CarEmissionParameters(BaseModel):

    category: EmissionCategory = EmissionCategory.TRANSPORT
    subcategory: TransportationMode = TransportationMode.CAR
    fuel_type: Union[CarFuel, str] = CarFuel.AVERAGE
    size: Union[Size, str] = Size.AVERAGE
    passengers: int = 1

    @validator("fuel_type", allow_reuse=True)
    def check_fueltype(cls, v):
        if isinstance(v, str):
            assert v.lower() in (item.value for item in CarFuel)
            v = v.lower()
        return CarFuel(v)

    @validator("size", allow_reuse=True)
    def check_size(cls, v, values):
        if isinstance(v, str):
            assert v.lower() in (item.value for item in Size)
            v = v.lower()
        return Size(v)


class PlaneEmissionParameters(BaseModel):

    category: EmissionCategory = EmissionCategory.TRANSPORT
    subcategory: TransportationMode = TransportationMode.PLANE
    seating: Union[FlightClass, str] = FlightClass.AVERAGE
    range: Union[FlightRange, str]

    @validator("range")
    def check_range(cls, v):
        if isinstance(v, str):
            assert v.lower() in (item.value for item in FlightRange)
            v = v.lower()
        return FlightRange(v)

    @validator("seating")
    def check_seating(cls, v):
        if isinstance(v, str):
            # Check if v is a valid value of enum FlightClass
            assert v.lower() in (item.value for item in FlightClass)
            v = v.lower()
        return FlightClass(v)


class FerryEmissionParameters(BaseModel):

    category: EmissionCategory = EmissionCategory.TRANSPORT
    subcategory: TransportationMode = TransportationMode.FERRY
    seating: Union[FerryClass, str] = FerryClass.AVERAGE

    @validator("seating")
    def check_seating(cls, v):
        if isinstance(v, str):
            assert v.lower() in (item.value for item in FerryClass)
            v = v.lower()
        return FerryClass(v)


class BusEmissionParameters(BaseModel):

    category: EmissionCategory = EmissionCategory.TRANSPORT
    subcategory: TransportationMode = TransportationMode.BUS
    fuel_type: Union[BusFuel, str] = BusFuel.DIESEL
    size: Union[Size, str] = Size.SMALL
    range: Union[BusTrainRange, str] = BusTrainRange.LONG_DISTANCE

    @validator("fuel_type", allow_reuse=True)
    def check_fueltype(cls, v):
        if isinstance(v, str):
            assert v.lower() in (item.value for item in BusFuel)
            v = v.lower()
        return BusFuel(v)

    @validator("size", allow_reuse=True)
    def check_size(cls, v):
        if isinstance(v, str):
            assert v.lower() in (item.value for item in Size)
            v = v.lower()
        return Size(v)

    @validator("range", allow_reuse=True)
    def check_range(cls, v):
        if isinstance(v, str):
            assert v.lower() in (item.value for item in BusTrainRange)
            v = v.lower()
        return BusTrainRange(v)


class MotorbikeEmissionParameters(BaseModel):

    category: EmissionCategory = EmissionCategory.TRANSPORT
    subcategory: TransportationMode = TransportationMode.MOTORBIKE
    size: Union[Size, str] = Size.AVERAGE

    @validator("size", allow_reuse=True)
    def check_size(cls, v):
        if isinstance(v, str):
            assert v.lower() in (item.value for item in Size)
            v = v.lower()
        return Size(v)


class ElectricityEmissionParameters(BaseModel):

    category: EmissionCategory = EmissionCategory.ELECTRICITY
    fuel_type: Union[ElectricityFuel, str] = ElectricityFuel.PRODUCTION_FUEL_MIX
    country_code: CountryCode2

    @validator("fuel_type", allow_reuse=True)
    def check_fueltype(cls, v):
        if isinstance(v, str):
            assert v.lower() in (item.value for item in ElectricityFuel)
            v = v.lower()
        return ElectricityFuel(v)


class HeatingEmissionParameters(BaseModel):

    category: EmissionCategory = EmissionCategory.HEATING
    fuel_type: Union[HeatingFuel, str] = HeatingFuel.GAS
    country_code: str = "global"

    @validator("fuel_type", allow_reuse=True)
    def check_fueltype(cls, v):
        if isinstance(v, str):
            assert v.lower() in (item.value for item in HeatingFuel)
            v = v.lower()
        return HeatingFuel(v)
