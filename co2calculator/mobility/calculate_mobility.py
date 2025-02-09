"""Function collection to calculate mobility type co2 emissions"""

from typing import Union, Tuple
from pydantic import ValidationError

from co2calculator.constants import EmissionCategory, FlightRange, TransportationMode
from .._types import Kilogram, Kilometer
from ..parameters import (
    BusEmissionParameters,
    CarEmissionParameters,
    FerryEmissionParameters,
    MotorbikeEmissionParameters,
    PlaneEmissionParameters,
    TrainEmissionParameters,
    TramEmissionParameters,
    PedelecEmissionParameters,
    BicycleEmissionParameters,
)
from ..data_handlers import ConversionFactors, EmissionFactors

emission_factors = EmissionFactors()
conversion_factors = ConversionFactors()


def calc_co2_car(
    distance: Kilometer, options: Union[CarEmissionParameters, dict] = None
) -> Tuple[Kilogram, float, CarEmissionParameters]:
    """Function to compute the emissions of a car trip.

    :param distance: Distance travelled by car (km), alternatively param <locations> can be provided
    :param options: Options for the car trip
    :type distance: Kilometer
    :type options: Union[CarEmissionParameters, dict]
    :return: Total emissions of trip in co2 equivalents, Co2e factor and the parameters
    :rtype: Tuple[Kilogram, float, CarEmissionParameters]
    """
    if options is None:
        options = {}
    # Validate parameters
    params = CarEmissionParameters.parse_obj(options)
    # Get the co2 factor
    co2e_factor = emission_factors.get(params.dict())
    # Calculate emissions
    co2e = distance * co2e_factor / params.passengers
    return co2e, co2e_factor, params


def calc_co2_motorbike(
    distance: Kilometer, options: Union[MotorbikeEmissionParameters, dict] = None
) -> Tuple[Kilogram, float, MotorbikeEmissionParameters]:
    """Function to compute the emissions of a motorbike trip.

    :param distance: Distance travelled by motorbike (km), alternatively param <locations> can be provided
    :param options: Options for the motorbike trip
    :type distance: Kilometer
    :type options: Union[MotorbikeEmissionParameters, dict]
    :return: Total emissions of trip in co2 equivalents, Co2e factor and the parameters
    :rtype: Tuple[Kilogram, float, MotorbikeEmissionParameters]
    """
    # Validate parameters
    if options is None:
        options = {}
    params = MotorbikeEmissionParameters.parse_obj(options)
    # Get the co2 factor
    co2e_factor = emission_factors.get(params.dict())
    # Calculate emissions
    co2e = distance * co2e_factor
    return co2e, co2e_factor, params


def calc_co2_bus(
    distance: Kilometer, options: Union[BusEmissionParameters, dict] = None
) -> Tuple[Kilogram, float, BusEmissionParameters]:
    """Function to compute the emissions of a bus trip.

    :param distance: Distance travelled by bus (km), alternatively param <locations> can be provided
    :param options: Options for the bus trip
    :type distance: Kilometer
    :type options: Union[BusEmissionParameters, dict]
    :return: Total emissions of trip in co2 equivalents, Co2e factor and the parameters
    :rtype: Tuple[Kilogram, float, BusEmissionParameters]
    """
    # Validate parameters
    if options is None:
        options = {}
    params = BusEmissionParameters.parse_obj(options)
    # Get the co2 factor
    co2e_factor = emission_factors.get(params.dict())
    # Calculate emissions
    co2e = distance * co2e_factor
    return co2e, co2e_factor, params


def calc_co2_train(
    distance: Kilometer, options: Union[TrainEmissionParameters, dict] = None
) -> Tuple[Kilogram, float, TrainEmissionParameters]:
    """Function to compute the emissions of a train trip.

    :param distance: Distance travelled by train (km), alternatively param <locations> can be provided
    :param options: Options for the train trip
    :type distance: Kilometer
    :type options: Union[TrainEmissionParameters, dict]
    :return: Total emissions of trip in co2 equivalents, Co2e factor and the parameters
    :rtype: Tuple[Kilogram, float, TrainEmissionParameters]
    """

    if options is None:
        options = {}
    params = TrainEmissionParameters.parse_obj(options)
    # Get the co2 factor
    co2e_factor = emission_factors.get(params.dict())
    # Calculate emissions
    co2e = distance * co2e_factor
    return co2e, co2e_factor, params


def calc_co2_plane(
    distance: Kilometer, options: PlaneEmissionParameters = None
) -> Tuple[Kilogram, float, PlaneEmissionParameters]:
    """Function to compute emissions of a plane trip

    :param distance: Distance of flight (km), alternatively param <locations> can be provided
    :param options: Options for the plane trip
    :type distance: Kilometer
    :type options: PlaneEmissionParameters
    :return: Total emissions of flight in co2 equivalents, Co2e factor and the parameters
    :rtype: Tuple[Kilogram, float, PlaneEmissionParameters]
    """

    if options is None:
        options = {}
    # Retrieve whether distance is <= 3700 or above 3700 km
    if distance is None:
        raise ValueError("Distance is not given. Range can not be calculated.")
    if distance <= 3700:
        options["vehicle_range"] = FlightRange.SHORT_HAUL
    else:
        options["vehicle_range"] = FlightRange.LONG_HAUL

    params = PlaneEmissionParameters.parse_obj(options)
    # Get the co2 factor
    co2e_factor = emission_factors.get(params.dict())
    # Calculate emissions
    co2e = distance * co2e_factor
    return co2e, co2e_factor, params


def calc_co2_ferry(
    distance: Kilometer, options: Union[FerryEmissionParameters, dict] = None
) -> Tuple[Kilogram, float, FerryEmissionParameters]:
    """Function to compute emissions of a ferry trip

    :param distance: Distance of ferry trip (km), alternatively param <locations> can be provided
    :param options: Options for the ferry trip
    :type distance: Kilometer
    :type options: Union[FerryEmissionParameters, dict]
    :return: Total emissions of ferry trip in co2 equivalents, Co2e factor and the parameters
    :rtype: Tuple[Kilogram, float, FerryEmissionParameters]
    """

    if options is None:
        options = {}
    params = FerryEmissionParameters.parse_obj(options)
    # Get the co2 factor
    co2e_factor = emission_factors.get(params.dict())
    # Calculate emissions
    co2e = distance * co2e_factor
    return co2e, co2e_factor, params


def calc_co2_bicycle(
    distance: Kilometer, options: Union[BicycleEmissionParameters, dict] = None
) -> Tuple[Kilogram, float, None]:
    """Calculate co2 emissions of a bicycle trip

    :param distance: Distance in km
    :param options: Options for the bicycle trip (only for error handling, no options allowed)
    :type distance: Kilometer
    :type options: Union[BicycleEmissionParameters, dict]
    :return: Total emissions of bicycle trip in co2 equivalents, Co2e factor and the parameters (None)
    :rtype: Tuple[Kilogram, float, None]
    """
    if options is None:
        options = {}
    params = BicycleEmissionParameters.parse_obj(options)
    # Get the co2 factor
    co2e_factor = emission_factors.get(params.dict())
    # Calculate emissions
    co2e = distance * co2e_factor
    return co2e, co2e_factor, None


def calc_co2_pedelec(
    distance: Kilometer, options: Union[PedelecEmissionParameters, dict] = None
) -> Tuple[Kilogram, float, None]:
    """Calculate co2 emissions of a pedelec trip

    :param distance: Distance in km
    :param options: Options for the pedelec trip (only for error handling, no options allowed)
    :type distance: Kilometer
    :type options: Union[PedelecEmissionParameters, dict]
    :return: Total emissions of pedelec trip in co2 equivalents, Co2e factor and the parameters (None)
    :rtype: Tuple[Kilogram, float, None]
    """
    if options is None:
        options = {}
    params = PedelecEmissionParameters.parse_obj(options)
    # Get the co2 factor
    co2e_factor = emission_factors.get(params.dict())
    # Calculate emissions
    co2e = distance * co2e_factor
    return co2e, co2e_factor, None


def calc_co2_tram(
    distance: Kilometer, options: Union[TramEmissionParameters, dict] = None
) -> Tuple[Kilogram, float, None]:
    """Calculate co2 emissions for commuting by tram

    :param distance: distance in km
    :param options: Options for the tram trip (only for error handling, no options allowed)
    :type distance: Kilometer
    :type options: Union[TramEmissionParameters, dict]
    :return: Total emissions of tram in co2 equivalents, Co2e factor and the parameters (None)
    :rtype: Tuple[Kilogram, float, None]
    """

    if options is None:
        options = {}
    params = TramEmissionParameters.parse_obj(options)
    # Get the co2 factor
    co2e_factor = emission_factors.get(params.dict())
    # Calculate emissions
    co2e = distance * co2e_factor
    return co2e, co2e_factor, None
