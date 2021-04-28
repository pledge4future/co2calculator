#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test heating calculations
"""

import os

from co2calculator import calc_co2_heating, calc_co2_electricity

script_path = os.path.dirname(os.path.realpath(__file__))


def test_heating_woodchips():
    """
    Test co2e calculation for heating: woodchips
    :return:
    """
    # Given parameters
    fuel_type = "woodchips"  # emission factor: 9322 kg/TJ
    consumption = 250
    unit = "kg"  # conversion factor to kWh = 5.4
    # divide by 277777.77777778 to convert from TJ to kWh
    co2e_kg_expected = 43.63

    # Calculate co2e
    co2e = calc_co2_heating(consumption=consumption, unit=unit, fuel_type=fuel_type)

    # Check if expected result matches calculated result
    assert round(co2e, 2) == co2e_kg_expected


def test_electricity():
    """
    Test co2e calculation for electricity
    :return:
    """
    # Given parameters
    fuel_type = "german energy mix"
    consumption_kwh = 10000
    co2e_kg_expected = 3942.65

    # Calculate co2e
    co2e = calc_co2_electricity(consumption=consumption_kwh, fuel_type=fuel_type)

    # Check if expected result matches calculated result
    assert round(co2e, 2) == co2e_kg_expected