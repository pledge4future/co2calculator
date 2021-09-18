#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Functions for obtaining the distance between given addresses.
"""

import numpy as np
import openrouteservice
from openrouteservice.directions import directions
from openrouteservice.geocode import pelias_search, pelias_autocomplete, pelias_structured
import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

ors_api_key = os.getenv('ORS_API_KEY')
script_path = os.path.dirname(os.path.realpath(__file__))


def haversine(lat_start, long_start, lat_dest, long_dest):
    """
    Function to compute the distance as the crown flies between given locations
    :param lat_start: latitude of Start
    :param long_start: Longitude of Start
    :param lat_dest: Latitude of Destination
    :param long_dest: Longitude of Destination
    :return: Distance in km
    """
    # convert angles from degree to radians
    lat_start, long_start, lat_dest, long_dest = np.deg2rad([lat_start, long_start, lat_dest, long_dest])
    # compute zeta
    a = np.sin((lat_dest - lat_start) / 2) ** 2 + np.cos(lat_start) * np.cos(lat_dest) * np.sin(
        (long_dest - long_start) / 2) ** 2
    c = 2 * np.arcsin(np.sqrt(a))
    r = 6371

    return c * r  # distance in km


def geocoding_airport(iata):
    """
    Function to obtain the coordinates of an airport by the IATA code
    :param iata: IATA airport code
    :return: name, coordinates and country of the found airport
    """
    clnt = openrouteservice.Client(key=ors_api_key)

    call = pelias_search(clnt, "%s Airport" % iata)

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
            if (feature["properties"]["confidence"] == 1) & (feature["properties"]["match_type"] == "exact"):
                name = feature["properties"]["name"]
                geom = feature["geometry"]["coordinates"]
                country = feature["properties"]["country_a"]
                break

    return name, geom, country


def geocoding(address):
    """
    Function to obtain coordinates for a given address
    :param address: Location/Address to be searched
            user should give address in the form:
            <adress>, <locality>, <country>
            e.g. Hauptbahnhof, Heidelberg, Germany
            e.g. Im Neuenheimer Feld 348, Heidelberg, Germany
            e.g. Heidelberg, Germany
    :return: Name, country and coordinates of the found location
    """

    clnt = openrouteservice.Client(key=ors_api_key)

    call = pelias_search(clnt, address)
    for feature in call["features"]:
        name = feature["properties"]["name"]
        country = feature["properties"]["country"]
        coords = feature["geometry"]["coordinates"]
        break

    return name, country, coords


def geocoding_structured(loc_dict):
    """
    Function to obtain coordinates for a given address
    :param loc_dict: dictionary describing the location. The dictionary kan have the keys:
        country: highest-level administrative divisions supported in a search.
                    Full country name or two-/three-letter abbreviations supported
                    e.g., Germany / "DE" / "DEU"
        region: first-level administrative divisions within countries, analogous to states and provinces
                    in the US and Canada
                    e.g., Delaware, Ontario, Ardennes, Baden-Württemberg
        county: administrative divisions between localities and regions
                    e.g., Alb-Donau-Kreis
        locality: equivalent to what are commonly referred to as cities
                    e.g., Bangkok, Caracas
        borough: mostly known in the context of NY, may exist in other cities like Mexico City
                    e.g. Manhatten in NY
                        Iztapalapa in Mexico City
        postalcode: postal code; !! Not working in many countries !!
        address: street name, optionally also house number
        neighbourhood: vernacular geographic entities that may not necessarily be official administrative
                        divisions but are important nonetheless
                    e.g. Notting Hill in London
                    Le Marais in Paris
    :return: Name, country and coordinates of the found location
    """

    clnt = openrouteservice.Client(key=ors_api_key)

    #call = pelias_structured(clnt, country=country, region=region, county=county, locality=locality, borough=borough,
    #                         postalcode=postalcode, address=address, neighbourhood=neighbourhood)
    call = pelias_structured(clnt, **loc_dict)
    n_results = len(call["features"])
    res = call["features"]
    print(res)
    if n_results == 0:
        raise Exception("No places found with these search parameters")

    for feature in res:
        name = feature["properties"]["name"]
        country = feature["properties"]["country"]
        coords = feature["geometry"]["coordinates"]
        layer = feature["properties"]["layer"]
        if loc_dict["locality"] is not None and loc_dict["address"] is not None:
            if layer != "address" or layer != "locality" and n_results > 1:
                print("Data type not matching search (%s instead of address or locality. Skipping %s, %s" % (layer, name, coords))
                continue
        confidence = feature["properties"]["confidence"]
        if confidence < 0.8 and n_results > 1:
            print("Low confidence: %.1f. Skipping %s, %s" % (confidence, name, coords))
            continue
        break
    print("%i location(s) found. Using this result: %s, %s (data type: %s)" % (n_results, name, country, layer))
    print("Coords: ", coords)

    return name, country, coords, res


def get_route(coords, profile=None):
    """
    Obtain the distance of a route between given waypoints using a given profile
    :param coords: list of [lat,long] coordinate-lists
    :param profile: driving-car, cycling-regular
    :return: distance of the route
    """
    # coords: list of [lat,long] lists
    # profile may be: driving-car, cycling-regular
    clnt = openrouteservice.Client(key=ors_api_key)

    allowed_profiles = ["driving-car", "cycling-regular"]
    if profile not in allowed_profiles or profile is None:
        print("Warning! Specified profile not available or no profile passed.\n"
              "Profile set to 'driving-car' by default.")
        profile = "driving-car"
    route = directions(clnt, coords, profile=profile)
    dist = route["routes"][0]["summary"]["distance"]

    return dist
