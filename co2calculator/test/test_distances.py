#!/usr/bin/env python
# -*- coding: utf-8 -*-

from co2calculator.distances import haversine
import math


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

    # Calculate co2e
    distance_expected = 1092
    distance = haversine(lat_a, long_a, lat_b, long_b)

    # Check if expected result matches calculated result
    assert math.isclose(distance, distance_expected, rel_tol=0.01)

