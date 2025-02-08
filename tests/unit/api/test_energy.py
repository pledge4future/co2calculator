#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for Energy class"""
from co2calculator.api.energy import Energy


def test_instantiate_energy():
    """Test whether class is instantiated correctly"""
    energy = Energy(consumption=300)
    assert isinstance(energy, Energy)
    assert energy.consumption == 300
    assert energy.fuel_type is None
    assert energy.own_share == 1.0


def test_calculation_electricity():
    """Test whether electricity emissions are calculated correctly"""
    energy = Energy(consumption=300).from_electricity(country_code="DE")
    assert isinstance(energy, tuple)
    assert isinstance(energy[0], float)


def test_calculation_heating():
    """Test whether heating emissions are calculated correctly"""
    energy = Energy(consumption=300, fuel_type="gas").from_heating(unit="m^3")
    assert isinstance(energy, tuple)
    assert isinstance(energy[0], float)
