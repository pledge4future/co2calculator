#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test pydantic models in parameters.py"""

from co2calculator import TransportationMode
from co2calculator.parameters import PlaneEmissionParameters
import pytest
from pydantic import ValidationError


def test_planeemissionparameter_raise_validation_error():
    """Tests that PlaneEmissionParameters raises a validation error when an invalid seating is provided."""
    with pytest.raises(ValidationError):
        PlaneEmissionParameters(subcategory=TransportationMode.PLANE, seating="INVALID")
