#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test pydantic models in parameters.py"""

from pathlib import Path
from co2calculator import TransportationMode
from co2calculator.data_handlers import EmissionFactors
from co2calculator.parameters import (
    PlaneEmissionParameters,
    HeatingEmissionParameters,
    ElectricityEmissionParameters,
    CarEmissionParameters,
)
from co2calculator import emission_factors
import pytest
from pydantic import ValidationError


def test_planeemissionparameter_raise_validation_error():
    """Tests that PlaneEmissionParameters raises a validation error when an invalid seating is provided."""
    with pytest.raises(ValidationError):
        PlaneEmissionParameters(subcategory=TransportationMode.PLANE, seating="INVALID")


def test_emission_factors_heating() -> None:
    """Test emission factors for heating"""
    # fuel_type = HeatingFuel.COAL
    fuel_type = "coal"

    params = HeatingEmissionParameters(fuel_type=fuel_type)
    # Get the co2 factor
    co2e = emission_factors.get(params.dict())

    assert isinstance(co2e, float)


def test_emission_factors_electricity() -> None:
    """Test emission factors for heating"""
    fuel_type = "production fuel mix"
    country_code = "DE"

    params = ElectricityEmissionParameters(
        fuel_type=fuel_type, country_code=country_code
    )

    # Get the co2 factor
    co2e = emission_factors.get(params.dict())

    assert isinstance(co2e, float)


@pytest.mark.skip(
    reason="No emission factor available, if defaults are used in combination with this user input"
    "We first need to decide how to handle this"
)
def test_emission_factors_car() -> None:
    """Test emission factors for car"""
    size = "small"
    co2e_expected = 0.1

    params = CarEmissionParameters(size=size)

    # Get the co2 factor
    co2e = emission_factors.get(params.dict())

    assert co2e == co2e_expected
