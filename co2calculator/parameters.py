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
)
from typing import Union


class TrainEmissionParameters(BaseModel):

    category: TransportationMode = EmissionCategory.TRANSPORT
    subcategory: TransportationMode = TransportationMode.TRAIN
    range: Union[BusTrainRange, str] = BusTrainRange.LONG_DISTANCE
    size: Union[Size, str] = Size.AVERAGE

    @validator("range", allow_reuse=True)
    def check_range(cls, v):
        if isinstance(v, str):
            assert v.lower() in (item.value for item in BusTrainRange)
            v = v.lower()
        return BusTrainRange(v)

    @validator("size", allow_reuse=True)
    def check_size(cls, v):
        if isinstance(v, str):
            assert v.lower() in (item.value for item in Size)
            v = v.lower()
        return Size(v)


class TramEmissionParameters(BaseModel):

    category: TransportationMode = EmissionCategory.TRANSPORT
    subcategory: TransportationMode = TransportationMode.TRAM
    size: Union[Size, str] = Size.AVERAGE

    @validator("size", allow_reuse=True)
    def check_size(cls, v):
        if isinstance(v, str):
            assert v.lower() in (item.value for item in Size)
            v = v.lower()
        return Size(v)


class CarEmissionParameters(BaseModel):

    category: TransportationMode = EmissionCategory.TRANSPORT
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

    category: TransportationMode = EmissionCategory.TRANSPORT
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

    category: TransportationMode = EmissionCategory.TRANSPORT
    subcategory: TransportationMode = TransportationMode.FERRY
    seating: Union[FerryClass, str] = FerryClass.AVERAGE

    @validator("seating")
    def check_seating(cls, v):
        if isinstance(v, str):
            assert v.lower() in (item.value for item in FerryClass)
            v = v.lower()
        return FerryClass(v)


class BusEmissionParameters(BaseModel):

    category: TransportationMode = EmissionCategory.TRANSPORT
    subcategory: TransportationMode = TransportationMode.BUS
    fuel_type: Union[BusFuel, str] = BusFuel.DIESEL
    size: Union[Size, str] = Size.AVERAGE
    occupancy: int = 50
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

    category: TransportationMode = EmissionCategory.TRANSPORT
    subcategory: TransportationMode = TransportationMode.MOTORBIKE
    size: Union[Size, str] = Size.AVERAGE

    @validator("size", allow_reuse=True)
    def check_size(cls, v):
        if isinstance(v, str):
            assert v.lower() in (item.value for item in Size)
            v = v.lower()
        return Size(v)


class ElectricityEmissionParameters(BaseModel):

    category: TransportationMode = EmissionCategory.ELECTRICITY
    fuel_type: Union[Size, str] = ElectricityFuel.PRODUCTION_FUEL_MIX

    @validator("fuel_type", allow_reuse=True)
    def check_fueltype(cls, v):
        if isinstance(v, str):
            assert v.lower() in (item.value for item in ElectricityFuel)
            v = v.lower()
        return ElectricityFuel(v)


class HeatingEmissionParameters(BaseModel):

    category: TransportationMode = EmissionCategory.HEATING
    fuel_type: Union[Size, str] = HeatingFuel.GAS

    @validator("fuel_type", allow_reuse=True)
    def check_fueltype(cls, v):
        if isinstance(v, str):
            assert v.lower() in (item.value for item in HeatingFuel)
            v = v.lower()
        return HeatingFuel(v)
