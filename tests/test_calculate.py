#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test co2calculator.calculate"""

import os
from typing import Optional

import pytest

import co2calculator.calculate as candidate

script_path = os.path.dirname(os.path.realpath(__file__))


@pytest.mark.parametrize(
    "distance,stops,passengers,size,fuel_type,expected_emissions,expected_distance",
    [
        pytest.param(
            100,
            None,
            None,
            None,
            None,
            21.5,
            100,
            id="Distance-based w/ defaults",
        ),
        pytest.param(
            444,
            None,
            3,
            "medium",
            "gasoline",
            34.188,
            444,
            id="Distance-based w/ specs",
        ),
    ],
)
def test_calc_co2_car__distance_based(
    distance: Optional[float],
    stops: Optional[list],
    passengers: Optional[int],
    size: Optional[str],
    fuel_type: Optional[str],
    expected_emissions: float,
    expected_distance: float,
):
    """Test: Calculate emissions based on given distance.
    Expect: Returns emissions and distance.
    """
    actual_emissions, actual_distance = candidate.calc_co2_car(
        distance, stops, passengers, size, fuel_type
    )

    assert actual_emissions == expected_emissions
    assert actual_distance == expected_distance


@pytest.mark.skip(reason="Not implemented yet")
def test_calc_co2_car__stops_based():
    """Test: Calculate emissions based on given stops.
    Expect: Returns emissions and distance.
    """
    assert True


def test_co2_car__failed():
    """Test: Calling calc_co2_car with no arguments.
    Expect: Raises ValueError.
    """
    with pytest.raises(ValueError):
        candidate.calc_co2_car()


def test_heating_woodchips():
    """Test co2e calculation for heating: woodchips"""
    # Given parameters
    fuel_type = "woodchips"  # emission factor: 9322 kg/TJ
    consumption = 250
    unit = "kg"  # conversion factor to kWh = 5.4
    # divide by 277777.77777778 to convert from TJ to kWh
    co2e_kg_expected = 43.63

    # Calculate co2e
    co2e = candidate.calc_co2_heating(
        consumption=consumption, unit=unit, fuel_type=fuel_type
    )

    # Check if expected result matches calculated result
    assert co2e == pytest.approx(co2e_kg_expected, rel=0.01)


def test_electricity():
    """Test co2e calculation for electricity"""
    # Given parameters
    fuel_type = "german_energy_mix"
    consumption_kwh = 10000
    co2e_kg_expected = 3942.65  # emission factor: 109518 kg/TJ

    # Calculate co2e
    co2e = candidate.calc_co2_electricity(
        consumption=consumption_kwh, fuel_type=fuel_type
    )

    # Check if expected result matches calculated result
    assert co2e == pytest.approx(co2e_kg_expected, rel=0.01)


def test_bus_given_dist():
    """Test co2e calculation for a bus trip of given distance"""
    # Given parameters
    fuel_type = "diesel"
    distance_km = 549
    bus_size = "large"
    bus_range = "long-distance"
    occupancy = 80
    co2e_kg_expected = 12.30  # emission factor: 0.0224 kg/P.km

    # Calculate co2e
    co2e, _ = candidate.calc_co2_bus(
        size=bus_size,
        fuel_type=fuel_type,
        occupancy=occupancy,
        vehicle_range=bus_range,
        distance=distance_km,
    )

    # Check if expected result matches calculated result
    assert co2e == pytest.approx(co2e_kg_expected, rel=0.01)


def test_train_given_dist():
    """Test co2e calculation for a train trip of given distance"""
    # Given parameters
    fuel_type = "electric"
    distance_km = 1162
    train_range = "long-distance"
    co2e_kg_expected = 37.18  # assuming emission factor: 0.032 kg/P.km
    # (still has to be checked by expert though! only 0.00948 kg/P.km according to Öko-Institut)

    # Calculate co2e
    co2e, _ = candidate.calc_co2_train(
        fuel_type=fuel_type, vehicle_range=train_range, distance=distance_km
    )

    # Check if expected result matches calculated result
    assert co2e == pytest.approx(co2e_kg_expected, rel=0.01)


def test_business_trip_plane_wrong_input():
    """
    Test if an error if raised if a dictionary instead of a string is provided as start location when using
    plane as transport mode
    """
    start_loc = {"country": "DEU", "locality": "Frankfurt"}
    stop_loc = "AMS"

    # Check if raises error
    with pytest.raises(ValueError) as e:
        _, _, _, _ = calc_co2_businesstrip(
            transportation_mode="plane", start=start_loc, destination=stop_loc
        )
    assert e.type is ValueError


@pytest.mark.parametrize(
    "transportation_mode,weekly_distance,size,fuel_type,occupancy,passengers,expected",
    [pytest.param("car", 30, "medium", "gasoline", None, None, 6.93, id="Car commute")],
)
def test_commuting_car(
    transportation_mode: str,
    weekly_distance: float,
    size: str,
    fuel_type: str,
    occupancy: Optional[int],
    passengers: Optional[int],
    expected: float,
):
    """Test co2 calculation for commuting by car"""

    # Calculate co2 emissions
    co2e = candidate.calc_co2_commuting(
        transportation_mode=transportation_mode,
        weekly_distance=weekly_distance,
        size=size,
        fuel_type=fuel_type,
        occupancy=occupancy,
        passengers=passengers,
    )
    assert round(co2e, 2) == expected


def test_commuting_bike():
    """Test co2 calculation for commuting by bike"""
    # Given parameters
    mode = "bicycle"
    distance = 60
    co2e_kg_expected = 0.54
    # emission factor for bike: 0.009
    # 0.231 * 30 = 6.93

    # Calculate co2e
    co2e = candidate.calc_co2_commuting(
        transportation_mode=mode, weekly_distance=distance
    )

    # Check if expected result matches calculated result
    assert co2e == pytest.approx(co2e_kg_expected, rel=0.01)
