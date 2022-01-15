#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for distance computation"""

"""Python tests"""

import os
from pathlib import Path
from co2calculator.distances import (
    haversine,
    geocoding_airport,
    is_valid_geocoding_dict,
    geocoding_train_stations,
)
from co2calculator.calculate import calc_co2_plane, calc_co2_train
import math
import numpy as np
import pytest
from dotenv import load_dotenv

load_dotenv()
ORS_API_KEY = os.environ.get("ORS_API_KEY")
script_path = str(Path(__file__).parent.parent)


def test_haversine():
    """Test haversine function to calculate distance"""
    # Given parameters
    # a: Frankfurt airport (FRA)
    lat_a = 50.0264
    long_a = 8.5431
    # b: Barcelona airport (BCN)
    lat_b = 41.2971
    long_b = 2.07846

    # Calculate distance
    distance_expected = 1092
    distance = haversine(lat_a, long_a, lat_b, long_b)

    # Check if expected result matches calculated result
    assert distance == pytest.approx(distance_expected, rel=0.01)


def test_geocoding_airport_FRA():
    """Test geocoding of airports using IATA code"""
    if ORS_API_KEY is None:
        pytest.skip("Skipping this test because no file '.env' was found.")
    # Given parameters
    iata = "FRA"  # Frankfurt Airport, Frankfurt a.M. (Germany)
    coords = [50.033056, 8.570556]

    # Retrieve coordinates
    name, res_coords, res_country = geocoding_airport(iata)

    # Check if expected coordinates match retrieved coordinates
    assert np.allclose(coords[::-1], res_coords, atol=0.03)


def test_geocoding_airport_JFK():
    """Test geocoding of airports using IATA code"""
    if ORS_API_KEY is None:
        pytest.skip("Skipping this test because no file '.env' was found.")
    # Given parameters
    iata = "JFK"  # John F. Kennedy International Airport, Queens, New York (USA)
    coords = [40.63975, -73.778925]

    # Retrieve coordinates
    name, res_coords, res_country = geocoding_airport(iata)

    # Check if expected coordinates match retrieved coordinates
    assert np.allclose(coords[::-1], res_coords, atol=0.03)


def test_geocoding_structured():
    """To do"""
    pass


def test_valid_geocoding_dict():
    """Test if a valid geocoding dictionary is recognized as valid"""
    # Given parameters
    loc_dict = {
        "country": "DE",
        "region": "Baden-Württemberg",
        "county": "Rhein-Neckar-Kreis",
        "locality": "Heidelberg",
        "borough": "Rohrbach",
        "address": "Im Bosseldorn 25",
        "postalcode": "69126",
        "neighbourhood": None,
    }

    # Call function; test will pass if no error is raised
    is_valid_geocoding_dict(loc_dict)


def test_invalid_geocoding_dict():
    """Test if a providing an invalid geocoding raises an error"""
    # Given parameters
    loc_dict = {
        "country": "DE",
        "locality": "Heidelberg",
        "adress": "Im Bosseldorn 25",  # wrong spelling of "address"
    }

    # Check if raises error
    with pytest.raises(AssertionError) as e:
        is_valid_geocoding_dict(loc_dict)
    assert e.type is AssertionError


def test_plane():
    """Test calculation of CO2 emissions of flights"""
    if ORS_API_KEY is None:
        pytest.skip("Skipping this test because no file '.env' was found.")
    # Given parameters
    start = "MUC"
    dest = "DME"
    seating = "business_class"
    # distance between "MUC" "DME": 1943.5387
    # add detour coefficient (95 km): 2038.5387 --> range class: long-haul
    # emission factor for business class and long-haul: 0.42385
    # 2038.5387 * 0.42385 = 864.0346
    co2e_kg_expected = 864.03

    # Calculate co2e
    co2e, dist = calc_co2_plane(start=start, destination=dest, seating_class=seating)
    # Check if expected result matches calculated result
    assert co2e == pytest.approx(co2e_kg_expected, 0.01)


def test_plane_invalid_seating_class():
    """Test if calculation of CO2 emissions for flights raises an error if an invalid seating class if provided"""
    # Given parameters
    start = "ZRH"
    dest = "FRA"
    seating = "second_class"  # this seating class does not exist

    # Check if raises error
    with pytest.raises(ValueError) as e:
        calc_co2_plane(start=start, destination=dest, seating_class=seating)
    assert e.type is ValueError


def test_plane_invalid_seating_range_combo():
    """
    Test if calculation of CO2 emissions for flights raises an error if the query results in an invalid combination
    of range and seating class
    """
    if ORS_API_KEY is None:
        pytest.skip("Skipping this test because no file '.env' was found.")
    # Given parameters
    start = "ZRH"
    dest = "FRA"
    # flight between Frankfurt and Zurich is short-haul (<= 1500 km)
    seating = "premium_economy_class"
    # Premium economy class is not available for short-haul flights -> Error should be raised!

    # Check if raises warning
    with pytest.warns(
        UserWarning, match=r"Seating class '\w+' not available for short-haul flights"
    ):
        calc_co2_plane(start=start, destination=dest, seating_class=seating)


def test_geocoding_train_stations_invalid():
    """Test geocoding of train stations if dictionary with invalid parameters is provided"""
    if ORS_API_KEY is None:
        pytest.skip("Skipping this test because no file '.env' was found.")
    # Given parameters
    station_dict = {
        "country": "DE",
        "address": "Heidelberg Hbf",
    }  # invalid parameters; has to be specified as "station_name"

    # Check if raises error
    with pytest.raises(ValueError) as e:
        geocoding_train_stations(station_dict)
    assert e.type is ValueError


def test_geocoding_train_stations_outside_europe():
    """Test geocoding of train stations outside of europe"""
    if ORS_API_KEY is None:
        pytest.skip("Skipping this test because no file '.env' was found.")
    # Given parameters
    stops = [
        {"country": "CHN", "address": "385 Meiyuan Rd", "locality": "Shanghai"},
        {"country": "CHN", "region": "Beijing", "address": "Beijing Station"},
    ]
    coords = [[121.450446, 31.251552], [116.42792, 39.902896]]
    fuel_type = "electric"
    vehicle_range = "long-distance"
    emission_factor = 0.032
    # emission factor for electric long distance trains: 0.032

    distance = haversine(coords[0][1], coords[0][0], coords[1][1], coords[1][0]) * 1.2
    co2e_kg_expected = distance * emission_factor

    # Calculate co2e
    co2e, dist = calc_co2_train(
        fuel_type=fuel_type, vehicle_range=vehicle_range, stops=stops
    )

    # Check if expected result matches calculated result
    assert co2e == pytest.approx(co2e_kg_expected, abs=0.1)
