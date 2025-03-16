#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for Energy class"""
import pytest

from co2calculator.api.energy import Energy
from co2calculator.api.emission import Emissions


def test_instantiate_energy():
    """Test whether class is instantiated correctly"""
    energy = Energy()
    assert isinstance(energy, Energy)


def test_calculation_electricity():
    """Test whether electricity emissions are calculated correctly"""
    energy = (
        Energy().from_electricity(consumption=300, country_code="DE").calculate_co2e()
    )
    assert isinstance(energy, Emissions)
    assert isinstance(energy.co2e, float)


def test_calculation_electricity_with_share():
    """Test whether electricity emissions are calculated correctly"""
    energy_inst = Energy().from_electricity(
        consumption=300, own_share=0.5, country_code="DE"
    )
    assert energy_inst.own_share == 0.5
    energy = energy_inst.calculate_co2e()
    assert isinstance(energy, Emissions)
    assert isinstance(energy.co2e, float)


def test_calculation_heating():
    """Test whether heating emissions are calculated correctly"""
    energy = Energy().from_heating(consumption=300, fuel_type="gas").calculate_co2e()
    assert isinstance(energy, Emissions)
    assert isinstance(energy.co2e, float)


def test_calculation_heating_with_share():
    """Test whether heating emissions are calculated correctly"""
    energy_inst = Energy().from_heating(consumption=300, fuel_type="gas", own_share=0.5)
    assert energy_inst.own_share == 0.5
    energy = energy_inst.calculate_co2e()
    assert isinstance(energy, Emissions)
    assert isinstance(energy.co2e, float)


def test_calculation_heating_pellets():
    """Test whether heating emissions are calculated correctly"""
    energy = (
        Energy()
        .from_heating(consumption=300, fuel_type="wood pellets")
        .calculate_co2e()
    )
    assert isinstance(energy, Emissions)
    assert energy.co2e == pytest.approx(17.3988, rel=0.01)


def test_calculation_heating_in_kwh():
    """Test whether heating emissions are calculated correctly"""
    energy = (
        Energy()
        .from_heating(consumption=300, fuel_type="gas", in_kwh=True)
        .calculate_co2e()
    )
    assert isinstance(energy, Emissions)
    assert energy.co2e == pytest.approx(54.0, rel=0.01)
