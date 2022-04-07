#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Functions for obtaining the distance between given addresses."""


from typing import Tuple, Union, Optional
import enum
from pathlib import Path
from dotenv import load_dotenv
import os
import warnings


import numpy as np
import pandas as pd
import openrouteservice
from openrouteservice.directions import directions
from openrouteservice.geocode import pelias_search, pelias_structured
from thefuzz import fuzz
from thefuzz import process
from pydantic import BaseModel


from ._types import Kilometer


load_dotenv()  # take environment variables from .env.

# Load environment vars (TODO: Use pydantic.BaseSettings)
ORS_API_KEY = os.environ.get("ORS_API_KEY")

# Set (module) global vars (TODO: Don't do it - make it a class and move it to attributes!)
script_path = str(Path(__file__).parent)
detour_df = pd.read_csv(f"{script_path}/../data/detour.csv")

# Module's models
@enum.unique
class TransportationMode(enum.Enum):
    CAR = enum.auto()
    MOTORBIKE = enum.auto()
    BUS = enum.auto()
    TRAIN = enum.auto()
    PLANE = enum.auto()
    FERRY = enum.auto()


class StructuredLocation(BaseModel):
    address: Optional[str]
    locality: str
    country: str


class TrainStation(BaseModel):
    station_name: str
    country: str  # NOTE: Could be improved with validator to country codes


class DistanceRequest(BaseModel):
    transportation_mode: TransportationMode
    start: Union[StructuredLocation, TrainStation]
    destination: Union[StructuredLocation, TrainStation]


IataCode = str  # NOTE: Could be improved with validation of IATA codes


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
    :return: Distance in km
    :rtype: float
    """
    # convert angles from degree to radians
    lat_start, long_start, lat_dest, long_dest = np.deg2rad(
        [lat_start, long_start, lat_dest, long_dest]
    )
    # compute zeta
    a = (
        np.sin((lat_dest - lat_start) / 2) ** 2
        + np.cos(lat_start)
        * np.cos(lat_dest)
        * np.sin((long_dest - long_start) / 2) ** 2
    )
    c = 2 * np.arcsin(np.sqrt(a))
    r = 6371

    return c * r


def geocoding_airport(iata: str) -> Tuple[str, Tuple[float, float], str]:
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

    # TODO: Replace loc_dict with pydantic.BaseModel approach
    is_valid_geocoding_dict(loc_dict)

    call = pelias_structured(clnt, **loc_dict)
    n_results = len(call["features"])
    res = call["features"]
    print(res)
    assert n_results != 0, "No places found with these search parameters"
    if n_results == 0:
        raise Exception("No places found with these search parameters")

    # TODO: Validate respone with a pydantic.BaseModel (`PeliasStructuredResponse`)
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
    stations_df = pd.read_csv(
        f"{script_path}/../data/stations/stations.csv",
        sep=";",
        low_memory=False,
        usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
    )
    # remove stations with no coordinates
    stations_df.dropna(subset=["latitude", "longitude"], inplace=True)
    countries_eu = stations_df["country"].unique()
    if "country" in loc_dict:
        country_code = loc_dict["country"]
        if country_code not in countries_eu:
            warnings.warn(
                "The provided country is not within Europe. "
                "Please provide the address of the station instead of the station name for accurate results."
            )
    else:
        raise ValueError("No 'country' provided. Cannot search for train station")
    if "station_name" in loc_dict:
        station_name = loc_dict["station_name"]
    else:
        raise ValueError("No 'station_name' provided. Cannot search for train station.")

    # filter stations by country
    stations_in_country_df = stations_df[stations_df["country"] == country_code]

    # use thefuzz to find best match
    choices = stations_in_country_df["slug"].values
    res_station_slug, score = process.extractOne(
        station_name, choices, scorer=fuzz.partial_ratio
    )
    res_station = stations_in_country_df[
        stations_in_country_df["slug"] == res_station_slug
    ]
    res_country, res_station_name = res_station[["country", "name"]].values[0]

    coords = (res_station.iloc[0]["latitude"], res_station.iloc[0]["longitude"])

    return res_station_name, res_country, coords


def is_valid_geocoding_dict(geocoding_dict):
    """Function to check if the dictionary is valid as input for pelias structured geocoding. Raises error if it is not
    the case

    :param geocoding_dict: dictionary describing the location
    """
    allowed_keys = [
        "country",
        "region",
        "county",
        "locality",
        "borough",
        "address",
        "postalcode",
        "neighbourhood",
    ]
    assert len(geocoding_dict) != 0, "Error! Empty dictionary provided."
    for key in geocoding_dict:
        assert (
            key in allowed_keys
        ), f"Error! Parameter {key} is not available. Please check the input data."
    # warnings
    if "country" not in geocoding_dict.keys():
        warnings.warn("Country was not provided. The results may be wrong.")
    if "locality" not in geocoding_dict.keys():
        warnings.warn(
            "Locality (city) was not provided. The results may be inaccurate."
        )


def get_route(coords, profile: str = None) -> Kilometer:
    """Obtain the distance of a route between given waypoints using a given profile

    :param coords: list of [lat,long] coordinates
    :param profile: driving-car, cycling-regular
    :return: distance of the route
    """
    # coords: list of [lat,long] lists
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
    :type distance: float
    :type transportation_mode: str
    :return: Distance accounted for detour
    :rtype: float
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
        Using detour_coefficient = {detour_coefficient} and detour_constant = {detour_constant}.
        """
        )
    distance_with_detour = detour_coefficient * distance + detour_constant

    return distance_with_detour


def get_distance(start, destination, transportation_mode):
    """Get the distance between start and destination

    Raises:
    - InvalidSpatialInput if start and stop are malformed or None
    """

    # TODO: Refactor to meet DRY

    if None in [start, destination]:
        raise InvalidSpatialInput("neither distance or start/destination  provided")

    if transportation_mode == "car":
        # Stops are formatted like:
        # [
        #   {
        #     "address": "Im Neuenheimer Feld 348",
        #     "locality": "Heidelberg",
        #     "country": "Germany"
        #   },
        #   {
        #     "country": "Germany",
        #     "locality": "Berlin",
        #     "address": "Alexanderplatz 1"
        #   }
        # ]
        # TODO: Validate with BaseModel

        coords = []
        for loc in [start, destination]:
            _, _, loc_coords, _ = geocoding_structured(loc)
            coords.append(loc_coords)
        return get_route(coords, "driving-car")

    if transportation_mode == "motorbike":
        # Same model as car!
        # [
        #     {"address": "Im Neuenheimer Feld 348", "locality": "Heidelberg", "country": "Germany"},
        #     {"country": "Germany", "locality": "Berlin", "address": "Alexanderplatz 1"}
        # ]
        coords = []
        for loc in [start, destination]:
            _, _, loc_coords, _ = geocoding_structured(loc)
            coords.append(loc_coords)
        distance = get_route(coords, "driving-car")

    if transportation_mode == "bus":
        # Same as car (StructuredLocation)
        # TODO: Validate with BaseModel
        # TODO: Question: Why are we not calculating the bus trip like `driving-car` routes?

        distance = 0
        coords = []
        for loc in [start, destination]:
            _, _, loc_coords, _ = geocoding_structured(loc)
            coords.append(loc_coords)
        for i in range(0, len(coords) - 1):
            distance += haversine(
                coords[i][1], coords[i][0], coords[i + 1][1], coords[i + 1][0]
            )
        return _apply_detour(distance, transportation_mode)

    if transportation_mode == "train":
        # Stops for train distance calculations are formed like this:
        # [
        #     {"station_name": "Heidelberg Hbf", "country": "DE"},
        #     {"station_name": "Berlin Hauptbahnhof", "country": "DE"}
        # ]
        # TODO: Validate with BaseModel

        distance = 0
        coords = []

        for loc in [start, destination]:
            try:
                _, _, loc_coords = geocoding_train_stations(loc)
            except RuntimeWarning:
                _, _, loc_coords, _ = geocoding_structured(loc)
            except ValueError:
                _, _, loc_coords, _ = geocoding_structured(loc)
            coords.append(loc_coords)

        for i in range(len(coords) - 1):
            # compute great circle distance between locations
            distance += haversine(
                coords[i][1], coords[i][0], coords[i + 1][1], coords[i + 1][0]
            )
        return _apply_detour(distance, transportation_mode)

    if transportation_mode == "plane":
        # Stops are IATA code of airports
        # TODO: Validate stops with BaseModel

        _, geom_start, _ = geocoding_airport(start)
        _, geom_dest, _ = geocoding_airport(destination)

        distance = haversine(geom_start[1], geom_start[0], geom_dest[1], geom_dest[0])
        return _apply_detour(distance, transportation_mode)

    if transportation_mode == "ferry":
        # Stops are formatted like {"locality":<city>, "county":<country>}
        # TODO: Validate stops with BaseModel

        _, _, geom_start, _ = geocoding_structured(start)
        _, _, geom_dest, _ = geocoding_structured(destination)
        # compute great circle distance between airports
        distance = haversine(geom_start[1], geom_start[0], geom_dest[1], geom_dest[0])

        return _apply_detour(distance, transportation_mode)
