#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Unit tests for co2calculator.calculate module"""

from typing import Optional

import pytest
from pytest_mock import MockerFixture

import co2calculator.calculate as candidate
from co2calculator.constants import RangeCategory
from pydantic import ValidationError

from co2calculator.exceptions import ConversionFactorNotFound


@pytest.mark.parametrize(
    "distance,passengers,size,fuel_type,expected_emissions",
    [
        pytest.param(100, None, None, None, 21.5, id="defaults"),
        pytest.param(444, 3, "medium", "gasoline", 34.19, id="all optional arguments"),
        pytest.param(10, 1, "small", None, 1.79, id="size: 'small'"),
        pytest.param(10, 1, "medium", None, 2.09, id="size: 'medium'"),
        pytest.param(10, 1, "large", None, 2.74, id="size: 'large'"),
        pytest.param(10, 1, "average", None, 2.15, id="size: 'average'"),
        pytest.param(10, 1, None, "diesel", 2.01, id="fuel_type: 'diesel'"),
        pytest.param(10, 1, None, "gasoline", 2.24, id="fuel_type: 'gasoline'"),
        pytest.param(10, 1, None, "cng", 2.37, id="fuel_type: 'cng'"),
        pytest.param(10, 1, None, "electric", 0.51, id="fuel_type: 'electric'"),
        pytest.param(10, 1, None, "hybrid", 1.2, id="fuel_type: 'hybrid'"),
        pytest.param(
            10, 1, None, "plug-in_hybrid", 0.93, id="fuel_type: 'plug-in_hybrid'"
        ),
        pytest.param(10, 1, None, "average", 2.15, id="fuel_type: 'average'"),
    ],
)
def test_calc_co2_car(
    distance: float,
    passengers: Optional[int],
    size: Optional[str],
    fuel_type: Optional[str],
    expected_emissions: float,
):
    """Test: Calculate car-trip emissions based on given distance.
    Expect: Returns emissions and distance.
    """
    actual_emissions = candidate.calc_co2_car(
        distance=distance,
        passengers=passengers,
        size=size,
        fuel_type=fuel_type,
    )

    assert round(actual_emissions, 2) == expected_emissions


@pytest.mark.parametrize(
    "distance,size,expected_emissions",
    [
        pytest.param(100, None, 11.36, id="defaults"),
        pytest.param(100, "small", 8.31, id="size: 'small'"),
        pytest.param(100, "medium", 10.09, id="size: 'medium'"),
        pytest.param(100, "large", 13.24, id="size: 'large'"),
        pytest.param(100, "average", 11.36, id="size: 'average'"),
    ],
)
def test_calc_co2_motorbike(
    distance: float, size: Optional[str], expected_emissions: float
):
    """Test: Calculate motorbike-trip emissions based on given distance.
    Expect: Returns emissions and distance.
    """
    actual_emissions = candidate.calc_co2_motorbike(distance=distance, size=size)

    assert round(actual_emissions, 2) == expected_emissions


@pytest.mark.parametrize(
    "distance,size,fuel_type,occupancy,vehicle_range,expected_emissions",
    [
        pytest.param(549, None, None, None, None, 21.63, id="defaults"),
        pytest.param(
            549, "large", "diesel", 80, "long-distance", 12.3, id="optional arguments"
        ),
        pytest.param(10, "medium", None, None, None, 0.42, id="size: 'medium'"),
        pytest.param(10, "large", None, None, None, 0.33, id="size: 'large'"),
        pytest.param(10, "average", None, None, None, 0.39, id="size: 'average'"),
        pytest.param(10, None, None, 20, None, 0.92, id="occupancy: 20"),
        pytest.param(10, None, None, 50, None, 0.39, id="occupancy: 50"),
        pytest.param(10, None, None, 80, None, 0.26, id="occupancy: 80"),
        pytest.param(10, None, None, 100, None, 0.22, id="occupancy: 100"),
        pytest.param(10, None, None, None, "local", 0.39, id="vehicle_range: 'local'"),
        pytest.param(
            10,
            None,
            None,
            None,
            "long-distance",
            0.39,
            id="vehicle_range: 'long-distance'",
        ),
        pytest.param(
            10,
            "small",
            "diesel",
            None,
            "long-distance",
            0.39,
            id="size: 'small', fuel_type: `diesel`, vehicle_range: 'long-distance'",
        ),
        pytest.param(
            10,
            "medium",
            "cng",
            None,
            "long-distance",
            0.62,
            id="fuel_type: `cng` and size",
        ),
        pytest.param(
            10,
            "small",
            "hydrogen",
            None,
            "local",
            0.25,
            id="fuel_type: `hydrogen` and size",
        ),
    ],
)
def test_calc_co2_bus(
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
    actual_emissions = candidate.calc_co2_bus(
        distance=distance,
        size=size,
        fuel_type=fuel_type,
        occupancy=occupancy,
        vehicle_range=vehicle_range,
    )

    assert round(actual_emissions, 2) == expected_emissions


@pytest.mark.parametrize(
    "distance,fuel_type,vehicle_range,expected_emissions",
    [
        pytest.param(1162, None, None, 38.23, id="defaults"),
        pytest.param(
            1162, "electric", "long-distance", 37.18, id="all optional arguments"
        ),
        pytest.param(10, "electric", None, 0.32, id="fuel_type: 'electric'"),
        pytest.param(10, "diesel", None, 0.7, id="fuel_type: 'diesel'"),
        pytest.param(10, "average", None, 0.33, id="fuel_type: 'average'"),
        pytest.param(10, None, "local", 0.6, id="vehicle_range: 'local'"),
        pytest.param(
            10, None, "long-distance", 0.33, id="vehicle_range: 'long-distance'"
        ),
    ],
)
def test_calc_co2_train(
    distance: float,
    fuel_type: Optional[str],
    vehicle_range: Optional[str],
    expected_emissions: float,
):
    """Test: Calculate train-trip emissions based on given distance.
    Expect: Returns emissions and distance.
    """

    actual_emissions = candidate.calc_co2_train(
        distance=distance, fuel_type=fuel_type, vehicle_range=vehicle_range
    )

    assert round(actual_emissions, 2) == expected_emissions


@pytest.mark.parametrize(
    "distance,seating_class,expected_emissions",
    [
        pytest.param(1000, None, 153.53, id="defaults, short-haul"),
        pytest.param(2000, None, 307.06, id="defaults, long-haul"),
        pytest.param(1000, "economy_class", 151.52, id="seating_class"),
    ],
)
def test_calc_co2_plane(
    distance: float,
    seating_class: Optional[str],
    expected_emissions: float,
):
    """Test: Calculate plane-trip emissions based on given distance.
    Expect: Returns emissions and distance.
    """

    actual_emissions = candidate.calc_co2_plane(
        distance=distance, seating=seating_class
    )

    assert round(actual_emissions, 2) == expected_emissions


def test_calc_co2_plane__failed() -> None:
    """Test: Calculation on plane-trip emissions fails due to false input.
    Expect: Raises ValidationError.
    """
    with pytest.raises(ValidationError):
        candidate.calc_co2_plane(distance=5000, seating="NON-EXISTENT")


def test_calc_co2_plane__invalid_distance_seating_combo() -> None:
    """Test: Calculation on plane-trip emissions fails due to false input.
    Expect: Raises ValueError.
    """
    # Check if raises warning (premium economy class is not available for short-haul flights)
    with pytest.raises(ConversionFactorNotFound):
        candidate.calc_co2_plane(distance=800, seating="premium_economy_class")


@pytest.mark.parametrize(
    "seating_class,expected_emissions",
    [
        pytest.param(None, 11.29, id="defaults"),
        pytest.param("average", 11.29, id="seating_class: 'average'"),
        pytest.param("foot_passenger", 1.87, id="seating_class: 'Foot passenger'"),
        pytest.param("car_passenger", 12.95, id="seating_class: 'Car passenger"),
    ],
)
def test_calc_ferry(seating_class: Optional[str], expected_emissions: float) -> None:
    """Test: Calculate ferry-trip emissions based on given distance.
    Expect: Returns emissions and distance.
    """
    actual_emissions = candidate.calc_co2_ferry(distance=100, seating=seating_class)
    assert round(actual_emissions, 2) == expected_emissions


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
    [
        pytest.param(
            "car", 30, "medium", "gasoline", None, None, 6.93, id="car commute"
        ),
        pytest.param("bicycle", 60, None, None, None, None, 0.54, id="bicycle commute"),
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
