#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""__description__"""
import pytest

from co2calculator.exceptions import ConversionFactorNotFound
from co2calculator.parameters import *
from co2calculator.enums import *
from co2calculator.reader import Reader


def test_read_emission_factors_ConversionFactorNotFound():

    reader = Reader()
    parameters = {"seating": PlaneSeatingClass.Premium_economy_class,
                  "range": PlaneRange.Short_haul}
    param = PlaneEmissionParameters(**parameters)

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
    assert factor == pytest.approx(expected, 0.3)

