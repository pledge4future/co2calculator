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


def test_emission_factors_car() -> None:
    """
    Test if a ValidationError is raised if only one parameter is given to find the right emission factor. In this way,
    the user is forced to provide all the necessary parameters to find the right emission factor.
    """
    size = "small"

    with pytest.raises(ValidationError):
        CarEmissionParameters(size=size)
