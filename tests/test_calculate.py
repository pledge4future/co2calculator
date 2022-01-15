#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test co2calculator.calculate"""

import os
from typing import Optional, List, Dict
from attr.validators import optional

import pytest
from pytest_mock import MockerFixture

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
            id="defaults",
        ),
        pytest.param(
            444,
            3,
            "medium",
            "gasoline",
            34.188,
            id="optional arguments",
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


@pytest.mark.parametrize(
    "stops,passengers,size,fuel_type,expected_emissions",
    [
        pytest.param([{}], None, None, None, 9.03, id="1 stop, defaults"),
        pytest.param([{}, {}], None, None, None, 9.03, id="2 stops, defaults"),
        pytest.param(
            [{}], 1, "average", "gasoline", 9.408, id="1 stop, optional arguments"
        ),
        pytest.param(
            [{}, {}], 1, "average", "gasoline", 9.408, id="2 stops, optional arguments"
        ),
    ],
)
def test_calc_co2_car__stops_based(
    mocker: MockerFixture,
    stops: List[Dict],
    passengers: int,
    size: str,
    fuel_type: str,
    expected_emissions: float,
) -> None:
    """Test: Calculate car-trip emissions based on given stops.
    Expect: Returns emissions and distance.
    """
    patched_geocoding = mocker.patch(
        "co2calculator.calculate.geocoding_structured",
        return_value=("NAME", "COUNTRY", (1.0, 2.0), "RES"),
    )
    patched_get_route = mocker.patch(
        "co2calculator.calculate.get_route",
        return_value=42,
    )

    actual_emissions, _ = candidate.calc_co2_car(
        distance=None,
        stops=stops,
        passengers=passengers,
        size=size,
        fuel_type=fuel_type,
    )

    assert actual_emissions == expected_emissions

    assert patched_geocoding.call_count == len(stops)
    patched_get_route.assert_called_once()


def test_co2_car__failed():
    """Test: Calling calc_co2_car with no arguments.
    Expect: Raises ValueError.
    """
    with pytest.raises(ValueError):
        candidate.calc_co2_car(distance=None, stops=None)


@pytest.mark.parametrize(
    "distance,size,expected_emissions",
    [
        pytest.param(100, None, 2.34, id=" defaults"),
        pytest.param(100, "medium", 2.39, id="size"),
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
        pytest.param(549, None, None, None, None, 21.63, id="defaults"),
        pytest.param(
            549, "large", "diesel", 80, "long-distance", 12.3, id="optional arguments"
        ),
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
        pytest.param(1162, None, None, 38.23, id="defaults"),
        pytest.param(1162, "electric", "long-distance", 37.18, id="optional arguments"),
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


@pytest.mark.parametrize(
    "seating_class,mocked_distance,expected_emissions",
    [
        pytest.param(None, 1000, 170.31, id="defaults, short-haul"),
        pytest.param(None, 2000, 399.83, id="defaults, long-haul"),
        pytest.param("economy_class", 1000, 167.51, id="seating_class"),
    ],
)
def test_calc_co2_plane(
    mocker: MockerFixture,
    seating_class: Optional[str],
    mocked_distance: float,
    expected_emissions: float,
):
    """Test: Calculate plane-trip emissions based on start and destination.
    Expect: Returns emissions and distance.
    """
    # Mocking functions called by calc_co2_plane
    patched_geocoding_airport = mocker.patch(
        "co2calculator.calculate.geocoding_airport",
        return_value=("TEST", (1.0, 2.0), "TEST"),
    )
    patched_haversine = mocker.patch(
        "co2calculator.calculate.haversine",
        return_value=mocked_distance,
    )

    # Test
    actual_emissions, _ = candidate.calc_co2_plane(
        start="SOME", destination="SOME", seating_class=seating_class
    )

    assert round(actual_emissions, 2) == expected_emissions

    assert patched_geocoding_airport.call_count == 2
    patched_haversine.assert_called_once()


def test_calc_co2_plane__failed(mocker: MockerFixture):
    """Test: Calculation on plane-trip emissions fails due to false input.
    Expect: Raises ValueError.
    """
    # Mocking functions called by calc_co2_plane
    patched_geocoding_airport = mocker.patch(
        "co2calculator.calculate.geocoding_airport",
        return_value=("TEST", (1.0, 2.0), "TEST"),
    )
    patched_haversine = mocker.patch(
        "co2calculator.calculate.haversine",
        return_value=1,
    )

    with pytest.raises(ValueError):
        candidate.calc_co2_plane(
            start="SOME", destination="SOME", seating_class="NON-EXISTANT"
        )

    assert patched_geocoding_airport.call_count == 2
    patched_haversine.assert_called_once()


@pytest.mark.parametrize(
    "seating_class,expected_emissions",
    [
        pytest.param(None, 24.43, id="defaults"),
        pytest.param("average", 24.43, id="seating_class: 'average'"),
        # TODO: Investigate why foot and car passenger fail
        # pytest.param("Foot passenger", 1, id="seating_class: 'Foot passenger'"),
        # pytest.param("Car passenger", 1, id="seating_class: 'Car passenger"),
    ],
)
def test_calc_ferry(
    mocker: MockerFixture, seating_class: Optional[str], expected_emissions: float
):
    """Test: Calculate ferry-trip emissions based on start and destination.
    Expect: Returns emissions and distance.
    """
    # Mocking functions called by calc_co2_plane
    # TODO: Check if return mock (especially `coords` & `res`) is correct
    # (type annotation missing)
    patched_geocoding = mocker.patch(
        "co2calculator.calculate.geocoding_structured",
        return_value=("NAME", "COUNTRY", (1.0, 2.0), "RES"),
    )
    patched_haversine = mocker.patch(
        "co2calculator.calculate.haversine",
        return_value=100,
    )

    # Test
    actual_emissions, _ = candidate.calc_co2_ferry(
        start={}, destination={}, seating_class=seating_class
    )

    assert actual_emissions == expected_emissions

    assert patched_geocoding.call_count == 2
    patched_haversine.assert_called_once()


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
