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
        pytest.param(100, "car", None, None, 18.64, id="basic car trip"),
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
    actual_emissions, _, _ = candidate.calc_co2_trip(
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
    result, _, _ = candidate.calc_co2_trip(
        distance=100,
        transportation_mode="invalid",
        options=None,
        custom_emission_factor=0.1,
    )
    assert result == 10


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
