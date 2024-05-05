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
)
import pytest
from pydantic import ValidationError


test_data_dir = str(Path(__file__).parent.parent)


@pytest.fixture
def emission_factors_test():
    return EmissionFactors(data_dir=test_data_dir)


def test_planeemissionparameter_raise_validation_error():
    """Tests that PlaneEmissionParameters raises a validation error when an invalid seating is provided."""
    with pytest.raises(ValidationError):
        PlaneEmissionParameters(subcategory=TransportationMode.PLANE, seating="INVALID")


def test_emission_factors_heating(emission_factors_test) -> None:
    """Test emission factors for heating"""
    # fuel_type = HeatingFuel.COAL
    fuel_type = "coal"
    co2e_expected = 0.35

    params = HeatingEmissionParameters(fuel_type=fuel_type)

    # Get the co2 factor
    co2e = emission_factors_test.get(params.dict())

    assert co2e == co2e_expected


def test_emission_factors_electricity(emission_factors_test) -> None:
    """Test emission factors for heating"""
    fuel_type = "production fuel mix"
    country_code = "DE"
    co2e_expected = 0.44912

    params = ElectricityEmissionParameters(
        fuel_type=fuel_type, country_code=country_code
    )

    # Get the co2 factor
    co2e = emission_factors_test.get(params.dict())

    assert co2e == co2e_expected


def test_emission_factors_bus():
    pass
