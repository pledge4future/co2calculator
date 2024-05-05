#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Check if values in the csv files are compliant with enums"""

import pytest

from co2calculator import HeatingFuel, emission_factors, ElectricityFuel


@pytest.mark.parametrize(
    "column_name,enum,emission_category",
    [
        pytest.param(
            "fuel_type", HeatingFuel, "heating", id="fuel_type: 'HeatingFuel'"
        ),
        pytest.param(
            "fuel_type",
            ElectricityFuel,
            "electricity",
            id="fuel_type: 'ElectricityFuel'",
        ),
    ],
)
def test_enums_heating(column_name, enum, emission_category):
    """Test whether all values in the csv files are present in the enums"""

    # Get unique values of the size column
    column_values = emission_factors.databases[emission_category][column_name].unique()

    # Check if all column values are present in the enum
    for v in column_values:
        # skip is v is nan
        if str(v) == "nan":
            continue
        assert v in (
            item.value for item in enum
        ), f"'{v}' in column '{column_name}' of csv file is not contained in enum '{enum}'."

    # Check if all values in the enum are present in the emission factor csv file
    for item in enum:
        assert (
            item.value in column_values
        ), f"Column '{enum}' in emission_factors.csv does not contain value '{item.value}' of enum 'Size'"
