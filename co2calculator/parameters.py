#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""__description__"""

from pydantic import BaseModel, validator, root_validator
from .enums import *
from typing import Union


class TrainEmissionParameters(BaseModel):

    subcategory: TransportationMode = TransportationMode.Train
    fuel_type: Union[TrainFuelType, str] = TrainFuelType.Average
    range: Union[TrainRange, str] = TrainRange.Long_distance
    size: Union[TrainSize, str] = TrainSize.Average

    @validator("fuel_type", allow_reuse=True)
    def check_fueltype(cls, v):
        v = v.lower() if isinstance(v, str) else v
        return TrainFuelType(v)

    @validator("range", allow_reuse=True)
    def check_range(cls, v):
        v = v.lower() if isinstance(v, str) else v
        return TrainRange(v)

    @validator("size", allow_reuse=True)
    def check_size(cls, v):
        v = v.lower() if isinstance(v, str) else v
        return TrainSize(v)


class CarEmissionParameters(BaseModel):

    subcategory: TransportationMode = TransportationMode.Car
    fuel_type: Union[CarFuelType, str] = CarFuelType.Average
    size: Union[CarSize, str] = CarSize.Average

    @validator("fuel_type", allow_reuse=True)
    def check_fueltype(cls, v):
        v = v.lower() if isinstance(v, str) else v
        return CarFuelType(v)

    @validator("size", allow_reuse=True)
    def check_size(cls, v, values):
        v = v.lower() if isinstance(v, str) else v
        return CarSize(v)


class PlaneEmissionParameters(BaseModel):

    subcategory: TransportationMode = TransportationMode.Plane
    seating: Union[PlaneSeatingClass, str] = PlaneSeatingClass.Average
    range: Union[PlaneRange, str]

    @validator("range")
    def check_range(cls, v):
        v = v.lower() if isinstance(v, str) else v
        return PlaneRange(v)

    @validator("seating")
    def check_seating(cls, v):
        v = v.lower() if isinstance(v, str) else v
        return PlaneSeatingClass(v)


class BusEmissionParameters(BaseModel):

    subcategory: TransportationMode = TransportationMode.Bus
    fuel_type: Union[BusFuelType, str] = BusFuelType.Diesel
    size: Union[BusSize, str] = BusSize.Average
    occupancy: Union[BusOccupancy, str] = None
    range: Union[BusRange, str] = BusRange.Long_distance

    @validator("fuel_type", allow_reuse=True)
    def check_fueltype(cls, v):
        if isinstance(v, str):
            return BusFuelType(v.lower())
        else:
            return v

    @validator("size", allow_reuse=True)
    def check_size(cls, v):
        v = v.lower() if isinstance(v, str) else v
        return BusSize(v)

    @validator("range", allow_reuse=True)
    def check_range(cls, v):
        v = v.lower() if isinstance(v, str) else v
        return BusRange(v)

    @validator("occupancy", allow_reuse=True)
    def check_occupancy(cls, v):
        v = v.lower() if isinstance(v, str) else v
        return BusOccupancy(v)

    @root_validator(pre=False)
    def check_occupancy(cls, values):
        if values['occupancy'] is None:
            if values['fuel_type'] in [BusFuelType.Cng, BusFuelType.Hydrogen]:
                values['occupancy'] = None
            else:
                values['occupancy'] = BusOccupancy.c_50
        else:
            values['occupancy'] = BusOccupancy(values['occupancy'])
        return values


class MotorbikeEmissionParameters(BaseModel):

    subcategory: TransportationMode = TransportationMode.Motorbike
    size: Union[MotorbikeSize, str] = MotorbikeSize.Average

    @validator("size", allow_reuse=True)
    def check_size(cls, v):
        v = v.lower() if isinstance(v, str) else v
        return MotorbikeSize(v)



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

