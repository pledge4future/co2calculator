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


@pytest.mark.parametrize(
    "distance, transportation_mode,options,custom_emission_factor,expected_emissions",
    [
        pytest.param(100, "car", None, None, 21.5, id="basic car trip"),
        pytest.param(
            100, "car", None, 0.1, 10.0, id="car trip with custom emission factor"
        ),
    ],
)
def test_calc_co2_trip(
    distance: float,
    transportation_mode: str,
    options: dict,
    custom_emission_factor: float,
    expected_emissions: float,
):
    """Test: Calculate car-trip emissions based on given distance.
    Expect: Returns emissions and distance.
    """
    actual_emissions = candidate.calc_co2_trip(
        distance=distance,
        transportation_mode=transportation_mode,
        options=options,
        custom_emission_factor=custom_emission_factor,
    )

    assert actual_emissions == expected_emissions


def test_calc_co2_trip_invalid_transportation_mode():
    """Test: Calculate car-trip emissions with invalid transportation mode.
    Expect: Test fails.
    """
    with pytest.raises(AssertionError):
        candidate.calc_co2_trip(
            distance=100,
            transportation_mode="invalid",
            options=None,
            custom_emission_factor=None,
        )


def test_calc_co2_trip_invalid_options_for_transportation_mode():
    """Test: Should raise exception if options are not valid for transportation mode.
    Expect: Test fails.
    """
    with pytest.raises(ValueError):
        candidate.calc_co2_trip(
            distance=100,
            transportation_mode="car",
            options={"size": "big"},
            custom_emission_factor=None,
        )


def test_calc_co2_trip_ignore_error_on_custom_emission_factor():
    """Test: Should ignore invalid transportation mode if custom emission factor is set"""
    result = candidate.calc_co2_trip(
        distance=100,
        transportation_mode="invalid",
        options=None,
        custom_emission_factor=0.1,
    )
    assert result == 10


# @pytest.mark.skip(
#    reason="Failing right now, but units will change anyways. let's check after the co2factors are updated"
# )
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
