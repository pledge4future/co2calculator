#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for Trip class"""
import pytest

from co2calculator import TransportationMode
from co2calculator.api.trip import Trip


def test_instantiate_trip_by_car():
    """Test whether class is instantiated correctly"""

    trip = Trip(300).by_car()
    assert trip.transport_mode == TransportationMode.CAR
    assert trip.fuel_type is None
    assert trip.size is None


def test_trip_by_car_calculation():
    """Test whether class is instantiated correctly"""

    emissions = Trip(300).by_car().calculate_co2e()
    assert isinstance(emissions.co2e, float)


def test_trip_by_car_distance_calculation():
    """Test whether class is instantiated correctly"""
    start = {"locality": "Heidelberg", "country": "Germany"}
    destination = {"locality": "Mannheim", "country": "Germany"}

    distance = Trip(start=start, destination=destination).by_car().calculate_distance()
    assert isinstance(distance, float)
    assert distance == pytest.approx(31, 1)
