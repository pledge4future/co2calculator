#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""__description__"""

__author__ = "Christina Ludwig, GIScience Research Group, Heidelberg University"
__email__ = "christina.ludwig@uni-heidelberg.de"

from co2calculator import Reader, PlaneRange, TrainFuelType
from co2calculator.parameters import CarEmissionParameters, TrainEmissionParameters, BusEmissionParameters, \
    PlaneEmissionParameters


def test_default_car_parameters():
    par = CarEmissionParameters()
    reader = Reader()
    expected = 0.215

    actual = reader.get_emission_factor(par.dict())
    assert actual == expected


def test_default_train_parameters():
    par = TrainEmissionParameters()
    reader = Reader()
    expected = 0.0329

    actual = reader.get_emission_factor(par.dict())
    assert actual == expected


def test_default_train_fuel_parameters():
    par = TrainEmissionParameters(fuel_type=TrainFuelType.Electric)
    reader = Reader()
    expected = 0.0329

    actual = reader.get_emission_factor(par.dict())
    assert actual == expected


def test_default_bus_parameters():
    par = BusEmissionParameters()
    reader = Reader()
    expected = 0.0394

    actual = reader.get_emission_factor(par.dict())
    assert actual == expected


def test_default_plane_parameters():
    par = PlaneEmissionParameters(range=PlaneRange.Long_haul)
    reader = Reader()
    expected = 0.19085

    actual = reader.get_emission_factor(par.dict())
    assert actual == expected