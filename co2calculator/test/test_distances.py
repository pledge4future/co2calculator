#!/usr/bin/env python
# -*- coding: utf-8 -*-

from co2calculator.distances import haversine, geocoding_airport, is_valid_geocoding_dict
from co2calculator.calculate import calc_co2_plane
import math
import numpy as np
import pytest


def test_haversine():
    """
    Test haversine function to calculate distance
    :return:
    """
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
    assert math.isclose(distance, distance_expected, rel_tol=0.01)


def test_geocoding_airport_FRA():
    """
        Test geocoding of airports using IATA code
    """
    # Given parameters
    iata = "FRA"  # Frankfurt Airport, Frankfurt a.M. (Germany)
    coords = [50.033056, 8.570556]

    # Retrieve coordinates
    name, res_coords, res_country = geocoding_airport(iata)

    # Check if expected coordinates match retrieved coordinates
    assert np.allclose(coords[::-1], res_coords, atol=0.03)


def test_geocoding_airport_JFK():
    """
        Test geocoding of airports using IATA code
    """
    # Given parameters
    iata = "JFK"  # John F. Kennedy International Airport, Queens, New York (USA)
    coords = [40.63975, -73.778925]

    # Retrieve coordinates
    name, res_coords, res_country = geocoding_airport(iata)

    # Check if expected coordinates match retrieved coordinates
    assert np.allclose(coords[::-1], res_coords, atol=0.03)


def test_geocoding_structured():
    pass


def test_valid_geocoding_dict():
    # Given parameters
    loc_dict = {"country": "DE",
                "region": "Baden-Württemberg",
                "county": "Rhein-Neckar-Kreis",
                "locality": "Heidelberg",
                "borough": "Rohrbach",
                "address": "Im Bosseldorn 25",
                "postalcode": "69126",
                "neighbourhood": None
                }

    # Check if raises error
    is_valid_geocoding_dict(loc_dict)


def test_invalid_geocoding_dict():
    # Given parameters
    loc_dict = {"country": "DE",
                "locality": "Heidelberg",
                "adress": "Im Bosseldorn 25",  # wrong spelling of "address"
                }

    # Check if raises error
    with pytest.raises(AssertionError) as e:
        is_valid_geocoding_dict(loc_dict)
    assert e.type is AssertionError


def test_plane():
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
    assert round(co2e, 2) == co2e_kg_expected


def test_plane_invalid_seating_class():
    # Given parameters
    start = "ZRH"
    dest = "FRA"
    seating = "second_class"  # this seating class does not exist

    # Check if raises error
    with pytest.raises(ValueError) as e:
        calc_co2_plane(start=start, destination=dest, seating_class=seating)
    assert e.type is ValueError


def test_plane_invalid_seating_range_combo():
    # Given parameters
    start = "ZRH"
    dest = "FRA"
    # flight between Frankfurt and Zurich is short-haul (<= 1500 km)
    seating = "premium_economy_class"
    # Premium economy class is not available for short-haul flights -> Error should be raised!

    # Check if raises error
    with pytest.raises(IndexError) as e:
        calc_co2_plane(start=start, destination=dest, seating_class=seating)
    assert e.type is IndexError
