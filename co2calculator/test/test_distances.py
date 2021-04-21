#!/usr/bin/env python
# -*- coding: utf-8 -*-

from co2calculator.distances import haversine
import math


def test_haversine():
    # a: Frankfurt airport (FRA)
    lat_a = 50.0264
    long_a = 8.5431
    # b: Barcelona airport (BCN)
    lat_b = 41.2971
    long_b = 2.07846
    expected_value = haversine(lat_a, long_a, lat_b, long_b)
    actual_value = 1092
    print(expected_value)
    assert math.isclose(actual_value, expected_value, rel_tol=0.01)

