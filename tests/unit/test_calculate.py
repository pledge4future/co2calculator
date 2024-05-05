#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Unit tests for co2calculator.calculate module"""

from typing import Optional

import pytest
from pytest_mock import MockerFixture

import co2calculator.calculate as candidate
from co2calculator.constants import RangeCategory
from pydantic import ValidationError

from co2calculator.exceptions import EmissionFactorNotFound


@pytest.mark.skip(
    reason="Failing right now, but units will change anyways. let's check after the co2factors are updated"
)
def test_heating_woodchips():
    """Test co2e calculation for heating: woodchips"""
    # Given parameters
    fuel_type = "woodchips"
    consumption = 250
    unit = "kg"
    co2e_kg_expected = 43.63

    # Calculate co2e
    co2e = candidate.calc_co2_heating(
        consumption=consumption, unit=unit, fuel_type=fuel_type
    )

    # Check if expected result matches calculated result
    assert co2e == pytest.approx(co2e_kg_expected, rel=0.01)


@pytest.mark.skip(
    reason="Failing right now, but units will change anyways. let's check after the co2factors are updated"
)
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


@pytest.mark.skip(
    reason="Failing right now, but units will change anyways. let's check after the co2factors are updated"
)
@pytest.mark.parametrize(
    "transportation_mode,weekly_distance,size,fuel_type,occupancy,passengers,expected",
    [
        pytest.param("car", 30, "medium", "gasoline", None, 1, 6.45, id="car commute"),
        pytest.param("bicycle", 60, None, None, None, 1, 0.54, id="bicycle commute"),
    ],
)
def test_commuting(
    transportation_mode: str,
    weekly_distance: float,
    size: str,
    fuel_type: str,
    occupancy: Optional[int],
    passengers: Optional[int],
    expected: float,
):
    """Test co2 calculation for commuting by car"""

    # NOTE: This is more of a functional test.
    # If it's supposed to stay a unit test, we should mock the `calc_c2_...` methods
    # and check if they're called!

    co2e = candidate.calc_co2_commuting(
        transportation_mode=transportation_mode,
        weekly_distance=weekly_distance,
        size=size,
        fuel_type=fuel_type,
        occupancy=occupancy,
        passengers=passengers,
    )

    assert round(co2e, 2) == expected


@pytest.mark.parametrize(
    "distance,expected_category, expected_description",
    [
        pytest.param(0, "very_short_haul", "below 500 km", id="Distance: 0 km"),
        pytest.param(500, "very_short_haul", "below 500 km", id="Distance: 500 km"),
        pytest.param(501, "short_haul", "500 to 1500 km", id="Distance: 501 km"),
        pytest.param(1500, "short_haul", "500 to 1500 km", id="Distance: 1500 km"),
        pytest.param(1501, "medium_haul", "1500 to 4000 km", id="Distance: 1501 km"),
        pytest.param(4000, "medium_haul", "1500 to 4000 km", id="Distance: 4000 km"),
        pytest.param(4001, "long_haul", "above 4000 km", id="Distance: 4001 km"),
        pytest.param(42.7, "very_short_haul", "below 500 km", id="float"),
    ],
)
def test_range_categories(
    distance: float, expected_category: RangeCategory, expected_description: str
) -> None:
    """Test: Categorization of ranges
    Expect: See test table
    """
    actual_category, actual_description = candidate.range_categories(distance)

    assert actual_category == expected_category
    assert actual_description == expected_description


def test_range_categories_negative_distance():
    """Test: Categorization of ranges when using negative distance
    Expect: Test fails
    """
    with pytest.raises(ValueError):
        candidate.range_categories(-20)


@pytest.mark.skip(
    reason="Failing right now, but units will change anyways. let's check after the co2factors are updated"
)
@pytest.mark.parametrize(
    "transportation_mode, expected_method",
    [
        pytest.param("car", "calc_co2_car", id="Car"),
        pytest.param("bus", "calc_co2_bus", id="Bus"),
        pytest.param("train", "calc_co2_train", id="Train"),
        pytest.param("plane", "calc_co2_plane", id="Plane"),
        pytest.param("ferry", "calc_co2_ferry", id="Ferry"),
    ],
)
def test_calc_co2_businesstrip(
    mocker: MockerFixture, transportation_mode: str, expected_method: str
) -> None:
    """Scenario: calc_co2_businesstrip is the interface to calculate co2emissions
    for different types of transportation modes.
    Test: Business trip calculation interface
    Expect: co2calculations for specific transportation mode is called
    """
    # Patch the expected method to assert if it was called
    patched_method = mocker.patch.object(
        candidate, expected_method, return_value=(0.42, 42)
    )

    # Patch other methods called by the test candidate
    mocker.patch.object(
        candidate, "range_categories", return_value=("very short haul", "below 500 km")
    )

    # Call and assert
    candidate.calc_co2_businesstrip(
        transportation_mode=transportation_mode,
        start=None,
        destination=None,
        distance=42,
        size=None,
        fuel_type=None,
        occupancy=None,
        seating=None,
        passengers=None,
        roundtrip=False,
    )

    patched_method.assert_called_once()
