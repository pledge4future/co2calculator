#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Check if values in the csv files are compliant with enums"""

import pytest

from co2calculator import (
    HeatingFuel,
    emission_factors,
    ElectricityFuel,
    Size,
    FlightClass,
    FerryClass,
    FlightRange,
    BusTrainRange,
)


@pytest.mark.parametrize(
    "column_name,enum,emission_category,subcategory",
    [
        pytest.param(
            "fuel_type", HeatingFuel, "heating", None, id="fuel_type: 'HeatingFuel'"
        ),
        pytest.param(
            "fuel_type",
            ElectricityFuel,
            "electricity",
            None,
            id="fuel_type: 'ElectricityFuel'",
        ),
        pytest.param("size", Size, "transport", None, id="Size: 'Size'"),
        pytest.param(
            "range", BusTrainRange, "transport", "bus", id="range: 'BusTrainRange'"
        ),
        pytest.param(
            "range", FlightRange, "transport", "plane", id="range: 'FlightRange'"
        ),
        pytest.param(
            "seating", FlightClass, "transport", "plane", id="seating: 'FlightClass'"
        ),
        pytest.param(
            "seating", FerryClass, "transport", "ferry", id="fuel_type: 'FerryClass'"
        ),
    ],
)
def test_enums_heating(column_name, enum, emission_category, subcategory):
    """Test whether all values in the csv files are present in the enums"""

    # Get unique values of the size column
    emission_factors_category = emission_factors.databases[emission_category]
    if subcategory:
        emission_factors_subcategory = emission_factors_category.loc[
            emission_factors_category["subcategory"] == subcategory
        ]
        column_values = emission_factors_subcategory[column_name].unique()
    else:
        column_values = emission_factors_category[column_name].unique()

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
        ), f"Column '{column_name}' in emission_factors.csv does not contain value '{item.value}' of enum '{enum}'"
