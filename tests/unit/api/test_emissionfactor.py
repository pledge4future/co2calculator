# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Unit tests for emission factor class"""

import pytest
from co2calculator.api.emission_factor import EmissionFactor


def test_emissionfactor():
    """Test if EmissionFactor class is instantiated correctly"""
    emission_factor = EmissionFactor(factor=2.5)
    assert emission_factor.factor == 2.5


def test_emissionfactor_postinit():
    """Test if EmissionFactor class is instantiated correctly"""
    with pytest.raises(ValueError):
        EmissionFactor(factor=-5)
    with pytest.raises(TypeError):
        EmissionFactor(factor="5")
