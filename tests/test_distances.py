#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for distance computation"""

import os
from pathlib import Path

import numpy as np
import pytest
from dotenv import load_dotenv
from pydantic import ValidationError

import co2calculator

load_dotenv()
ORS_API_KEY = os.environ.get("ORS_API_KEY")
script_path = str(Path(__file__).parent.parent)


def test_haversine():
    """Test haversine function to calculate distance"""
    # Given parameters
    # a: Frankfurt airport (FRA)
    lat_a = 50.0264
    long_a = 8.5431
    # b: Barcelona airport (BCN)
    lat_b = 41.2971
    long_b = 2.07846

    # Calculate distance
    distance_expected = 1092
    distance = co2calculator.distances.haversine(lat_a, long_a, lat_b, long_b)

    # Check if expected result matches calculated result
    assert distance == pytest.approx(distance_expected, rel=0.01)


def test_geocoding_airport_pelias_FRA(mocker):
    """Test geocoding of airports using IATA code"""
    # Given parameters
    iata = "FRA"  # Frankfurt Airport, Frankfurt a.M. (Germany)
    coords = [50.033056, 8.570556]

    # mock API call
    mocker.patch(
        "co2calculator.distances.geocoding_airport_pelias",
        return_value=["Flughafen Frankfurt am Main", [8.579247, 50.051285], "DEU"],
    )

    # Retrieve coordinates
    name, res_coords, res_country = co2calculator.distances.geocoding_airport_pelias(
        iata
    )

    # Check if expected coordinates match retrieved coordinates
    assert np.allclose(coords[::-1], res_coords, atol=0.03)


def test_geocoding_airport_HAM():
    """Test geocoding of airports using IATA code"""
    # Given parameters
    iata = "HAM"  # Hamburg Airport
    coords = [53.630278, 9.988333]

    # Retrieve coordinates
    name, res_coords, res_country = co2calculator.distances.geocoding_airport(iata)

    # Check if expected coordinates match retrieved coordinates
    assert np.allclose(np.array(coords)[::-1], np.array(res_coords), atol=0.03)


def test_geocoding_airport_EAP():
    """Test geocoding of airports using IATA code"""
    # Given parameters
    iata = "EAP"  # Basel-Mulhouse

    # Airport currently does not exist in database, check if call raises an error
    with pytest.raises(ValidationError) as e:
        co2calculator.distances.geocoding_airport(iata)
    assert e.type is ValidationError


def test_geocoding_structured():
    """To do"""
    pass


def test_valid_geocoding_dict():
    """Test if a valid geocoding dictionary is recognized as valid"""
    # Given parameters
    loc_dict = {
        "country": "DE",
        "region": "Baden-Württemberg",
        "county": "Rhein-Neckar-Kreis",
        "locality": "Heidelberg",
        "borough": "Rohrbach",
        "address": "Im Bosseldorn 25",
        "postalcode": "69126",
        "neighbourhood": None,
    }
    # Check if raises error
    co2calculator.distances.geocoding_structured(loc_dict)


def test_invalid_geocoding_dict():
    """Test if a providing an invalid geocoding raises an error"""
    # Given parameters
    loc_dict = {
        "country": "DE",
        "locality": "Heidelberg",
        "adress": "Im Bosseldorn 25",  # wrong spelling of "address"
    }
    # Check if raises error
    with pytest.raises(ValidationError) as e:
        co2calculator.distances.geocoding_structured(loc_dict)
    assert e.type is ValidationError


def test_geocoding_train_stations_invalid_dict():
    """Test geocoding of train stations if dictionary with invalid parameters is provided"""
    # Given parameters
    station_dict = {
        "country": "DE",
        "address": "Heidelberg Hbf",
    }  # invalid parameters; has to be specified as "station_name"
    # Check if raises error
    with pytest.raises(ValidationError) as e:
        co2calculator.distances.geocoding_train_stations(station_dict)
    assert e.type is ValidationError


def test_geocoding_train_stations_invalid_country():
    """Test geocoding of train stations if dictionary with invalid country code is provided"""
    # Given parameters
    station_dict = {
        "country": "DU",  # invalid
        "station_name": "Heidelberg Hbf",
    }
    # Check if raises error
    with pytest.raises(ValidationError) as e:
        co2calculator.distances.geocoding_train_stations(station_dict)
    assert e.type is ValidationError


def test_geocoding_train_stations():
    """Test geocoding of European train station"""
    # Given parameters
    station_dict = {
        "country": "DE",
        "station_name": "Heidelberg Hbf",
    }
    coords = [49.404381, 8.675858]
    (
        station_name,
        country,
        res_coords,
    ) = co2calculator.distances.geocoding_train_stations(station_dict)
    assert station_name == "Heidelberg"
    assert country == station_dict["country"]
    # Check if expected coordinates match retrieved coordinates
    assert np.allclose(coords, res_coords, atol=0.03)


@pytest.mark.parametrize(
    "distance, transportation_mode, expected_distance",
    [
        pytest.param(100, "train", 120.0, id="Train"),
        pytest.param(100, "bus", 150.0, id="Bus"),
        pytest.param(100, "plane", 195.0, id="Plane"),
        pytest.param(100, "car", 100.0, id="Car"),
    ],
)
def test_apply_detour(
    distance: float, transportation_mode: str, expected_distance: float
) -> None:
    """Test apply detour function"""
    distance_with_detour = co2calculator.distances._apply_detour(
        distance, transportation_mode
    )
    assert distance_with_detour == expected_distance
