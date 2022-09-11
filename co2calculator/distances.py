#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Functions for obtaining the distance between given addresses."""

import os
import warnings
from pathlib import Path
from typing import Tuple, Union, Optional

import numpy as np
import openrouteservice
import pandas as pd
from dotenv import load_dotenv
from openrouteservice.directions import directions
from openrouteservice.geocode import pelias_search, pelias_structured
from pydantic import BaseModel, ValidationError, Extra, confloat
from thefuzz import fuzz
from thefuzz import process

from ._types import Kilometer
from .constants import (
    TransportationMode,
    CountryCode2,
    CountryCode3,
    CountryName,
    IataAirportCode,
    DF_AIRPORTS,
)

load_dotenv()  # take environment variables from .env.

# Load environment vars (TODO: Use pydantic.BaseSettings)
ORS_API_KEY = os.environ.get("ORS_API_KEY")

# Set (module) global vars (TODO: Don't do it - make it a class and move it to attributes!)
script_path = str(Path(__file__).parent)
detour_df = pd.read_csv(f"{script_path}/../data/detour.csv")


class StructuredLocation(BaseModel, extra=Extra.forbid):
    address: Optional[str]
    locality: str
    country: Union[CountryCode2, CountryCode3, CountryName]
    region: Optional[str]
    county: Optional[str]
    borough: Optional[str]
    postalcode: Optional[str]
    neighbourhood: Optional[str]


class TrainStation(BaseModel):
    station_name: str
    country: CountryCode2


class Airport(BaseModel):
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


def geocoding_airport_pelias(iata: str) -> Tuple[str, Tuple[float, float], str]:
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


def geocoding_airport(iata) -> Tuple[str, Tuple[float, float], str]:
    """Function to obtain the coordinates of an airport by the IATA code

    :param iata: IATA airport code
    :type iata: str
    :return: name, coordinates and country of the found airport
    :rtype: Tuple[str, Tuple[float, float], str]
    """

    airport = Airport(iata_code=iata)
    name, lat, lon, country = (
        DF_AIRPORTS[DF_AIRPORTS.iata_code == airport.iata_code][
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
                print(
                    f"Data type not matching search ({layer} instead of address or locality. Skipping {name}, {coords}"
                )
                continue
        confidence = feature["properties"]["confidence"]
        if confidence < 0.8:
            warnings.warn(
                f"Low confidence: {confidence:.1f} for result {name}, {coords}"
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
    station = TrainStation(**loc_dict)

    stations_df = pd.read_csv(
        f"{script_path}/../data/stations/stations.csv",
        sep=";",
        low_memory=False,
        usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
    )
    # remove stations with no coordinates
    stations_df.dropna(subset=["latitude", "longitude"], inplace=True)
    countries_eu = stations_df["country"].unique()
    country_code = station.country
    if country_code not in countries_eu:
        warnings.warn(
            "The provided country is not within Europe. "
            "Please provide the address of the station instead of the station name for accurate results."
        )

    # filter stations by country
    stations_in_country_df = stations_df[stations_df["country"] == country_code]

    # use thefuzz to find best match
    choices = stations_in_country_df["slug"].values
    res_station_slug, score = process.extractOne(
        station.station_name, choices, scorer=fuzz.partial_ratio
    )
    res_station = stations_in_country_df[
        stations_in_country_df["slug"] == res_station_slug
    ]
    res_country, res_station_name = res_station[["country", "name"]].values[0]

    coords = (res_station.iloc[0]["latitude"], res_station.iloc[0]["longitude"])

    return res_station_name, res_country, coords


def get_route(coords: list, profile: str = None) -> Kilometer:
    """Obtain the distance of a route between given waypoints using a given profile
    todo: check if coords may also be a tuple/array etc.

    :param list coords: list of [lat,long] coordinates
    :param str profile: driving-car, cycling-regular
    :return: distance of the route
    :rtype: Kilometer
    """
    # profile may be: driving-car, cycling-regular
    clnt = openrouteservice.Client(key=ORS_API_KEY)

    allowed_profiles = ["driving-car", "cycling-regular"]
    if profile not in allowed_profiles or profile is None:
        profile = "driving-car"
        warnings.warn(
            f"Warning! Specified profile not available or no profile passed.\n"
            f"Profile set to '{profile}' by default."
        )
    route = directions(clnt, coords, profile=profile)
    dist = (
        route["routes"][0]["summary"]["distance"] / 1000
    )  # divide my 1000, as we're working with distances in km

    return dist


def _apply_detour(distance: Kilometer, transportation_mode: str) -> Kilometer:
    """
    Function to apply specific detour parameters to a distance as the crow flies
    :param distance: Distance as the crow flies between location of departure and destination of a trip
    :param transportation_mode: Mode of transport used in the trip
    :type distance: Kilometer
    :type transportation_mode: str
    :return: Distance accounted for detour
    :rtype: Kilometer
    """
    try:
        detour_coefficient = detour_df[
            detour_df["transportation_mode"] == transportation_mode
        ]["coefficient"].values[0]
        detour_constant = detour_df[
            detour_df["transportation_mode"] == transportation_mode
        ]["constant [km]"].values[0]
    except KeyError:
        detour_coefficient = 1.0
        detour_constant = 0.0
        warnings.warn(
            f"""
        No detour coefficient or constant available for this transportation mode.
        Detour parameters are available for the following transportation modes:
        {detour_df["transportation_mode"]}
        Using detour_coefficient = {detour_coefficient} and detour_constant = {detour_constant}.
        """
        )
    distance_with_detour = detour_coefficient * distance + detour_constant

    return distance_with_detour


def create_distance_request(
    start: Union[str, dict],
    destination: Union[str, dict],
    transportation_mode: TransportationMode,
) -> DistanceRequest:
    """Transform and validate the user input into a proper model for distance calculations

    Raises:
        - InvalidSpatialInput for validation error
        - InvalidSpatialInput for unknown transportation_mode
    """

    # Validate the spatial data wrt. the mode of transportation
    # NOTE: Since `start` and `destination` are different depending on the `transportation_mode`,
    # we map the respective models to the mode of transportation.
    # NOTE: Eventually the user of co2calculator should use the models right away (improve their
    # structure in that iteration too!).

    try:
        if transportation_mode in [
            TransportationMode.CAR,
            TransportationMode.MOTORBIKE,
            TransportationMode.BUS,
            TransportationMode.FERRY,
        ]:
            return DistanceRequest(
                transportation_mode=transportation_mode,
                start=StructuredLocation(**start),
                destination=StructuredLocation(**destination),
            )

        if transportation_mode in [TransportationMode.TRAIN]:
            return DistanceRequest(
                transportation_mode=transportation_mode,
                start=TrainStation(**start),
                destination=TrainStation(**destination),
            )

        if transportation_mode in [TransportationMode.PLANE]:
            return DistanceRequest(
                transportation_mode=transportation_mode,
                start=Airport(iata_code=start),
                destination=Airport(iata_code=destination),
            )

    except ValidationError as e:
        raise InvalidSpatialInput(e)

    raise InvalidSpatialInput(f"unknown transportation_mode: '{transportation_mode}'")


def get_distance(request: DistanceRequest) -> Kilometer:
    """Get the distance between start and destination

    Raises:
    - InvalidSpatialInput if start and stop are malformed or None
    :param request: Request for distance calculation between two locations for a given transportation mode
    :type request: DistanceRequest
    :return: Distance
    :rtype: Kilometer
    """

    detour_map = {
        TransportationMode.CAR: False,
        TransportationMode.MOTORBIKE: False,
        TransportationMode.BUS: True,
        TransportationMode.TRAIN: True,
        TransportationMode.PLANE: True,
        TransportationMode.FERRY: True,
    }

    if request.transportation_mode in [
        TransportationMode.CAR,
        TransportationMode.MOTORBIKE,
    ]:
        coords = []
        for loc in [request.start, request.destination]:
            _, _, loc_coords, _ = geocoding_structured(loc.dict())
            coords.append(loc_coords)
        return get_route(coords, "driving-car")

    if request.transportation_mode == TransportationMode.BUS:
        # Same as car (StructuredLocation)
        # TODO: Validate with BaseModel
        # TODO: Question: Why are we not calculating the bus trip like `driving-car` routes?

        distance = 0
        coords = []
        for loc in [request.start, request.destination]:
            _, _, loc_coords, _ = geocoding_structured(loc.dict())
            coords.append(loc_coords)
        for i in range(0, len(coords) - 1):
            distance += haversine(
                coords[i][1], coords[i][0], coords[i + 1][1], coords[i + 1][0]
            )
        return _apply_detour(distance, request.transportation_mode)

    if request.transportation_mode == TransportationMode.TRAIN:

        distance = 0
        coords = []

        for loc in [request.start, request.destination]:
            try:
                _, _, loc_coords = geocoding_train_stations(loc.dict())
            except RuntimeWarning:
                _, _, loc_coords, _ = geocoding_structured(loc.dict())
            except ValueError:
                _, _, loc_coords, _ = geocoding_structured(loc.dict())
            coords.append(loc_coords)

        for i in range(len(coords) - 1):
            # compute great circle distance between locations
            distance += haversine(
                coords[i][1], coords[i][0], coords[i + 1][1], coords[i + 1][0]
            )
        return _apply_detour(distance, request.transportation_mode)

    if request.transportation_mode == TransportationMode.PLANE:
        # Stops are IATA code of airports
        # TODO: Validate stops with BaseModel

        _, geom_start, _ = geocoding_airport(request.start.iata_code)
        _, geom_dest, _ = geocoding_airport(request.destination.iata_code)

        distance = haversine(geom_start[1], geom_start[0], geom_dest[1], geom_dest[0])
        return _apply_detour(distance, request.transportation_mode)

    if request.transportation_mode == TransportationMode.FERRY:
        # todo: Do we have a way of checking if there even exists a ferry connection between the given cities (or if the
        #  cities even have a port?
        _, _, geom_start, _ = geocoding_structured(request.start.dict())
        _, _, geom_dest, _ = geocoding_structured(request.destination.dict())
        # compute great circle distance between airports
        distance = haversine(geom_start[1], geom_start[0], geom_dest[1], geom_dest[0])

        return _apply_detour(distance, request.transportation_mode)
