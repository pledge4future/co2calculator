#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for distance computation"""

import os
from pathlib import Path

import numpy as np
import pytest
from dotenv import load_dotenv
from pydantic import ValidationError

from co2calculator.distances import (
    haversine,
    geocoding_airport,
    is_valid_geocoding_dict,
    geocoding_train_stations,
)

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
    distance = haversine(lat_a, long_a, lat_b, long_b)

    # Check if expected result matches calculated result
    assert distance == pytest.approx(distance_expected, rel=0.01)


def test_geocoding_airport_FRA(mocker):
    """Test geocoding of airports using IATA code"""
    # Given parameters
    iata = "FRA"  # Frankfurt Airport, Frankfurt a.M. (Germany)
    coords = [50.033056, 8.570556]

    # mock API call
    mocker.patch(
        "co2calculator.distances.geocoding_airport",
        return_values=["Flughafen Frankfurt am Main", [8.579247, 50.051285], "DEU"],
    )

    # Retrieve coordinates
    name, res_coords, res_country = geocoding_airport(iata)

    # Check if expected coordinates match retrieved coordinates
    assert np.allclose(coords[::-1], res_coords, atol=0.03)


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

    # Call function; test will pass if no error is raised
    is_valid_geocoding_dict(loc_dict)


def test_invalid_geocoding_dict():
    """Test if a providing an invalid geocoding raises an error"""
    # Given parameters
    loc_dict = {
        "country": "DE",
        "locality": "Heidelberg",
        "adress": "Im Bosseldorn 25",  # wrong spelling of "address"
    }

    # Check if raises error
    with pytest.raises(AssertionError) as e:
        is_valid_geocoding_dict(loc_dict)
    assert e.type is AssertionError


def test_geocoding_train_stations_invalid_dict():
    """Test geocoding of train stations if dictionary with invalid parameters is provided"""

    # Given parameters
    station_dict = {
        "country": "DE",
        "address": "Heidelberg Hbf",
    }  # invalid parameters; has to be specified as "station_name"

    # Check if raises error
    with pytest.raises(ValidationError) as e:
        geocoding_train_stations(station_dict)
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
        geocoding_train_stations(station_dict)
    assert e.type is ValidationError


def test_geocoding_train_stations():
    """Test geocoding of train stations if dictionary with invalid parameters is provided"""
    # Given parameters

    station_dict = {
        "country": "DE",
        "station_name": "Heidelberg Hbf",
    }
    coords = [49.404381, 8.675858]

    station_name, country, res_coords = geocoding_train_stations(station_dict)

    assert station_name == "Heidelberg"
    assert country == station_dict["country"]
    # Check if expected coordinates match retrieved coordinates
    assert np.allclose(coords, res_coords, atol=0.03)
