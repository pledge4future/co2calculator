#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for Trip class"""
import pytest

from co2calculator import TransportationMode
from co2calculator.api.emission import Emissions
from co2calculator.api.trip import Trip


def test_instantiate_trip_by_car():
    """Test whether class is instantiated correctly"""
    trip = Trip(300).by_car()
    assert trip.transportation_mode == TransportationMode.CAR
    assert trip.fuel_type is None
    assert trip.size is None


def test_trip_by_car_calculation():
    """Test whether trip emissions are calculated"""
    emissions = Trip(300).by_car().calculate_co2e()
    assert isinstance(emissions, Emissions)
    assert isinstance(emissions.co2e, float)


@pytest.mark.ors
def test_trip_by_car_distance_calculation():
    """Test whether distance is calculated correctly"""
    start = {"locality": "Heidelberg", "country": "Germany"}
    destination = {"locality": "Mannheim", "country": "Germany"}

    distance = Trip(start=start, destination=destination).by_car().calculate_distance()
    assert isinstance(distance, float)
    assert distance == pytest.approx(31, 1)


@pytest.mark.ors
def test_trip_by_car_distance_calculation_2():
    """Test whether distance is calculated correctly"""
    start = {"locality": "Heidelberg", "country": "Germany", "address_type": "address"}
    destination = {
        "locality": "Mannheim",
        "country": "Germany",
        "address_type": "address",
    }

    distance = Trip(start=start, destination=destination).by_car().calculate_distance()
    assert isinstance(distance, float)
    assert distance == pytest.approx(31, 1)


def test_instantiate_trip_by_train():
    """Test whether class is instantiated correctly"""
    trip = Trip(300).by_train()
    assert trip.transportation_mode == TransportationMode.TRAIN


def test_trip_by_train_calculation():
    """Test whether trip emissions are calculated"""
    emissions = Trip(300).by_train().calculate_co2e()
    assert isinstance(emissions, Emissions)
    assert isinstance(emissions.co2e, float)


def test_trip_by_train_distance_calculation():
    """Test whether distance is calculated"""
    start = {
        "station_name": "Heidelberg Hbf",
        "country": "DE",
        "address_type": "trainstation",
    }
    destination = {
        "station_name": "Mannheim Hbf",
        "country": "DE",
        "address_type": "trainstation",
    }

    distance = (
        Trip(start=start, destination=destination).by_train().calculate_distance()
    )
    assert isinstance(distance, float)


def test_instantiate_trip_by_plane():
    """Test whether class is instantiated correctly"""
    trip = Trip(300).by_plane()
    assert trip.transportation_mode == TransportationMode.PLANE
    assert trip.seating is None


def test_trip_by_plane_calculation():
    """Test whether trip emissions are calculated"""
    emissions = Trip(300).by_plane().calculate_co2e()
    assert isinstance(emissions, Emissions)
    assert isinstance(emissions.co2e, float)


def test_trip_by_plane_distance_calculation():
    """Test whether distance is calculated"""
    start = {"IATA": "FRA", "address_type": "airport"}
    destination = {"IATA": "STR", "address_type": "airport"}

    distance = (
        Trip(start=start, destination=destination).by_plane().calculate_distance()
    )
    assert isinstance(distance, float)


def test_instantiate_trip_by_tram():
    """Test whether class is instantiated correctly"""
    trip = Trip(300).by_tram()
    assert trip.transportation_mode == TransportationMode.TRAM


def test_trip_by_tram_calculation():
    """Test whether trip emissions are calculated"""
    emissions = Trip(300).by_tram().calculate_co2e()
    assert isinstance(emissions, Emissions)
    assert isinstance(emissions.co2e, float)


def test_trip_by_tram_distance_calculation():
    """Test whether distance is calculated"""
    start = {
        "station_name": "Heidelberg Hbf",
        "country": "DE",
        "address_type": "trainstation",
    }
    destination = {
        "station_name": "Mannheim Hbf",
        "country": "DE",
        "address_type": "trainstation",
    }

    distance = Trip(start=start, destination=destination).by_tram().calculate_distance()
    assert isinstance(distance, float)


def test_instanitate_trip_by_ferry():
    """Test whether class is instantiated correctly"""
    trip = Trip(300).by_ferry()
    assert trip.transportation_mode == TransportationMode.FERRY
    assert trip.ferry_class is None


def test_trip_by_ferry_calculation():
    """Test whether trip emissions are calculated"""
    emissions = Trip(300).by_ferry().calculate_co2e()
    assert isinstance(emissions, Emissions)
    assert isinstance(emissions.co2e, float)


def test_trip_by_ferry_distance_calculation():
    """Test whether distance is calculated"""
    start = {"locality": "Hamburg", "country": "DE"}  # --> working
    destination = {"locality": "Cuxhaven", "country": "DE"}  # --> working

    # start = {"address": "Bubendey-Ufer","locality": "Hamburg", "country": "Germany"} #--> not working
    # destination = {"address": "Altona (Fischmarkt)","locality": "Hamburg", "country": "Germany"} #--> not working

    distance = (
        Trip(start=start, destination=destination).by_ferry().calculate_distance()
    )
    assert isinstance(distance, float)


def test_instantiate_trip_by_bus():
    """Test whether class is instantiated correctly"""
    trip = Trip(300).by_bus()
    assert trip.transportation_mode == TransportationMode.BUS
    assert trip.fuel_type is None
    assert trip.size is None
    assert trip.vehicle_range is None


def test_trip_by_bus_calculation():
    """Test whether trip emissions are calculated"""
    emissions = Trip(300).by_bus().calculate_co2e()
    assert isinstance(emissions, Emissions)
    assert isinstance(emissions.co2e, float)


@pytest.mark.ors
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
    assert trip.transportation_mode == TransportationMode.MOTORBIKE
    assert trip.size is None


def test_trip_by_motorbike_calculation():
    """Test whether trip emissions are calculated"""
    emissions = Trip(300).by_motorbike().calculate_co2e()
    assert isinstance(emissions, Emissions)
    assert isinstance(emissions.co2e, float)


@pytest.mark.ors
def test_trip_by_motorbike_distance_calculation():
    """Test whether distance is calculated correctly"""
    start = {"locality": "Heidelberg", "country": "Germany"}
    destination = {"locality": "Mannheim", "country": "Germany"}

    distance = (
        Trip(start=start, destination=destination).by_motorbike().calculate_distance()
    )
    assert isinstance(distance, float)
    assert distance == pytest.approx(31, 1)


def test_instantiate_trip_by_bicycle():
    """Test whether class is instantiated correctly"""
    trip = Trip(300).by_bicycle()
    assert trip.transportation_mode == TransportationMode.BICYCLE


def test_trip_by_bicycle_calculation():
    """Test whether trip emissions are calculated"""
    emissions = Trip(300).by_bicycle().calculate_co2e()
    assert isinstance(emissions, Emissions)
    assert isinstance(emissions.co2e, float)


@pytest.mark.ors
def test_trip_by_bicycle_distance_calculation():
    """Test whether distance is calculated correctly"""
    start = {"locality": "Heidelberg", "country": "Germany"}
    destination = {"locality": "Mannheim", "country": "Germany"}

    distance = (
        Trip(start=start, destination=destination).by_bicycle().calculate_distance()
    )
    assert isinstance(distance, float)
    assert distance == pytest.approx(31, 1)


def test_instantiate_trip_by_pedelec():
    """Test whether class is instantiated"""
    trip = Trip(300).by_pedelec()
    assert trip.transportation_mode == TransportationMode.PEDELEC


def test_trip_by_pedelec_calculation():
    """Test whether trip emissions are calculated"""
    emissions = Trip(300).by_pedelec().calculate_co2e()
    assert isinstance(emissions, Emissions)
    assert isinstance(emissions.co2e, float)


@pytest.mark.ors
def test_trip_by_pedelec_distance_calculation():
    """Test whether distance is calculated correctly"""
    start = {"locality": "Heidelberg", "country": "Germany"}
    destination = {"locality": "Mannheim", "country": "Germany"}

    distance = (
        Trip(start=start, destination=destination).by_pedelec().calculate_distance()
    )
    assert isinstance(distance, float)
    assert distance == pytest.approx(31, 1)


def test_trip_by_custom_calculation():
    """Test whether custom trip emissions are calculated"""
    emissions = Trip(300).by_custom(emission_factor=0.1).calculate_co2e()
    assert isinstance(emissions, Emissions)
    assert isinstance(emissions.co2e, float)


def test_trip_by_custom_no_emission_factor():
    """
    Test whether custom trip calculation raises an error
    if no emission factor is provided
    """
    with pytest.raises(TypeError):
        Trip(300).by_custom().calculate_co2e()


def test_trip_by_custom_distance_calculation():
    """Test whether distance is calculated correctly"""
    start = {"locality": "Heidelberg", "country": "Germany"}
    destination = {"locality": "Mannheim", "country": "Germany"}

    distance = (
        Trip(start=start, destination=destination)
        .by_custom(transportation_mode="car", emission_factor=0.1)
        .calculate_distance()
    )
    assert isinstance(distance, float)
    assert distance == pytest.approx(31, 1)


def test_trip_by_custom_co2e_train_to_airport_by_car():
    """Test a travel by car from Trainstation to airport"""
    start = {
        "station_name": "Heidelberg Hbf",
        "country": "DE",
        "address_type": "trainstation",
    }
    destination = {"IATA": "STR", "address_type": "airport"}

    trip = (
        Trip(start=start, destination=destination)
        .by_custom(transportation_mode="car", emission_factor=0.1)
        .calculate_co2e()
    )


def test_geocoding_structured_single_input():
    """Test geocoding with minimal structured input"""
    start = {
        "locality": "Heidelberg",
        "address_type": "address",
    }
    destination = {
        "locality": "Hamburg",
        "address_type": "address",
    }

    distance = (
        Trip(start=start, destination=destination).by_train().calculate_distance()
    )

    assert distance == pytest.approx(569.7402306228078, 1)


def test_geocoding_structured_single_input_str():
    """Test geocoding with str as input"""
    start = "Heidelberg"

    destination = "Hamburg"

    distance = (
        Trip(start=start, destination=destination).by_train().calculate_distance()
    )

    assert distance == pytest.approx(569.7402306228078, 1)
