#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test enums"""

from co2calculator import HeatingFuel


def test_heatingfuel():
    """Test if HeatingFuel enum returns the same value as in the csv file"""
    assert HeatingFuel.OIL.value == "oil"
