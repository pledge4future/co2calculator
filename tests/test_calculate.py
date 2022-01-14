#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test co2calculator.calculate"""

import os
from typing import Optional
from attr.validators import optional

import pytest

import co2calculator.calculate as candidate

script_path = os.path.dirname(os.path.realpath(__file__))


@pytest.mark.parametrize(
    "distance,passengers,size,fuel_type,expected_emissions",
    [
        pytest.param(
            100,
            None,
            None,
            None,
            21.5,
            id="w/ defaults",
        ),
        pytest.param(
            444,
            3,
            "medium",
            "gasoline",
            34.188,
            id="w/ specs",
        ),
    ],
)
def test_calc_co2_car__distance_based(
    distance: float,
    passengers: Optional[int],
    size: Optional[str],
    fuel_type: Optional[str],
    expected_emissions: float,
):
    """Test: Calculate car-trip emissions based on given distance.
    Expect: Returns emissions and distance.
    """
    actual_emissions, actual_distance = candidate.calc_co2_car(
        distance=distance,
        stops=None,
        passengers=passengers,
        size=size,
        fuel_type=fuel_type,
    )

    assert actual_emissions == expected_emissions
    assert actual_distance == distance


@pytest.mark.skip(reason="Not implemented yet")
def test_calc_co2_car__stops_based():
    """Test: Calculate car-trip emissions based on given stops.
    Expect: Returns emissions and distance.
    """
    assert True


def test_co2_car__failed():
    """Test: Calling calc_co2_car with no arguments.
    Expect: Raises ValueError.
    """
    with pytest.raises(ValueError):
        candidate.calc_co2_car(distance=None, stops=None)


@pytest.mark.parametrize(
    "distance,size,expected_emissions",
    [
        pytest.param(100, None, 2.34, id="w/ defaults"),
        pytest.param(100, "medium", 2.39, id="w/ size"),
    ],
)
def test_calc_co2_motorbike__distance_based(
    distance: float, size: Optional[str], expected_emissions: float
):
    """Test: Calculate motorbike-trip emissions based on given distance.
    Expect: Returns emissions and distance.
    """
    actual_emissions, actual_distance = candidate.calc_co2_motorbike(
        distance=distance, stops=None, size=size
    )

    assert actual_emissions == expected_emissions
    assert actual_distance == distance


@pytest.mark.skip(reason="Not implemented yet")
def test_calc_co2_motorbike__stops_based():
    """Test: Calculate motorbike-trip emissions based on given stops.
    Expect: Returns emissions and distance.
    """
    assert True


def test_calc_co2_motorbike__failed():
    """Test: Calling calc_co2_motorbike with no arguments.
    Expect: Raises ValueError.
    """
    with pytest.raises(ValueError):
        candidate.calc_co2_motorbike(distance=None, stops=None)


@pytest.mark.parametrize(
    "distance,size,fuel_type,occupancy,vehicle_range,expected_emissions",
    [
        pytest.param(549, None, None, None, None, 21.63, id="w/ defaults"),
        pytest.param(549, "large", "diesel", 80, "long-distance", 12.3, id="w/ specs"),
    ],
)
def test_calc_co2_bus__distance_based(
    distance: float,
    size: Optional[str],
    fuel_type: Optional[str],
    occupancy: Optional[int],
    vehicle_range: Optional[str],
    expected_emissions: float,
):
    """Test: Calculate bus-trip emissions based on given distance.
    Expect: Returns emissions and distance.
    """

    # Calculate co2e
    actual_emissions, actual_distance = candidate.calc_co2_bus(
        distance=distance,
        stops=None,
        size=size,
        fuel_type=fuel_type,
        occupancy=occupancy,
        vehicle_range=vehicle_range,
    )

    assert round(actual_emissions, 2) == expected_emissions
    assert actual_distance == actual_distance


@pytest.mark.skip(reason="Not implemented yet")
def test_calc_co2_bus__stops_based():
    """Test: Calculate bus-trip emissions based on given stops.
    Expect: Returns emissions and distance.
    """
    assert True


def test_calc_co2_bus__failed():
    """Test: Calling calc_co2_bus with no arguments.
    Expect: Raises ValueError.
    """
    with pytest.raises(ValueError):
        candidate.calc_co2_bus(distance=None, stops=None)


@pytest.mark.parametrize(
    "distance,fuel_type,vehicle_range,expected_emissions",
    [
        pytest.param(1162, None, None, 38.23, id="w/ defaults"),
        pytest.param(1162, "electric", "long-distance", 37.18, id="w/ specs"),
    ],
)
def test_train__distance_based(
    distance: float,
    fuel_type: Optional[str],
    vehicle_range: Optional[str],
    expected_emissions: float,
):
    """Test: Calculate train-trip emissions based on given distance.
    Expect: Returns emissions and distance.
    """
    actual_emissions, actual_distance = candidate.calc_co2_train(
        distance=distance,
        stops=None,
        fuel_type=fuel_type,
        vehicle_range=vehicle_range,
    )

    # Check if expected result matches calculated result
    assert round(actual_emissions, 2) == expected_emissions


@pytest.mark.skip(reason="Not implemented yet")
def test_calc_co2_train__stops_based():
    """Test: Calculate train-trip emissions based on given stops.
    Expect: Returns emissions and distance.
    """
    assert True


def test_calc_co2_train__failed():
    """Test: Calling calc_co2_train with no arguments.
    Expect: Raises ValueError.
    """
    with pytest.raises(ValueError):
        candidate.calc_co2_train(distance=None, stops=None)


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
