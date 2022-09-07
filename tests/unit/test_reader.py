#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""__description__"""
import pytest

from co2calculator.exceptions import ConversionFactorNotFound
from co2calculator.parameters import *
from co2calculator.enums import *
from co2calculator.reader import Reader


def test_read_emission_factors_factornotfound():

    reader = Reader()
    parameters = { "fuel_type": TrainFuelType.Electric,
                  "range": TrainRange.Long_distance}
    param = TrainEmissionParameters(**parameters)

    with pytest.raises(ConversionFactorNotFound):
        reader.get_emission_factor(param.dict())


def test_read_emission_factors():

    reader = Reader()
    parameters = {
        "fuel_type": CarFuelType.Electric,
        "size": CarSize.Average
                  }
    expected = 0.05728

    param = CarEmissionParameters(**parameters)
    factor = reader.get_emission_factor(param.dict())
    assert factor == expected


def test_read_emission_factors_error():
    reader = Reader()
    parameters = {
        "fuel_type": CarFuelType.Electric,
    }

    param = CarEmissionParameters(**parameters)
    with pytest.raises(ConversionFactorNotFound):
        factor = reader.get_emission_factor(param.dict())
