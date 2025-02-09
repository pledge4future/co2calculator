#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Functions for obtaining the distance between given addresses."""

import os
import warnings
from pathlib import Path
from typing import Tuple, Union, Optional

import numpy as np
import openrouteservice
from dotenv import load_dotenv
from openrouteservice.directions import directions
from openrouteservice.geocode import pelias_search, pelias_structured
from pydantic import BaseModel, ValidationError, Extra, confloat
from thefuzz import fuzz
from thefuzz import process

from ._types import Kilometer
from .constants import (
    TransportationMode,
    AddressType,
    CountryCode2,
    CountryCode3,
    CountryName,
    IataAirportCode,
    DetourCoefficient,
    DetourConstant,
    RangeCategory,
    RoutingProfile,
)
from .data_handlers import Airports, EUTrainStations

load_dotenv()  # take environment variables from .env.

# Load environment vars (TODO: Use pydantic.BaseSettings)
ORS_API_KEY = os.environ.get("ORS_API_KEY")
# TODO: check if key exists or is valid
script_path = str(Path(__file__).parent)


class StructuredLocation(BaseModel, extra=Extra.forbid):
    address: Optional[str]
    locality: str
    country: Optional[Union[CountryCode2, CountryCode3, CountryName]]
    region: Optional[str]
    county: Optional[str]
    borough: Optional[str]
    postalcode: Optional[str]
    neighbourhood: Optional[str]


class TrainStation(BaseModel, extra=Extra.forbid):
    station_name: str
    country: CountryCode2


class Airport(BaseModel, extra=Extra.forbid):
    iata_code: IataAirportCode


class DistanceRequest(BaseModel):
    transportation_mode: TransportationMode
    start: Union[StructuredLocation, TrainStation, Airport]
    destination: Union[StructuredLocation, TrainStation, Airport]


class Coordinate(BaseModel):
    lat: confloat(ge=-90, le=90)
    long: confloat(ge=-180, le=180)
    lat_rad: confloat(ge=-np.pi / 2, le=np.pi / 2) = None
    long_rad: confloat(ge=-np.pi, le=np.pi) = None

    def deg2rad(self):
        self.lat_rad = np.deg2rad(self.lat)
        self.long_rad = np.deg2rad(self.long)


# Module's exceptions
class InvalidSpatialInput(Exception):
    """Raised when consumer inputs invalid spatial information"""


def haversine(
    lat_start: float, long_start: float, lat_dest: float, long_dest: float
) -> Kilometer:
    """Function to compute the distance as the crow flies between given locations

    :param lat_start: latitude of start
    :param long_start: Longitude of start
    :param lat_dest: Latitude of destination
    :param long_dest: Longitude of destination
    :type lat_start: float
    :type long_start: float
    :type lat_dest: float
    :type long_dest: float
    :return: Distance
    :rtype: Kilometer
    """
    start = Coordinate(lat=lat_start, long=long_start)
    dest = Coordinate(lat=lat_dest, long=long_dest)

    # convert angles from degree to radians
    start.deg2rad()
    dest.deg2rad()

    # compute zeta
    a = (
        np.sin((dest.lat_rad - start.lat_rad) / 2) ** 2
        + np.cos(start.lat_rad)
        * np.cos(dest.lat_rad)
        * np.sin((dest.long_rad - start.long_rad) / 2) ** 2
    )
    c = 2 * np.arcsin(np.sqrt(a))
    r = 6371

    return c * r


def geocoding_airport_pelias(
    iata: IataAirportCode,
) -> Tuple[str, Tuple[float, float], str]:
    """Function to obtain the coordinates of an airport by the IATA code

    :param iata: IATA airport code
    :type iata: str
    :return: name, coordinates and country of the found airport
    :rtype: Tuple[str, Tuple[float, float], str]
    """
    clnt = openrouteservice.Client(key=ORS_API_KEY)

    call = pelias_search(clnt, f"{iata} Airport")

    for feature in call["features"]:
        try:
            if feature["properties"]["addendum"]["osm"]["iata"] == iata:
                name = feature["properties"]["name"]
                geom = feature["geometry"]["coordinates"]
                country = feature["properties"]["country_a"]
                break
        except KeyError:
            # unfortunately, not all osm tags are available with geocoding, so osm entries might not be found and filter
            # for "aerodrome" tag not possible (could be done with ORS maybe?)
            if (feature["properties"]["confidence"] == 1) & (
                feature["properties"]["match_type"] == "exact"
            ):
                name = feature["properties"]["name"]
                geom = feature["geometry"]["coordinates"]
                country = feature["properties"]["country_a"]
                break

    return name, geom, country


def geocoding_airport(iata: IataAirportCode) -> Tuple[str, Tuple[float, float], str]:
    """Function to obtain the coordinates of an airport by the IATA code

    :param iata: IATA airport code
    :type iata: str
    :return: name, coordinates and country of the found airport
    :rtype: Tuple[str, Tuple[float, float], str]
    """
    df_airports = Airports().airports

    airport = Airport(iata_code=iata)
    name, lat, lon, country = (
        df_airports[df_airports.iata_code == airport.iata_code][
            ["name", "latitude_deg", "longitude_deg", "iso_country"]
        ]
        .values.flatten()
        .tolist()
    )
    # coords is a string - convert to list of floats
    coords = [lon, lat]

    return name, coords, country


def geocoding(address):
    """Function to obtain coordinates for a given address

    :param address: Location/Address to be searched
            user should give address in the form:
            <address>, <locality>, <country>
            e.g. Hauptbahnhof, Heidelberg, Germany
            e.g. Im Neuenheimer Feld 348, Heidelberg, Germany
            e.g. Heidelberg, Germany
    :return: Name, country and coordinates of the found location
    """

    clnt = openrouteservice.Client(key=ORS_API_KEY)

    call = pelias_search(clnt, address)
    for feature in call["features"]:
        name = feature["properties"]["name"]
        country = feature["properties"]["country"]
        coords = feature["geometry"]["coordinates"]
        break

    return name, country, coords


def geocoding_structured(loc_dict):
    """Function to obtain coordinates for a given address

    :param loc_dict: dictionary describing the location.

    .. code-block:: none

     The dictionary can have the keys:
        country:        highest-level administrative divisions supported in a search.

                        Full country name or two-/three-letter abbreviations supported
                        e.g., Germany / "DE" / "DEU"

        region:         first-level administrative divisions within countries, analogous to states and provinces
                        in the US and Canada
                        e.g., Delaware, Ontario, Ardennes, Baden-Württemberg

        county:         administrative divisions between localities and regions
                        e.g., Alb-Donau-Kreis

        locality:       equivalent to what are commonly referred to as cities
                        e.g., Bangkok, Caracas

        borough:        mostly known in the context of NY, may exist in other cities like Mexico City
                        e.g. Manhattan in NY, Iztapalapa in Mexico City

        postalcode:     postal code; !! Not working in many countries !!

        address:        street name, optionally also house number

        neighbourhood:  vernacular geographic entities that may not necessarily be official administrative
                        divisions but are important nonetheless
                        e.g. Notting Hill in London, Le Marais in Paris

    :return: Name, country and coordinates of the found location
    """

    clnt = openrouteservice.Client(key=ORS_API_KEY)

    location = StructuredLocation(**loc_dict)

    call = pelias_structured(clnt, **location.dict())
    n_results = len(call["features"])
    res = call["features"]
    assert n_results != 0, "No places found with these search parameters"
    if n_results == 0:
        raise Exception("No places found with these search parameters")

    # TODO: Validate response with a pydantic.BaseModel (`PeliasStructuredResponse`)
    # TODO: Unpack required data from response with a pydantic.BaseModel which we use internally
    # as Point of Interest (or similar, e.g., `PointOfInterest`)
    for feature in res:
        name = feature["properties"]["name"]
        country = feature["properties"]["country"]
        coords = feature["geometry"]["coordinates"]
        layer = feature["properties"]["layer"]
        if "locality" in loc_dict.keys() and "address" in loc_dict.keys():
            if (
                layer != "address" and layer != "locality" and layer != "street"
            ) and n_results > 1:
                warnings.warn(
                    f"Data type not matching search ({layer} instead of address or locality. Skipping {name}, {coords}",
                    stacklevel=2,
                )
                continue
        confidence = feature["properties"]["confidence"]
        if confidence < 0.8:
            warnings.warn(
                f"Low confidence: {confidence:.1f} for result {name}, {coords}",
                stacklevel=2,
            )
        break
    print(
        f"{n_results} location(s) found. Using this result: {name}, {country} (data type: {layer})"
    )
    print("Coords: ", coords)

    # todo: check if to return res or not!
    return name, country, coords, res


def geocoding_train_stations(loc_dict):
    """Function to obtain coordinates for a given train station

    :param loc_dict: dictionary describing the location.

    .. code-block:: none

     The dictionary can have the keys:

        country:        highest-level administrative divisions supported in a search.
                        Only two-letter abbreviations supported
                        e.g., 'DE'

        station_name:   Name of the train station
                        e.g., 'Heidelberg Hbf'

    :return: Name, country and coordinates of the found location
    """
    eu_train_stations = EUTrainStations().stations
    station = TrainStation(**loc_dict)

    country_code = station.country
    countries_eu = eu_train_stations["country"].unique()

    if country_code not in countries_eu:
        warnings.warn(
            "The provided country is not within Europe. "
            "Please provide the address of the station instead of the station name for accurate results.",
            stacklevel=2,
        )

    # filter stations by country
    stations_in_country = eu_train_stations[
        eu_train_stations["country"] == country_code
    ]

    # use thefuzz to find best match
    choices = stations_in_country["slug"].values
    res_station_slug, score = process.extractOne(
        station.station_name, choices, scorer=fuzz.partial_ratio
    )
    res_station = stations_in_country[stations_in_country["slug"] == res_station_slug]
    res_country, res_station_name = res_station[["country", "name"]].values[0]

    coords = (res_station.iloc[0]["latitude"], res_station.iloc[0]["longitude"])

    return res_station_name, res_country, coords


def get_route(coords: list, profile: RoutingProfile = None) -> Kilometer:
    """Obtain the distance of a route between given waypoints using a given profile
    todo: check if coords may also be a tuple/array etc.

    :param coords: list of [lat,long] coordinates
    :param profile: driving-car, cycling-regular
    :type coords: list
    :type profile: str
    :return: distance of the route
    :rtype: Kilometer
    """
    clnt = openrouteservice.Client(key=ORS_API_KEY)

    # profile may be: driving-car, cycling-regular
    if profile not in [RoutingProfile.CAR, RoutingProfile.CYCLING] or profile is None:
        profile = RoutingProfile.CAR
        warnings.warn(
            f"Warning! Specified profile not available or no profile passed.\n"
            f"Profile set to '{profile}' by default.",
            stacklevel=2,
        )
    route = directions(clnt, coords, profile=profile)
    dist = (
        route["routes"][0]["summary"]["distance"] / 1000
    )  # divide by 1000, as we're working with distances in km

    return dist


def get_route_ferry(
    coords: list, profile: RoutingProfile = None
) -> Tuple[Kilometer, Kilometer]:
    """Obtain the distance of a ferry route (and the total trip distance) between given waypoints
    todo: check if coords may also be a tuple/array etc.

    :param coords: list of [lat,long] coordinates
    :param profile: driving-car, foot-walking
    :type coords: list
    :type profile: str
    :return: distance of the ferry crossing, total distance
    :rtype: Kilometer, Kilometer
    """
    # profile may be: driving-car, walking
    clnt = openrouteservice.Client(key=ORS_API_KEY)

    if profile not in [RoutingProfile.WALK, RoutingProfile.CAR] or profile is None:
        profile = RoutingProfile.WALK
        warnings.warn(
            f"Warning! Specified profile not available or no profile passed.\n"
            f"Profile set to '{profile}' by default.",
            stacklevel=2,
        )
    res = directions(clnt, coords, profile=profile, extra_info=["waytype"])
    """waytypes = {0: "Unknown",
                1: "State Road",
                2: "Road",
                3: "Street",
                4: "Path",
                5: "Track",
                6: "Cycleway",
                7: "Footway",
                8: "Steps",
                9: "Ferry",
                10: "Construction"}"""
    dist_per_waytype = res["routes"][0]["extras"]["waytypes"]["summary"]
    try:
        dist_ferry = [d["distance"] for d in dist_per_waytype if d["value"] == 9.0][
            0
        ] / 1000
    except IndexError:
        # todo: raise Error
        raise InvalidSpatialInput(
            "The generated route does not contain any ferry crossing. Are you sure about the waypoints?"
        )
        dist_ferry = 0.0
    total_dist = (
        res["routes"][0]["summary"]["distance"] / 1000
    )  # divide by 1000, as we're working with distances in km

    if (dist_ferry + 100) < total_dist and dist_ferry != 0.0:
        warnings.warn(
            """
            "Total distance is much larger than ferry crossing.
            Your ferry route might not be contained in the database.
            If you are sure you entered the correct addresses of the ferry ports, consider entering
            the approximate ferry trip distance directly instead of the port addresses.
            """,
            UserWarning,
            stacklevel=2,
        )

    return dist_ferry, total_dist


def _apply_detour(
    distance: Kilometer, transportation_mode: TransportationMode
) -> Kilometer:
    """Function to apply specific detour parameters to a distance as the crow flies

    :param distance: Distance as the crow flies between location of departure and destination of a trip
    :param transportation_mode: Mode of transport used in the trip
    :type distance: Kilometer
    :type transportation_mode: str
    :return: Distance accounted for detour
    :rtype: Kilometer
    """
    try:
        detour_coefficient = DetourCoefficient[transportation_mode.upper()]
        detour_constant = DetourConstant[transportation_mode.upper()]
    except KeyError:
        detour_coefficient = 1.0
        detour_constant = 0.0
        warnings.warn(
            f"""
        No detour coefficient or constant available for this transportation mode.
        Detour parameters are available for the following transportation modes:
        {list(DetourCoefficient)}
        Using detour_coefficient = {detour_coefficient} and detour_constant = {detour_constant}.
        """,
            stacklevel=2,
        )
    distance_with_detour = detour_coefficient * distance + detour_constant

    return distance_with_detour


def range_categories(distance: Kilometer) -> Tuple[RangeCategory, str]:
    """Function to categorize a trip according to the travelled distance

    :param distance: Distance travelled in km
    :type distance: Kilometer
    :return: Range category of the trip [very short haul, short haul, medium haul, long haul]
             Range description (i.e., what range of distances does to category correspond to)
    :rtype: tuple[RangeCategory, str]
    """
    if distance < 0:
        raise ValueError("Distance must not be negative!")
    elif distance <= 500:
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


def create_distance_request(
    start: dict,
    destination: dict,
    transportation_mode: TransportationMode,
) -> DistanceRequest:
    """Transform and validate the user input into a proper model for distance calculations

    Raises:
    - InvalidSpatialInput for validation error
    - InvalidSpatialInput for unknown transportation_mode
    :param start: Start of the trip
    :param destination: Destination of the trip
    :param transportation_mode: Mode of transport used in the trip
    :type start: Union[str, dict]
    :type destination: Union[str, dict]
    :type transportation_mode: TransportationMode
    :return: Request for distance calculation between two locations for a given transportation mode
    :rtype: DistanceRequest
    """

    # Validate the spatial data wrt. the mode of transportation
    # And creates a DistanceRequest object containing either StructuredLocation,
    # TrainStation or Airport objects based on the unser input address_type
    # for start and destination, if nothing is given assume StructuredLocation

    try:
        locations = [None, None]
        for i, o in enumerate([start, destination]):
            if isinstance(o, dict):
                if "address_type" in o:
                    if o["address_type"] == AddressType.ADDRESS:
                        del o["address_type"]
                        locations[i] = StructuredLocation(**o)
                    elif o["address_type"] == AddressType.TRAINSTATION:
                        del o["address_type"]
                        locations[i] = TrainStation(**o)
                    elif o["address_type"] == AddressType.AIRPORT:
                        del o["address_type"]
                        locations[i] = Airport(iata_code=o["IATA"])
                    else:
                        raise InvalidSpatialInput(
                            f"unknown address type: '{o['address_type']}'"
                        )
                else:
                    print(
                        "No address type provided: ('address', 'trainstation' ,'airport'), assume address"
                    )
                    locations[i] = StructuredLocation(**o)
            elif isinstance(o, str):
                locations[i] = StructuredLocation(locality=o)
            else:
                raise InvalidSpatialInput(
                    f"start and destination must be either dict or string, not {type(o)}"
                )

        return DistanceRequest(
            transportation_mode=transportation_mode,
            start=locations[0],
            destination=locations[1],
        )

    except ValidationError as e:
        raise InvalidSpatialInput(e)


def get_distance(request: DistanceRequest) -> Kilometer:
    """Get the distance between start and destination

    Raises:
    - InvalidSpatialInput if start and stop are malformed or None
    :param request: Request for distance calculation between two locations for a given transportation mode
    :type request: DistanceRequest
    :return: Distance
    :rtype: Kilometer
    """

    # Calculate cords
    coords = []
    # StructuredLocation, TrainStation, Airport based on the object class of
    # start and destination in the request
    for loc in [request.start, request.destination]:
        if isinstance(loc, StructuredLocation):
            _, _, loc_coords, _ = geocoding_structured(loc.dict())
        elif isinstance(loc, TrainStation):
            _, _, loc_coords = geocoding_train_stations(loc.dict())
        elif isinstance(loc, Airport):
            _, loc_coords, _ = geocoding_airport(loc.iata_code)
        else:
            raise Exception("Address Type not valid")
        coords.append(loc_coords)

    # TODO: Do we want to calculate the distance for bicycles and pedelecs same like for cars?
    if request.transportation_mode in [
        TransportationMode.CAR,
        TransportationMode.MOTORBIKE,
        TransportationMode.PEDELEC,
        TransportationMode.BICYCLE,
    ]:
        return get_route(coords, RoutingProfile.CAR)

    elif request.transportation_mode in [
        TransportationMode.TRAIN,
        TransportationMode.TRAM,
        TransportationMode.BUS,
        TransportationMode.PLANE,
    ]:

        distance = 0
        # This could also be used for longer lists of cords (with via)
        for i in range(len(coords) - 1):
            # compute great circle distance between locations
            distance += haversine(
                coords[i][1], coords[i][0], coords[i + 1][1], coords[i + 1][0]
            )
        return _apply_detour(distance, request.transportation_mode)

    if request.transportation_mode == TransportationMode.FERRY:
        # hardcoding not ideal, profile should be determined based on specified "seating type"
        distance, distance_total = get_route_ferry(coords, profile=RoutingProfile.WALK)

        # if "seating" is "Car passenger", the remaining distance should be calculated as car trip ...
        # TODO: implement this
        # remaining_distance = distance - distance_total
        return distance
