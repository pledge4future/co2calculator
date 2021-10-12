#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test co2e calculations
"""

import os

from co2calculator import *

script_path = os.path.dirname(os.path.realpath(__file__))


def test_heating_woodchips():
    """
    Test co2e calculation for heating: woodchips
    :return:
    """
    # Given parameters
    fuel_type = "woodchips"  # emission factor: 9322 kg/TJ
    consumption = 250
    unit = "kg"  # conversion factor to kWh = 5.4
    # divide by 277777.77777778 to convert from TJ to kWh
    co2e_kg_expected = 43.63

    # Calculate co2e
    co2e = calc_co2_heating(consumption=consumption, unit=unit, fuel_type=fuel_type)

    # Check if expected result matches calculated result
    assert round(co2e, 2) == co2e_kg_expected


def test_electricity():
    """
    Test co2e calculation for electricity
    :return:
    """
    # Given parameters
    fuel_type = "german_energy_mix"
    consumption_kwh = 10000
    co2e_kg_expected = 3942.65  # emission factor: 109518 kg/TJ

    # Calculate co2e
    co2e = calc_co2_electricity(consumption=consumption_kwh, fuel_type=fuel_type)

    # Check if expected result matches calculated result
    assert round(co2e, 2) == co2e_kg_expected


def test_bus_given_dist():
    """
    Test co2e calculation for a bus trip of given distance
    :return:
    """
    # Given parameters
    fuel_type = "diesel"
    distance_km = 549
    bus_size = "large"
    bus_range = "long-distance"
    occupancy = 80
    co2e_kg_expected = 12.30  # emission factor: 0.0224 kg/P.km

    # Calculate co2e
    co2e, _ = calc_co2_bus(size=bus_size, fuel_type=fuel_type, occupancy=occupancy, vehicle_range=bus_range,
                        distance=distance_km)

    # Check if expected result matches calculated result
    assert round(co2e, 2) == co2e_kg_expected


def test_car_given_dist():
    """
    Test co2e calculation for a car trip of given distance
    :return:
    """
    # Given parameters
    fuel_type = "gasoline"
    distance_km = 444
    car_size = "medium"
    passengers = 3
    co2e_kg_expected = 34.19  # emission factor: 0.231 kg/P.km

    # Calculate co2e
    co2e, _ = calc_co2_car(passengers, size=car_size, fuel_type=fuel_type, distance=distance_km)

    # Check if expected result matches calculated result
    assert round(co2e, 2) == co2e_kg_expected


def test_train_given_dist():
    """
    Test co2e calculation for a train trip of given distance
    :return:
    """
    # Given parameters
    fuel_type = "electric"
    distance_km = 1162
    train_range = "long-distance"
    co2e_kg_expected = 37.18  # assuming emission factor: 0.032 kg/P.km
    # (still has to be checked by expert though! only 0.00948 kg/P.km according to Öko-Institut)

    # Calculate co2e
    co2e, _ = calc_co2_train(fuel_type=fuel_type, vehicle_range=train_range, distance=distance_km)

    # Check if expected result matches calculated result
    assert round(co2e, 2) == co2e_kg_expected


def test_commuting_car():
    """
    Test co2 calculation for commuting by car
    :return:
    """
    # Given parameters
    mode = "car"
    distance = 30
    passengers = 1
    car_size = "medium"
    fuel_type = "gasoline"
    co2e_kg_expected = 6.93
    # emission factor for car, medium, gasoline: 0.231
    # 0.231 * 30 = 6.93

    # Calculate co2e
    co2e = calc_co2_commuting(transportation_mode=mode,
                              weekly_distance=distance,
                              passengers=passengers,
                              size=car_size,
                              fuel_type=fuel_type)

    # Check if expected result matches calculated result
    assert round(co2e, 2) == co2e_kg_expected
