#!/usr/bin/env python
# -*- coding: utf-8 -*-

from co2calculator.distances import haversine, geocoding_airport
import math
import numpy as np


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
