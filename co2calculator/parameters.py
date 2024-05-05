#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Base classes to handle and validate parameters for emission calculations"""

from typing import Union

from pydantic import BaseModel, validator, root_validator, ValidationError

# from .api.trip import Trip ##--> causes circular import
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


class TrainEmissionParameters(BaseModel):

    category: EmissionCategory = EmissionCategory.TRANSPORT
    subcategory: TransportationMode = TransportationMode.TRAIN
    vehicle_range: Union[BusTrainRange, str] = BusTrainRange.LONG_DISTANCE
    country_code: str = "global"

    @validator("vehicle_range", allow_reuse=True)
    def check_range(cls, v):
        if isinstance(v, str):
            assert v.lower() in (item.value for item in BusTrainRange)
            v = v.lower()
        return BusTrainRange(v)

    @root_validator(pre=True)
    def validate_input_parameters(cls, values):
        allowed_keys = {"vehicle_range", "country_code"}
        invalid_keys = set(values.keys()) - allowed_keys

        if invalid_keys:
            raise ValueError(
                f"Invalid parameter(s): {', '.join(invalid_keys)}. "
                "Only 'vehicle_range' and 'country_code' are allowed as input parameters for train."
            )

        return values

    @root_validator
    def validate_country_code_and_range(cls, values):
        country_code = values.get("country_code")
        vehicle_range = values.get("vehicle_range")

        # check if size is specified, fuel_type must also be specified
        if country_code != "global" and vehicle_range != BusTrainRange.AVERAGE:
            raise ValueError(
                "If 'country_code' is specified, 'vehicle_range' must be 'average'."
            )

        return values


class TramEmissionParameters(BaseModel):

    category: EmissionCategory = EmissionCategory.TRANSPORT
    subcategory: TransportationMode = TransportationMode.TRAM

    @root_validator(pre=True)
    def validate_input_parameters(cls, values):
        allowed_keys = {None}
        invalid_keys = set(values.keys()) - allowed_keys

        if invalid_keys:
            raise ValueError(
                f"Invalid parameter(s): {', '.join(invalid_keys)}. "
                "No input parameters are allowed for tram."
            )

        return values


class BicycleEmissionParameters(BaseModel):

    category: EmissionCategory = EmissionCategory.TRANSPORT
    subcategory: TransportationMode = TransportationMode.BICYCLE

    @root_validator(pre=True)
    def validate_input_parameters(cls, values):
        allowed_keys = {None}
        invalid_keys = set(values.keys()) - allowed_keys

        if invalid_keys:
            raise ValueError(
                f"Invalid parameter(s): {', '.join(invalid_keys)}. "
                "No input parameters are allowed for bicycle."
            )

        return values


class PedelecEmissionParameters(BaseModel):

    category: EmissionCategory = EmissionCategory.TRANSPORT
    subcategory: TransportationMode = TransportationMode.PEDELEC

    @root_validator(pre=True)
    def validate_input_parameters(cls, values):
        allowed_keys = {None}
        invalid_keys = set(values.keys()) - allowed_keys

        if invalid_keys:
            raise ValueError(
                f"Invalid parameter(s): {', '.join(invalid_keys)}. "
                "No input parameters are allowed for pedelec."
            )

        return values


class CarEmissionParameters(BaseModel):

    category: EmissionCategory = EmissionCategory.TRANSPORT
    subcategory: TransportationMode = TransportationMode.CAR
    fuel_type: Union[CarFuel, str] = CarFuel.AVERAGE
    size: Union[Size, str] = Size.AVERAGE
    passengers: int = 1

    @root_validator(pre=True)
    def validate_input_parameters(cls, values):
        allowed_keys = {"fuel_type", "size", "passengers"}
        invalid_keys = set(values.keys()) - allowed_keys

        if invalid_keys:
            raise ValueError(
                f"Invalid parameter(s): {', '.join(invalid_keys)}. "
                "Only 'fuel_type', 'size' and 'passengers' are allowed as input parameters for car."
            )

        return values

    @root_validator
    def validate_size_and_fuel_type(cls, values):
        size = values.get("size")
        fuel_type = values.get("fuel_type")

        # check if size is specified, fuel_type must also be specified
        if size != Size.AVERAGE and fuel_type == CarFuel.AVERAGE:
            raise ValueError(
                "If 'size' is specified, 'fuel_type' must also be specified."
            )

        return values

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
    vehicle_range: Union[FlightRange, str] = None
    # vehicle_range needs to be added here but therefore the user
    # can also give vehicle_range as input.

    @root_validator(pre=True)
    def validate_input_parameters(cls, values):
        allowed_keys = {"seating", "vehicle_range"}  #
        invalid_keys = set(values.keys()) - allowed_keys

        if invalid_keys:
            raise ValueError(
                f"Invalid parameter(s): {', '.join(invalid_keys)}. "
                "Only 'seating' is allowed as input parameter for plane. Range is defined through distance."
            )

        return values

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
    ferry_class: Union[FerryClass, str] = FerryClass.AVERAGE

    @root_validator(pre=True)
    def validate_input_parameters(cls, values):
        allowed_keys = {"ferry_class"}
        invalid_keys = set(values.keys()) - allowed_keys

        if invalid_keys:
            raise ValueError(
                f"Invalid parameter(s): {', '.join(invalid_keys)}. "
                "Only 'ferry_class' is allowed as input parameter for ferry."
            )

        return values

    @validator("ferry_class")
    def check_ferry_class(cls, v):
        if isinstance(v, str):
            assert v.lower() in (item.value for item in FerryClass)
            v = v.lower()
        return FerryClass(v)


class BusEmissionParameters(BaseModel):

    category: EmissionCategory = EmissionCategory.TRANSPORT
    subcategory: TransportationMode = TransportationMode.BUS
    fuel_type: Union[BusFuel, str] = BusFuel.DIESEL
    size: Union[Size, str] = Size.SMALL
    vehicle_range: Union[BusTrainRange, str] = BusTrainRange.LONG_DISTANCE

    @root_validator(pre=True)
    def validate_input_parameters(cls, values):
        allowed_keys = {"fuel_type", "size", "vehicle_range"}
        invalid_keys = set(values.keys()) - allowed_keys

        if invalid_keys:
            raise ValueError(
                f"Invalid parameter(s): {', '.join(invalid_keys)}. "
                "Only 'fuel_type', 'size' and 'vehicle_range' are allowed as input parameters for bus."
            )

        return values

    @root_validator
    def validate_fuel_type_electric_with_size_and_range(cls, values):
        size = values.get("size")
        fuel_type = values.get("fuel_type")
        vehicle_range = values.get("vehicle_range")

        # check if fuel_type is electric, size must be average and range must be local
        if fuel_type == BusFuel.ELECTRIC and (
            size != Size.AVERAGE or vehicle_range != BusTrainRange.LOCAL
        ):
            raise ValueError(
                "If 'fuel_type' is 'electric', 'size' must be 'average' and 'vehicle_range' must be 'local'."
            )

        return values

    @root_validator
    def validate_fuel_type_cng_with_range(cls, values):
        fuel_type = values.get("fuel_type")
        vehicle_range = values.get("vehicle_range")

        # check if fuel_type is cng range must be local
        if fuel_type == BusFuel.CNG and vehicle_range != BusTrainRange.LOCAL:
            raise ValueError(
                "If 'fuel_type' is 'cng', 'vehicle_range' must be 'local'."
            )

        return values

    @root_validator
    def validate_fuel_type_diesel_with_range_and_size(cls, values):
        size = values.get("size")
        fuel_type = values.get("fuel_type")
        vehicle_range = values.get("vehicle_range")

        # check if fuel_type is diesel and vehicle_range is long-distance, size must be small or large
        if (
            fuel_type == BusFuel.DIESEL
            and vehicle_range == BusTrainRange.LONG_DISTANCE
            and size not in {Size.SMALL, Size.LARGE}
        ):
            raise ValueError(
                "If 'fuel_type' is 'diesel' and 'vehicle_range' is 'long-distance', size must be 'small' or 'large'."
            )

        return values

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

    @validator("vehicle_range", allow_reuse=True)
    def check_range(cls, v):
        if isinstance(v, str):
            assert v.lower() in (item.value for item in BusTrainRange)
            v = v.lower()
        return BusTrainRange(v)


class MotorbikeEmissionParameters(BaseModel):

    category: EmissionCategory = EmissionCategory.TRANSPORT
    subcategory: TransportationMode = TransportationMode.MOTORBIKE
    size: Union[Size, str] = Size.AVERAGE

    @root_validator(pre=True)
    def validate_input_parameters(cls, values):
        allowed_keys = {"size"}
        invalid_keys = set(values.keys()) - allowed_keys

        if invalid_keys:
            raise ValueError(
                f"Invalid parameter(s): {', '.join(invalid_keys)}. "
                "Only 'size' is allowed as input parameter for motorbike."
            )

        return values

    @validator("size", allow_reuse=True)
    def check_size(cls, v):
        if isinstance(v, str):
            assert v.lower() in (item.value for item in Size)
            v = v.lower()
        return Size(v)


class ElectricityEmissionParameters(BaseModel):

    category: EmissionCategory = EmissionCategory.ELECTRICITY
    fuel_type: Union[ElectricityFuel, str] = ElectricityFuel.PRODUCTION_FUEL_MIX
    country_code: CountryCode2  # TODO: Shall we set a default? Or add a watning if not provided?

    @validator("fuel_type", allow_reuse=True)
    def check_fueltype(cls, v):
        if isinstance(v, str):
            assert v.lower() in (item.value for item in ElectricityFuel)
            v = v.lower()
        return ElectricityFuel(v)


class ElectricityParameters(BaseModel):
    electricity_emission_parameters: ElectricityEmissionParameters
    energy_share: float

    @validator("energy_share", allow_reuse=True)
    def check_energy_share(cls, v):
        assert 0 <= v <= 1
        return v


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


class HeatingParameters(BaseModel):
    heating_emission_parameters: HeatingEmissionParameters
    unit: Unit
    area_share: float

    @validator("unit", allow_reuse=True)
    def check_unit(cls, v):
        if isinstance(v, str):
            assert v.lower() in (item.value for item in Unit)
            v = v.lower()
        return Unit(v)

    @validator("area_share", allow_reuse=True)
    def check_area_share(cls, v):
        assert 0 <= v <= 1
        return v
