"""Function colleciton to calculate mobility type co2 emissions"""

from typing import Union
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
) -> Kilogram:
    """
    Function to compute the emissions of a car trip.
    :param distance: Distance travelled by car;
    :param options: Options for the car trip;
    :return: Total emissions of trip in co2 equivalents, Co2e factor and the parameters
    :rtype: Kilogram
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
) -> Kilogram:
    """
    Function to compute the emissions of a motorbike trip.
    :param distance: Distance travelled by motorbike;
                        alternatively param <locations> can be provided
    :param options: Options for the motorbike trip;
    :type distance: Kilometer
    :type size: str
    :return: Total emissions of trip in co2 equivalents, Co2e factor and the parameters
    :rtype: Kilogram
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
    distance: Kilometer, options: Union[BusEmissionParameters, dict] =None
) -> Kilogram:
    """
    Function to compute the emissions of a bus trip.
    :param distance: Distance travelled by bus;
                        alternatively param <locations> can be provided
    :param options: Options for the bus trip;
    :type distance: Kilometer
    :type size: str
    :type fuel_type: str
    :type vehicle_range: str
    :return: Total emissions of trip in co2 equivalents, Co2e factor and the parameters
    :rtype: Kilogram
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
) -> Kilogram:
    """
    Function to compute the emissions of a train trip.
    :param distance: Distance travelled by train;
    :param options: Options for the train trip;
    :type distance: Kilometer
    :type fuel_type: float
    :type vehicle_range: str
    :return: Total emissions of trip in co2 equivalents, Co2e factor and the parameters
    :rtype: Kilogram
    """

    if options is None:
        options = {}
    params = TrainEmissionParameters.parse_obj(options)
    # Get the co2 factor
    co2e_factor = emission_factors.get(params.dict())
    # Calculate emissions
    co2e = distance * co2e_factor
    return co2e, co2e_factor, params


def calc_co2_plane(distance: Kilometer, options: PlaneEmissionParameters = None) -> Kilogram:
    """
    Function to compute emissions of a plane trip
    :param distance: Distance of plane flight
    :param options: Options for the plane trip
    :type distance: Kilometer
    :type seating: str
    :return: Total emissions of flight in co2 equivalents, Co2e factor and the parameters
    :rtype: Kilogram
    """

    if options is None:
        options = {}
    # Retrieve whether distance is <= 3700 or above 3700 km
    if distance is None:
        raise ValueError("Distance is not given. Range can not be calculated.")
    if distance <= 3700:
        options["range"] = FlightRange.SHORT_HAUL
    else:
        options["range"] = FlightRange.LONG_HAUL

    params = PlaneEmissionParameters.parse_obj(options)
    # Get the co2 factor
    co2e_factor = emission_factors.get(params.dict())
    # Calculate emissions
    co2e = distance * co2e_factor
    return co2e, co2e_factor, params


def calc_co2_ferry(
    distance: Kilometer, options: Union[FerryEmissionParameters, dict] = None
) -> Kilogram:
    """
    Function to compute emissions of a ferry trip
    :param distance: Distance of ferry trip
    :param options: Options for the ferry trip
    :type distance: Kilometer
    :type seating: str
    :return: Total emissions of sea travel in co2 equivalents, Co2e factor and the Parameters
    :rtype: Kilogram
    """

    if options is None:
        options = {}
    params = FerryEmissionParameters.parse_obj(options)
    # Get the co2 factor
    co2e_factor = emission_factors.get(params.dict())
    # Calculate emissions
    co2e = distance * co2e_factor
    return co2e, co2e_factor, params


def calc_co2_bicycle(distance: Kilometer, options: Union[BicycleEmissionParameters, dict] = None) -> Kilogram:
    """Calculate co2 emissions for commuting by bicycle

    :param distance: distance in km
    :return: Total emissions of bicycle in co2 equivalents, Co2e factor and the parameters
    :rtype: Kilogram
    """
    if options is None:
        options = {}
    params = PedelecEmissionParameters.parse_obj(options)
    # Get the co2 factor
    co2e_factor = emission_factors.get(params.dict())
    # Calculate emissions
    co2e = distance * co2e_factor
    return co2e, co2e_factor, None


def calc_co2_pedelec(distance: Kilometer, options: Union[PedelecEmissionParameters, dict] = None) -> Kilogram:
    """Calculate co2 emissions for commuting by pedelec

    :param distance: distance in km
    :return: Total emissions of pedelec in co2 equivalents, Co2e factor and the parameters
    :rtype: Kilogram
    """
    if options is None:
        options = {}
    params = PedelecEmissionParameters.parse_obj(options)
    # Get the co2 factor
    co2e_factor = emission_factors.get(params.dict())
    # Calculate emissions
    co2e = distance * co2e_factor
    return co2e, co2e_factor, None


def calc_co2_tram(distance : Kilometer, options: Union[TramEmissionParameters, dict] = None) -> Kilogram:
    """Calculate co2 emissions for commuting by tram
    :param options: Options for the tram trip
    :param distance: distance in km
    :return: Total emissions of tram in co2 equivalents, Co2e factor and the parameters
    :rtype: Kilogram
    """

    if options is None:
        options = {}
    params = TramEmissionParameters.parse_obj(options)
    # Get the co2 factor
    co2e_factor = emission_factors.get(params.dict())
    # Calculate emissions
    co2e = distance * co2e_factor
    return co2e, co2e_factor, None
