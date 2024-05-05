#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test data handlers"""

from co2calculator.data_handlers import EmissionFactors
import pandas as pd


def test_load_emission_factors():
    """Test if the emission factors are loaded correctly"""
    emission_factors = EmissionFactors()
    assert isinstance(emission_factors.heating, pd.DataFrame)
    assert isinstance(emission_factors.electricity, pd.DataFrame)
    assert isinstance(emission_factors.transport, pd.DataFrame)
