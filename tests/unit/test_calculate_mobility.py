#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Unit tests for co2calculator.calculate module"""

from typing import Optional

from pydantic import ValidationError
import pytest
from pytest_mock import MockerFixture

import co2calculator.mobility.calculate_mobility as mobility

from co2calculator.exceptions import ConversionFactorNotFound, EmissionFactorNotFound


@pytest.mark.parametrize(
    "distance,options,expected_emissions",
    [
        pytest.param(100, None, 21.5, id="defaults"),
        pytest.param(
            444,
            {"passengers": 3, "size": "medium", "fuel_type": "gasoline"},
            34.19,
            id="all optional arguments",
        ),
        pytest.param(
            10, {"passengers": 1, "size": "average"}, 1.79, id="only 2 arguments'"
        ),
        pytest.param(10, {"passengers": 1}, 2.15, id="only passengers'"),
        pytest.param(10, {}, 2.15, id="empty options'"),
    ],
)
def test_calc_co2_car(distance: float, options: dict, expected_emissions: float):
    """Test: Calculate car-trip emissions based on given distance.
    Expect: Returns emissions and distance.
    """
    actual_emissions = mobility.calc_co2_car(distance=distance, options=options)

    assert isinstance(actual_emissions, float)


@pytest.mark.parametrize(
    "distance,options,expected_emissions",
    [
        pytest.param(100, None, 11.36, id="defaults"),
        pytest.param(100, {"size": "small"}, 8.31, id="size: 'small'"),
        pytest.param(100, {}, 11.36, id="size: 'medium'"),
    ],
)
def test_calc_co2_motorbike(distance: float, options: dict, expected_emissions: float):
    """Test: Calculate motorbike-trip emissions based on given distance.
    Expect: Returns emissions and distance.
    """
    actual_emissions = mobility.calc_co2_motorbike(distance=distance, options=options)

    assert isinstance(actual_emissions, float)


@pytest.mark.parametrize(
    "distance,options,expected_emissions",
    [
        pytest.param(549, None, 21.63, id="defaults"),
        pytest.param(
            549,
            {
                "size": "large",
                "fuel_type": "diesel",
                "occupancy": 80,
                "vehicle_range": "long-distance",
            },
            12.3,
            id="all options",
        ),
        pytest.param(10, {"size": "small"}, 0.42, id="size: 'small'"),
        pytest.param(10, {"occupancy": 20}, 0.92, id="occupancy: 20"),
        pytest.param(10, {"vehicle_range": "local"}, 0.39, id="local range"),
        pytest.param(
            549,
            {},
            21.63,
            id="empty options",
        ),
    ],
)
def test_calc_co2_bus(
    distance: float,
    options: dict,
    expected_emissions: float,
):
    """Test: Calculate bus-trip emissions based on given distance.
    Expect: Returns emissions and distance.
    """

    # Calculate co2e
    actual_emissions = mobility.calc_co2_bus(
        distance=distance,
        options=options,
    )

    assert isinstance(actual_emissions, float)


@pytest.mark.parametrize(
    "distance,options,expected_emissions",
    [
        pytest.param(1162, None, 38.23, id="defaults"),
        pytest.param(1162, {}, 38.23, id="defaults on empty"),
        pytest.param(
            1162,
            {"vehicle_range": "long-distance"},
            37.18,
            id="all optional arguments",
        ),
    ],
)
def test_calc_co2_train(
    distance: float,
    options: dict,
    expected_emissions: float,
):
    """Test: Calculate train-trip emissions based on given distance.
    Expect: Returns emissions and distance.
    """

    actual_emissions = mobility.calc_co2_train(distance=distance, options=options)

    assert isinstance(actual_emissions, float)


@pytest.mark.parametrize(
    "distance,options,expected_emissions",
    [
        pytest.param(1000, None, 153.53, id="defaults on none, short-haul"),
        pytest.param(2000, {}, 307.06, id="defaults on empty, long-haul"),
        pytest.param(1000, {"seating": "economy_class"}, 151.52, id="seating_class"),
    ],
)
def test_calc_co2_plane(
    distance: float,
    options: dict,
    expected_emissions: float,
):
    """Test: Calculate plane-trip emissions based on given distance.
    Expect: Returns emissions and distance.
    """

    actual_emissions = mobility.calc_co2_plane(distance=distance, options=options)

    assert isinstance(actual_emissions, float)


def test_calc_co2_plane__failed() -> None:
    """Test: Calculation on plane-trip emissions fails due to false input.
    Expect: Raises ValidationError.
    """
    with pytest.raises(ValidationError):
        mobility.calc_co2_plane(distance=5000, options={"seating": "NON-EXISTENT"})


def test_calc_co2_plane__invalid_distance_seating_combo() -> None:
    """Test: Calculation on plane-trip emissions fails due to false input.
    Expect: Raises ValueError.
    """
    # Check if raises warning (premium economy class is not available for short-haul flights)
    with pytest.raises(EmissionFactorNotFound):
        mobility.calc_co2_plane(distance=800, options={"seating": "first_class"})


@pytest.mark.parametrize(
    "options,expected_emissions",
    [
        pytest.param(None, 11.29, id="defaults"),
        pytest.param({}, 11.29, id="defaults on empty"),
        pytest.param({"seating": "average"}, 11.29, id="seating_class: 'average'"),
        pytest.param(
            {"seating": "foot_passenger"}, 1.87, id="seating_class: 'Foot passenger'"
        ),
    ],
)
def test_calc_ferry(options: dict, expected_emissions: float) -> None:
    """Test: Calculate ferry-trip emissions based on given distance.
    Expect: Returns emissions and distance.
    """
    actual_emissions = mobility.calc_co2_ferry(distance=100, options=options)
    assert isinstance(actual_emissions, float)
