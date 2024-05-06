#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test data handlers"""

from pathlib import Path
import pytest
from co2calculator.data_handlers import EmissionFactors, Airports, EUTrainStations
from co2calculator.parameters import HeatingEmissionParameters
import pandas as pd


test_data_dir = str(Path(__file__).parent.parent)


@pytest.fixture
def emission_factors_test():
    return EmissionFactors(data_dir=test_data_dir)


@pytest.fixture
def airports_test():
    return Airports()


@pytest.fixture
def eu_train_stations_test():
    return EUTrainStations()


def test_load_emission_factors(emission_factors_test):
    """Test if the emission factors are loaded correctly"""
    assert isinstance(emission_factors_test.heating, pd.DataFrame)
    assert isinstance(emission_factors_test.electricity, pd.DataFrame)
    assert isinstance(emission_factors_test.transport, pd.DataFrame)


def test_load_airports(airports_test):
    """Test if the airports are loaded correctly"""
    assert isinstance(airports_test.airports, pd.DataFrame)


def test_load_train_stations(eu_train_stations_test):
    """Test if the train stations are loaded correctly"""
    assert isinstance(eu_train_stations_test.stations, pd.DataFrame)
