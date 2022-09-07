#!/usr/bin/env python
# coding: utf-8
"""Functions to calculate co2 emissions"""

from typing import Tuple
from ._types import Kilogram, Kilometer
from .constants import (
    KWH_TO_TJ,
    FerryClass,
    ElectricityFuel,
    RangeCategory
)
from .distances import create_distance_request, get_distance, DistanceRequest, StructuredLocation
from .parameters import CarEmissionParameters, BusEmissionParameters, TrainEmissionParameters, PlaneEmissionParameters
from .reader import Reader
from .enums import *


script_path = str(Path(__file__).parent)
emission_factor_df = pd.read_csv(f"{script_path}/../data/emission_factors.csv")
conversion_factor_df = pd.read_csv(
    f"{script_path}/../data/conversion_factors_heating.csv"
)
detour_df = pd.read_csv(f"{script_path}/../data/detour.csv")

reader = Reader()


def calc_co2_car(
    distance: Kilometer,
    passengers: int = None,
    size: str = None,
    fuel_type: str = None,
) -> Kilogram:
    """
    Function to compute the emissions of a car trip.
    :param distance: Distance travelled by car;
    :param passengers: Number of passengers in the car (including the person answering the questionnaire),
                        [1, 2, 3, 4, 5, 6, 7, 8, 9]                             default: 1
    :param size: size of car
                        ["small", "medium", "large", "average"]                 default: "average"
    :param fuel_type: type of fuel the car is using
                        ["diesel", "gasoline", "cng", "electric", "hybrid", "plug-in_hybrid", "average"]    default: "average"
    :type distance: Kilometer
    :type passengers: int
    :type size: str
    :type fuel_type: str
    :return: Total emissions of trip in co2 equivalents
    :rtype: Kilogram
    """
    # NOTE: Tests fail for 'cng'  as `fuel_type` (IndexError)
    # Set default values
    # params = {}
    if passengers is None:
         passengers = 1
         #warnings.warn(
         #    f"Number of car passengers was not provided. Using default value: '{passengers}'"
         #)
    # if size is not None:
    #     params["size"] = size
    #     #warnings.warn(f"Size of car was not provided. Using default value: '{size}'")
    # if fuel_type is not None:
    #     params["fuel_type"] = fuel_type
    #     #fuel_type = CarBusFuel.AVERAGE
    #     #warnings.warn(
    #     #    f"Car fuel type was not provided. Using default value: '{fuel_type}'"
    #     #)

    params = locals()
    params = {k: v for k, v in params.items() if v is not None}
    params = CarEmissionParameters(**params)
    co2e = reader.get_emission_factor(params.dict())

    # Get the co2 factor, calculate and return
    emissions = distance * co2e / int(passengers)

    return emissions


def calc_co2_motorbike(distance: Kilometer = None, size: str = None) -> Kilogram:
    """
    Function to compute the emissions of a motorbike trip.
    :param distance: Distance travelled by motorbike;
                        alternatively param <locations> can be provided
    :param size: size of motorbike
                        ["small", "medium", "large", "average"]
    :type distance: Kilometer
    :type size: str
    :return: Total emissions of trip in co2 equivalents
    :rtype: Kilogram
    """

    transport_mode = TransportationMode.Motorbike

    # Set default values
    #if size is None:
    #    size = Size.AVERAGE
        #warnings.warn(
        #    f"Size of motorbike was not provided. Using default value: '{size}'"
        #)

    co2e = emission_factor_df[
        (emission_factor_df["subcategory"] == transport_mode)
        & (emission_factor_df["size"] == size)
    ]["co2e"].values[0]
    emissions = distance * co2e

    return emissions


def calc_co2_bus(
    distance: Kilometer,
    size: str = None,
    fuel_type: str = None,
    occupancy: int = None,
    vehicle_range: str = None,
) -> Kilogram:
    """
    Function to compute the emissions of a bus trip.
    :param distance: Distance travelled by bus;
    :param size: size class of the bus;                 ["medium", "large", "average"]
    :param fuel_type: type of fuel the bus is using;    ["diesel"]
    :param occupancy: number of people on the bus       [20, 50, 80, 100]
    :param vehicle_range: range/haul of the vehicle     ["local", "long-distance"]
    :type distance: Kilometer
    :type size: str
    :type fuel_type: str
    :type occupancy: int
    :type vehicle_range: str
    :return: Total emissions of trip in co2 equivalents
    :rtype: Kilogram
    """
    # NOTE: vehicle_rage 'local' fails with IndexError
    # Set default values
    #if size is not None:
        #size = Size.AVERAGE
    #    params["size"] = size
        #warnings.warn(f"Size of bus was not provided. Using default value: '{size}'")
   # if fuel_type is not None:
   #     params["fuel_type"] = fuel_type
        #fuel_type = CarBusFuel.DIESEL
        #warnings.warn(
        #    f"Bus fuel type was not provided. Using default value: '{fuel_type}'"
        #)
    #elif fuel_type not in [CarBusFuel.DIESEL, CarBusFuel.CNG, CarBusFuel.HYDROGEN]:
    #    warnings.warn(
    #        f"Bus fuel type {fuel_type} not available. Using default value: 'diesel'"
    #    )
    #    fuel_type = "diesel"
    #if occupancy is not None:
    #    params["occupancy"] = occupancy
        # occupancy = "c_50"
        #warnings.warn(f"Occupancy was not provided. Using default value: '{occupancy}'")
    #if vehicle_range is not None:
    #    params["vehicle_range"] = vehicle_range
        #vehicle_range = BusTrainRange.LONG_DISTANCE
        #warnings.warn(
        #    f"Intended range of trip was not provided. Using default value: '{vehicle_range}'"
        #)
    params = locals()
    params = {k: v for k, v in params.items() if v is not None}

    params = BusEmissionParameters(**params)
    co2e = reader.get_emission_factor(params.dict())

    # Get co2 factor, calculate and return
    #co2e = emission_factor_df[
    #    (emission_factor_df["subcategory"] == transport_mode)
    #    & (emission_factor_df["size"] == size)
    #    & (emission_factor_df["fuel_type"] == fuel_type)
    #    & (emission_factor_df["occupancy"] == occupancy)
    #    & (emission_factor_df["range"] == vehicle_range)
    #]["co2e"].values[0]
    emissions = distance * co2e

    return emissions


def calc_co2_train(
    distance: Kilometer,
    fuel_type: str = None,
    vehicle_range: str = None,
) -> Kilogram:
    """
    Function to compute the emissions of a train trip.
    :param distance: Distance travelled by train;
    :param fuel_type: type of fuel the train is using;    ["diesel", "electric", "average"]
    :param vehicle_range: range/haul of the vehicle       ["local", "long-distance"]
    :type distance: Kilometer
    :type fuel_type: float
    :type vehicle_range: str
    :return: Total emissions of trip in co2 equivalents
    :rtype: Kilogram
    """
    # Set default values
    #if fuel_type is None:

        #fuel_type = CarBusFuel.AVERAGE
        #warnings.warn(
        #    f"Car fuel type was not provided. Using default value: '{fuel_type}'"
        #)
    #if vehicle_range is None:
    #    #vehicle_range = BusTrainRange.LONG_DISTANCE
   #     warnings.warn(
   #         f"Intended range of trip was not provided. Using default value: '{vehicle_range}'"
   #     )

    params = locals()
    params = {k: v for k, v in params.items() if v is not None}
    params = TrainEmissionParameters(**params)
    co2e = reader.get_emission_factor(params.dict())
    print(co2e)
    # Get the co2 factor, calculate and return
    #co2e = emission_factor_df[
    #    (emission_factor_df["subcategory"] == transport_mode)
    #    & (emission_factor_df["fuel_type"] == fuel_type)
    #    & (emission_factor_df["range"] == vehicle_range)
    #]["co2e"].values[0]
    emissions = distance * co2e
    print(emissions)
    return emissions


def calc_co2_plane(distance: Kilometer, seating: str = None) -> Kilogram:
    """
    Function to compute emissions of a plane trip
    :param distance: Distance of plane flight
    :param seating_class: Seating class in the airplane; Emission factors differ between seating classes because
                          business class or first class seats take up more space. An airplane with more such therefore
                          needs to have higher capacity to transport less people -> more co2
                          ["average", "economy_class", "business_class", "premium_economy_class", "first_class"]
    :type distance: Kilometer
    :type seating_class: str
    :return: Total emissions of flight in co2 equivalents
    :rtype: Kilogram
    """

    #transport_mode = TransportationMode.Plane

    # Set defaults
    #if seating_class is None:
    #    seating_class = PlaneSeatingClass.Average
    #    warnings.warn(
    #        f"Seating class was not provided. Using default value: '{seating_class}'"
    #    )

    params = locals()
    params = {k: v for k, v in params.items() if v is not None}

    # Retrieve whether distance is below or above 1500 km
    if distance <= 1500:
        params["range"] = PlaneRange.Short_haul
    else:
        params["range"] = PlaneRange.Long_haul
    # NOTE: Should be checked before geocoding and haversine calculation
    #seating_choices = [item for item in PlaneSeatingClass]

    #if seating_class not in seating_choices:
    #    raise ValueError(
    #        f"No emission factor available for the specified seating class '{seating_class}'.\n"
    #        f"Please use one of the following: {seating_choices}"
    #    )

    params = PlaneEmissionParameters(**params)
    co2e = reader.get_emission_factor(params.dict())

    # Get co2 factor, calculate and return
    # try:
    #
    #     co2e = emission_factor_df[
    #         (emission_factor_df["subcategory"] == transport_mode)
    #         & (emission_factor_df["range"] == flight_range)
    #         & (emission_factor_df["seating"] == seating_class)
    #     ]["co2e"].values[0]
    # except IndexError:
    #     default_seating = FlightClass.ECONOMY
    #     warnings.warn(
    #         f"Seating class '{seating_class}' not available for {flight_range} flights. Switching to "
    #         f"'{default_seating}'..."
    #     )
    #     co2e = emission_factor_df[
    #         (emission_factor_df["range"] == flight_range)
    #         & (emission_factor_df["seating"] == default_seating)
    #     ]["co2e"].values[0]
    # multiply emission factor with distance
    emissions = distance * co2e

    return emissions


def calc_co2_ferry(distance: Kilometer, seating: str = None) -> Kilogram:
    """
    Function to compute emissions of a ferry trip
    :param distance: Distance of ferry trip
    :param seating_class: ["average", "Foot passenger", "Car passenger"]
    :type distance: Kilometer
    :type seating_class: str
    :return: Total emissions of sea travel in co2 equivalents
    :rtype: Kilogram
    """
    # NOTE: 'Foot passenger' and 'Car passenger' fails with IndexError

    transport_mode = TransportationMode.Ferry

    if seating is None:
        seating = FerryClass.AVERAGE
        #warnings.warn(
        #    f"Seating class was not provided. Using default value: '{seating_class}'"
        #)

    # get emission factor
    co2e = emission_factor_df[
        (emission_factor_df["subcategory"] == transport_mode)
        & (emission_factor_df["seating"] == seating)
    ]["co2e"].values[0]
    # multiply emission factor with distance
    emissions = distance * co2e

    return emissions


def calc_co2_electricity(
    consumption: float, fuel_type: str = None, energy_share: float = 1
) -> Kilogram:
    """Function to compute electricity emissions

    :param consumption: energy consumption
    :param fuel_type: energy (mix) used for electricity [german_energy_mix, solar]
    :param energy_share: the research group's approximate share of the total electricity energy consumption
    :type consumption: float
    :type fuel_type: str
    :type energy_share: float
    :return: total emissions of electricity energy consumption
    :rtype: Kilogram
    """
    # Set defaults
    if fuel_type is None:
        fuel_type = ElectricityFuel.GERMAN_ENERGY_MIX
        #warnings.warn(
        #    f"No fuel type or energy mix specified. Using default value: '{fuel_type}'"
        #)
    co2e = emission_factor_df[
        (emission_factor_df["category"] == "electricity")
        & (emission_factor_df["fuel_type"] == fuel_type)
    ]["co2e"].values[0]
    # co2 equivalents for heating and electricity refer to a consumption of 1 TJ
    # so consumption needs to be converted to TJ
    emissions = consumption * energy_share / KWH_TO_TJ * co2e

    return emissions


def calc_co2_heating(
    consumption: float, fuel_type: str, unit: str = None, area_share: float = 1.0
) -> Kilogram:
    """Function to compute heating emissions

    :param consumption: energy consumption
    :param fuel_type: fuel type used for heating [coal, district_heating, electricity, gas, heat_pump_air, heat_pump_ground, liquid_gas, oil, pellet, solar, woodchips]
    :param unit: unit of energy consumption [kwh, kg, l, m^3]
    :param area_share: share of building area used by research group
    :type consumption: float
    :type fuel_type: str
    :type unit: str
    :type area_share: float
    :return: total emissions of heating energy consumption
    :rtype: Kilogram
    """
    # Set defaults
    if unit is None:
        unit = "kWh"
        #warnings.warn(f"Unit was not provided. Assuming default value: '{unit}'")
    #if area_share > 1:
        #warnings.warn(
        #    f"Share of building area must be a float in the interval (0,1], but was set to '{area_share}'\n."
        #    f"The parameter will be set to '1.0' instead"
        #)
    valid_unit_choices = ["kWh", "l", "kg", "m^3"]
    assert (
        unit in valid_unit_choices
    ), f"unit={unit} is invalid. Valid choices are {', '.join(valid_unit_choices)}"
    if unit != "kWh":
        try:
            conversion_factor = conversion_factor_df[
                (conversion_factor_df["fuel"] == fuel_type)
                & (conversion_factor_df["unit"] == unit)
            ]["conversion_value"].values[0]
        except KeyError:
            raise ValueError(
                f"""
                No conversion data is available for this fuel type.
                Conversion is only supported for the following fuel types and units:
                {conversion_factor_df["fuel", "unit"]}.
                Alternatively, provide consumption in the unit kWh.
                """
            )

        consumption_kwh = consumption * conversion_factor
    else:
        consumption_kwh = consumption

    co2e = emission_factor_df[
        (emission_factor_df["category"] == "heating")
        & (emission_factor_df["fuel_type"] == fuel_type)
    ]["co2e"].values[0]
    # co2 equivalents for heating and electricity refer to a consumption of 1 TJ
    # so consumption needs to be converted to TJ
    emissions = consumption_kwh * area_share / KWH_TO_TJ * co2e

    return emissions


def calc_co2_businesstrip(
    transportation_mode: str,
    start=None,
    destination=None,
    distance: Kilometer = None,
    size: str = None,
    fuel_type: str = None,
    occupancy: int = None,
    seating: str = None,
    passengers: int = None,
    roundtrip: bool = False,
) -> Tuple[Kilogram, Kilometer, str, str]:
    """Function to compute emissions for business trips based on transportation mode and trip specifics

    :param transportation_mode: mode of transport [car, bus, train, plane, ferry]
    :param start: Start of the trip (alternatively, distance can be provided)
    :param destination: Destination of the trip (alternatively, distance can be provided)
    :param distance: Distance travelled in km (alternatively, start and destination can be provided)
    :param size: Size class of the vehicle [small, medium, large, average] - only used for car and bus
    :param fuel_type: Fuel type of the vehicle [average, cng, diesel, electric, gasoline, hybrid, hydrogen, plug-in_hybrid] - only used for
                                                car, bus and train
    :param occupancy: Occupancy of the vehicle in % [20, 50, 80, 100] - only used for bus
    :param seating: seating class ["average", "Economy class", "Premium economy class", "Business class", "First class"]
                    - only used for plane
    :param passengers: Number of passengers in the vehicle (including the participant), number from 1 to 9
                                                - only used for car
    :param roundtrip: whether the trip is a round trip or not [True, False]
    :type transportation_mode: str
    :type distance: Kilometer
    :type size: str
    :type fuel_type: str
    :type occupancy: int
    :type seating: str
    :type passengers: int
    :type roundtrip: bool
    :return:    Emissions of the business trip in co2 equivalents,
                Distance of the business trip,
                Range category of the business trip [very short haul, short haul, medium haul, long haul]
                Range description (i.e., what range of distances does to category correspond to)
    :rtype: tuple[Kilogram, Kilometer, str, str]
    """

    # Evaluate if distance- or stop-based request.
    # Rules:
    # - `distance` is dominant;
    # - if distance not provided, take stops;
    # - if stops not available, raise error;
    # In general:
    # - If stop-based, calculate distance first, then continue only distance-based

    if not distance:
        request = DistanceRequest(
                transportation_mode=transportation_mode,
                start=StructuredLocation(**start),
                destination=StructuredLocation(**destination),
            )
        #request = create_distance_request(start, destination, transportation_mode)
        distance = get_distance(request)

    if transportation_mode == TransportationMode.Car:
        emissions = calc_co2_car(
            distance=distance,
            passengers=passengers,
            size=size,
            fuel_type=fuel_type,
        )

    elif transportation_mode == TransportationMode.Bus:
        emissions = calc_co2_bus(
            distance=distance,
            size=size,
            fuel_type=fuel_type,
            occupancy=occupancy,
            vehicle_range=TrainRange.Long_distance,
        )

    elif transportation_mode == TransportationMode.Train:
        emissions = calc_co2_train(
            distance=distance,
            fuel_type=fuel_type,
            vehicle_range=TrainRange.Long_distance,
        )

    elif transportation_mode == TransportationMode.Plane:
        emissions = calc_co2_plane(distance, seating=seating)

    elif transportation_mode == TransportationMode.Ferry:
        emissions = calc_co2_ferry(distance, seating=seating)

    else:
        raise ValueError(
            f"No emission factor available for the specified mode of transport '{transportation_mode}'."
        )
    if roundtrip is True:
        emissions *= 2

    # categorize according to distance (range)
    range_category, range_description = range_categories(distance)

    return emissions, distance, range_category, range_description


def range_categories(distance: Kilometer) -> Tuple[RangeCategory, str]:
    """Function to categorize a trip according to the travelled distance

    :param distance: Distance travelled in km
    :type distance: Kilometer
    :return: Range category of the trip [very short haul, short haul, medium haul, long haul]
             Range description (i.e., what range of distances does to category correspond to)
    :rtype: tuple[RangeCategory, str]
    """
    if distance <= 500:
        range_cat = RangeCategory.VERY_SHORT_HAUL
        range_description = "below 500 km"
    elif distance <= 1500:
        range_cat = RangeCategory.SHORT_HAUL
        range_description = "500 to 1500 km"
    elif distance <= 4000:
        range_cat = RangeCategory.MEDIUM_HAUL
        range_description = "1500 to 4000 km"
    else:
        range_cat = RangeCategory.LONG_HAUL
        range_description = "above 4000 km"

    return range_cat, range_description


def calc_co2_commuting(
    transportation_mode: str,
    weekly_distance: Kilometer,
    size: str = None,
    fuel_type: str = None,
    occupancy: int = None,
    passengers: int = None,
) -> Kilogram:
    """Calculate co2 emissions for commuting per mode of transport

    :param transportation_mode: [car, bus, train, bicycle, pedelec, motorbike, tram]
    :param weekly_distance: distance in km per week
    :param size: size of car or bus if applicable: [small, medium, large, average]
    :param fuel_type: fuel type of car, bus or train if applicable
    :param occupancy: occupancy [%], if applicable/known (only for bus): [20, 50, 80, 100]
    :param passengers: number of passengers, if applicable (only for car)
    :type transportation_mode: str
    :type weekly_distance: Kilometer
    :type size: str
    :type fuel_type: str
    :type occupancy: int
    :type passengers: int
    :return: total weekly emissions for the respective mode of transport
    :rtype: Kilogram
    """

    # get weekly co2e for respective mode of transport
    if transportation_mode == TransportationMode.Car:
        weekly_co2e = calc_co2_car(
            passengers=passengers,
            size=size,
            fuel_type=fuel_type,
            distance=weekly_distance,
        )

    elif transportation_mode == TransportationMode.Motorbike:
        weekly_co2e = calc_co2_motorbike(size=size, distance=weekly_distance)
    elif transportation_mode == TransportationMode.Bus:
        weekly_co2e = calc_co2_bus(
            size=size,
            fuel_type=fuel_type,
            occupancy=occupancy,
            vehicle_range="local",
            distance=weekly_distance,
        )

    elif transportation_mode == TransportationMode.Train:
        weekly_co2e = calc_co2_train(
            fuel_type=fuel_type, vehicle_range="local", distance=weekly_distance
        )

    elif transportation_mode == TransportationMode.Tram:
        # NOTE: It's recommended to still move such small things to own methods.
        # (Easier to test and maintain)
        co2e = emission_factor_df[
            (emission_factor_df["name"] == "Strassen-Stadt-U-Bahn")
        ]["co2e"].values[0]
        weekly_co2e = co2e * weekly_distance

    elif transportation_mode in [
        TransportationMode.Pedelec,
        TransportationMode.Bicycle,
    ]:
        # NOTE: It's recommended to still move such small things to own methods.
        # (Easier to test and maintain)
        co2e = emission_factor_df[
            (emission_factor_df["subcategory"] == transportation_mode)
        ]["co2e"].values[0]
        weekly_co2e = co2e * weekly_distance

    else:
        raise ValueError(
            f"Transportation mode {transportation_mode} not found in database."
        )

    return weekly_co2e


def commuting_emissions_group(
    aggr_co2: Kilogram, n_participants: int, n_members: int
) -> Kilogram:
    """Calculate the group's co2e emissions from commuting.

    .. note:: Assumption: a representative sample of group members answered the questionnaire.

    :param aggr_co2: (Annual/monthly) co2e emissions from commuting, aggregated for all group members who answered the
                            questionnaire (can also be calculated for only one mode of transport)
    :param n_participants: Number of group members who answered the questionnaire
    :param n_members: Total number of members of the group
    :type aggr_co2: Kilogram
    :type n_participants: int
    :type n_members: int
    :return: Calculated or estimated emissions of the entire working group.
    :rtype: Kilogram
    """
    group_co2e = aggr_co2 / n_participants * n_members

    return group_co2e
