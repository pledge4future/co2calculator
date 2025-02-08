#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for Energy class"""
from co2calculator.api.energy import Energy
from co2calculator.api.emission import Emissions


def test_instantiate_energy():
    """Test whether class is instantiated correctly"""
    energy = Energy(consumption=300)
    assert isinstance(energy, Energy)
    assert energy.consumption == 300
    assert energy.fuel_type is None
    assert energy.own_share == 1.0


def test_calculation_electricity():
    """Test whether electricity emissions are calculated correctly"""
    energy = (
        Energy(consumption=300).from_electricity(country_code="DE").calculate_co2e()
    )
    assert isinstance(energy, Emissions)
    assert isinstance(energy.co2e, float)


def test_calculation_heating():
    """Test whether heating emissions are calculated correctly"""
    energy = (
        Energy(consumption=300, fuel_type="gas")
        .from_heating(unit="m^3")
        .calculate_co2e()
    )
    assert isinstance(energy, Emissions)
    assert isinstance(energy.co2e, float)
