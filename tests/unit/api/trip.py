#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for Trip class"""
import pytest

from co2calculator import TransportationMode
from co2calculator.api.emission import Emissions
from co2calculator.api.trip import Trip
from co2calculator.distances import TrainStation


def test_instantiate_trip_by_car():
    """Test whether class is instantiated correctly"""
    trip = Trip(300).by_car()
    assert trip.transport_mode == TransportationMode.CAR
    assert trip.fuel_type is None
    assert trip.size is None


def test_trip_by_car_calculation():
    """Test whether trip emissions are calculated correctly"""
    emissions = Trip(300).by_car().calculate_co2e()
    assert isinstance(emissions, Emissions)
    assert isinstance(emissions.co2e, float)


def test_trip_by_car_distance_calculation():
    """Test whether distance is calculated correctly"""
    start = {"locality": "Heidelberg", "country": "Germany"}
    destination = {"locality": "Mannheim", "country": "Germany"}

    distance = Trip(start=start, destination=destination).by_car().calculate_distance()
    assert isinstance(distance, float)
    assert distance == pytest.approx(31, 1)


def test_instantiate_trip_by_train():
    """Test whether class is instantiated correctly"""
    trip = Trip(300).by_train()
    assert trip.transport_mode == TransportationMode.TRAIN


def test_trip_by_train_calculation():
    """Test whether trip emissions are calculated correctly"""
    emissions = Trip(300).by_train().calculate_co2e()
    assert isinstance(emissions, Emissions)
    assert isinstance(emissions.co2e, float)


def test_trip_by_train_distance_calculation():
    """Test whether distance is calculated correctly"""
    start = {"station_name": "Heidelberg Hbf", "country": "DE"}
    destination = {"station_name": "Mannheim Hbf", "country": "DE"}

    distance = (
        Trip(start=start, destination=destination).by_train().calculate_distance()
    )
    assert isinstance(distance, float)


def test_instantiate_trip_by_plane():
    """Test whether class is instantiated correctly"""
    trip = Trip(300).by_plane()
    assert trip.transport_mode == TransportationMode.PLANE
    assert trip.seating is None


# def test_trip_by_plane_calculation():
#    """Test whether trip emissions are calculated correctly"""
#    emissions = Trip(300).by_plane().calculate_co2e()
#    assert isinstance(emissions, Emissions)
#    assert isinstance(emissions.co2e, float)


def test_trip_by_plane_distance_calculation():
    """Test whether distance is calculated correctly"""
    start = "FRA"
    destination = "STR"

    distance = (
        Trip(start=start, destination=destination).by_plane().calculate_distance()
    )
    assert isinstance(distance, float)


def test_instantiate_trip_by_tram():
    """Test whether class is instantiated correctly"""
    trip = Trip(300).by_tram()
    assert trip.transport_mode == TransportationMode.TRAM


# def test_trip_by_tram_calculation():
#    """Test whether trip emissions are calculated correctly"""
#    emissions = Trip(300).by_tram().calculate_co2e()
#    assert isinstance(emissions, Emissions)
#    assert isinstance(emissions.co2e, float)


def test_instanitate_trip_by_ferry():
    """Test whether class is instantiated correctly"""
    trip = Trip(300).by_ferry()
    assert trip.transport_mode == TransportationMode.FERRY
    assert trip.ferry_class is None


def test_trip_by_ferry_calculation():
    """Test whether trip emissions are calculated correctly"""
    emissions = Trip(300).by_ferry().calculate_co2e()
    assert isinstance(emissions, Emissions)
    assert isinstance(emissions.co2e, float)


# def test_trip_by_ferry_distance_calculation():
#    """Test whether distance is calculated correctly"""
#    start = {"locality": "Winterhuder Fährhaus", "country":"Germany"}
#    destination = {"locality": "Streekbrücke", "country":"Germany"}

#    distance = (Trip(start=start, destination=destination).by_ferry().calculate_distance())
#
# assert isinstance(distance, float)


def test_instantiate_trip_by_bus():
    """Test whether class is instantiated correctly"""
    trip = Trip(300).by_bus()
    assert trip.transport_mode == TransportationMode.BUS
    assert trip.fuel_type is None
    assert trip.size is None
    assert trip.range is None


def test_trip_by_bus_calculation():
    """Test whether trip emissions are calculated correctly"""
    emissions = Trip(300).by_bus().calculate_co2e()
    assert isinstance(emissions, Emissions)
    assert isinstance(emissions.co2e, float)


def test_trip_by_bus_distance_calculation():
    """Test whether distance is calculated correctly"""
    start = {"locality": "Heidelberg", "country": "Germany"}
    destination = {"locality": "Mannheim", "country": "Germany"}

    distance = Trip(start=start, destination=destination).by_bus().calculate_distance()
    assert isinstance(distance, float)
    assert distance == pytest.approx(31, 1)


def test_instantiate_trip_by_motorbike():
    """Test whether class is instantiated correctly"""
    trip = Trip(300).by_motorbike()
    assert trip.transport_mode == TransportationMode.MOTORBIKE
    assert trip.size is None


def test_trip_by_motorbike_calculation():
    """Test whether trip emissions are calculated correctly"""
    emissions = Trip(300).by_motorbike().calculate_co2e()
    assert isinstance(emissions, Emissions)
    assert isinstance(emissions.co2e, float)


def test_trip_by_motorbike_distance_calculation():
    """Test whether distance is calculated correctly"""
    start = {"locality": "Heidelberg", "country": "Germany"}
    destination = {"locality": "Mannheim", "country": "Germany"}

    distance = (
        Trip(start=start, destination=destination).by_motorbike().calculate_distance()
    )
    assert isinstance(distance, float)
    assert distance == pytest.approx(31, 1)


# def test_trip_by_train_distance_calculation():
#    """Test whether class is instantiated correctly"""
#    start = {"locality": "Heidelberg", "country": "Germany"}
#    destination = {"locality": "Mannheim", "country": "Germany"}

#    distance = (
#        Trip(start=start, destination=destination).by_train().calculate_distance()
#    )
#    assert isinstance(distance, float)
