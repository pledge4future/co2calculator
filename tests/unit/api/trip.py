#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for Trip class"""


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
