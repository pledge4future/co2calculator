#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""__description__"""

from pydantic import BaseModel, validator, root_validator
from constants import (
    TransportationMode,
    Size,
    CarFuel,
    BusFuel,
    TrainFuel,
    BusTrainRange,
    FlightRange,
    FlightClass,
)
from typing import Union


class TrainEmissionParameters(BaseModel):

    subcategory: TransportationMode = TransportationMode.TRAIN
    fuel_type: Union[TrainFuel, str] = TrainFuel.AVERAGE
    range: Union[BusTrainRange, str] = BusTrainRange.LONG_DISTANCE
    size: Union[Size, str] = Size.AVERAGE

    @validator("fuel_type", allow_reuse=True)
    def check_fueltype(cls, v):
        v = v.lower() if isinstance(v, str) else v
        return TrainFuel(v)

    @validator("range", allow_reuse=True)
    def check_range(cls, v):
        v = v.lower() if isinstance(v, str) else v
        return BusTrainRange(v)

    @validator("size", allow_reuse=True)
    def check_size(cls, v):
        v = v.lower() if isinstance(v, str) else v
        return Size(v)


class TramEmissionParameters(BaseModel):

    subcategory: TransportationMode = TransportationMode.TRAM
    size: Union[Size, str] = Size.AVERAGE

    @validator("size", allow_reuse=True)
    def check_size(cls, v):
        v = v.lower() if isinstance(v, str) else v
        return Size(v)


class CarEmissionParameters(BaseModel):

    subcategory: TransportationMode = TransportationMode.CAR
    fuel_type: Union[CarFuel, str] = CarFuel.AVERAGE
    size: Union[Size, str] = Size.AVERAGE

    @validator("fuel_type", allow_reuse=True)
    def check_fueltype(cls, v):
        v = v.lower() if isinstance(v, str) else v
        return CarFuel(v)

    @validator("size", allow_reuse=True)
    def check_size(cls, v, values):
        v = v.lower() if isinstance(v, str) else v
        return Size(v)


class PlaneEmissionParameters(BaseModel):

    subcategory: TransportationMode = TransportationMode.PLANE
    seating: Union[FlightClass, str] = FlightClass.AVERAGE
    range: Union[FlightRange, str]

    @validator("range")
    def check_range(cls, v):
        v = v.lower() if isinstance(v, str) else v
        return FlightRange(v)

    @validator("seating")
    def check_seating(cls, v):
        v = v.lower() if isinstance(v, str) else v
        return FlightClass(v)


class BusEmissionParameters(BaseModel):

    subcategory: TransportationMode = TransportationMode.BUS
    fuel_type: Union[BusFuel, str] = BusFuel.DIESEL
    size: Union[Size, str] = Size.AVERAGE
    occupancy: int = 50
    range: Union[BusTrainRange, str] = BusTrainRange.LONG_DISTANCE

    @validator("fuel_type", allow_reuse=True)
    def check_fueltype(cls, v):
        if isinstance(v, str):
            return BusFuel(v.lower())
        else:
            return v

    @validator("size", allow_reuse=True)
    def check_size(cls, v):
        v = v.lower() if isinstance(v, str) else v
        return Size(v)

    @validator("range", allow_reuse=True)
    def check_range(cls, v):
        v = v.lower() if isinstance(v, str) else v
        return BusTrainRange(v)


class MotorbikeEmissionParameters(BaseModel):

    subcategory: TransportationMode = TransportationMode.MOTORBIKE
    size: Union[Size, str] = Size.AVERAGE

    @validator("size", allow_reuse=True)
    def check_size(cls, v):
        v = v.lower() if isinstance(v, str) else v
        return Size(v)


# class EmissionParameters(BaseModel):
#
#     subcategory: Union[TransportationMode, str]
#     fuel_type: Union[CarFuelType, BusFuelType, PlaneFuelType, TrainFuelType, str] = None
#     size: Union[CarSize, BusSize, TrainSize, str] = None
#     occupancy: Union[BusOccupancy, TrainOccupancy, str] = None
#     range: Union[BusRange, TrainRange, str] = None
#     seating_class: Union[PlaneSeatingClass, FerrySeatingClass, str] = None
#
#     @validator("fuel_type", allow_reuse=True)
#     def check_fueltype(cls, v, values):
#         v = v.lower() if isinstance(v, str) else v
#         if v is "average":
#             if "Average" not in TrainFuelType.__members__.keys():
#                 return eval(f"{t}FuelType('nan')")
#             else:
#                 raise FactorNotFound("Fuel type needs to be provided. No average value found.")
#         else:
#             return eval(f"{t}FuelType('{v}')")
#
#     @validator("size", allow_reuse=True, pre=True)
#     def check_size(cls, v, values):
#         t = values["subcategory"].lower().capitalize()
#         v = v.lower() if isinstance(v, str) else v
#         return eval(f"{t}Size('{v}')")
#
#     @validator("range", allow_reuse=True)
#     def check_range(cls, v, values):
#         t = values["subcategory"].lower().capitalize()
#         v = v.lower() if isinstance(v, str) else v
#         return eval(f"{t}Range('{v}')")
#
#     @validator("seating_class", allow_reuse=True)
#     def check_seating_class(cls, v, values):
#         t = values["subcategory"].lower().capitalize()
#         v = v.lower() if isinstance(v, str) else v
#         return eval(f"{t}SeatingClass('{v}')")
#
#     @validator("occupancy", allow_reuse=True)
#     def check_occupancy(cls, v, values):
#         t = values["subcategory"].lower().capitalize()
#         v = v.lower() if isinstance(v, str) else v
#         return eval(f"{t}Occupancy('{v}')")
#
#
