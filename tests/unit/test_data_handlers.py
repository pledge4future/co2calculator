#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test data handlers"""

from pathlib import Path
import pytest
from co2calculator.data_handlers import EmissionFactors
from co2calculator.parameters import HeatingEmissionParameters
import pandas as pd


test_data_dir = str(Path(__file__).parent.parent)


@pytest.fixture
def emission_factors_test():
    return EmissionFactors(data_dir=test_data_dir)


def test_load_emission_factors(emission_factors_test):
    """Test if the emission factors are loaded correctly"""
    assert isinstance(emission_factors_test.heating, pd.DataFrame)
    assert isinstance(emission_factors_test.electricity, pd.DataFrame)
    assert isinstance(emission_factors_test.transport, pd.DataFrame)
