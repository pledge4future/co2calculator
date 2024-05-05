#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Data handler class to handle and validate emission factors from csv file"""

from pathlib import Path
import pandas as pd
from .exceptions import EmissionFactorNotFound, ConversionFactorNotFound

script_path = str(Path(__file__).parent)


class EmissionFactors:
    def __init__(self):
        """Init"""
        self.emission_factors = pd.read_csv(
            f"{script_path}/../data/emission_factors.csv"
        )
        self.column_names = self.emission_factors.columns

    def get(self, parameters: dict):
        """
        Returns factors from the database
        :param parameters:
        :type parameters:
        :return:
        :rtype:
        """
        selected_factors = self.emission_factors

        for k, v in parameters.items():
            # TODO: shortterm hack to make it work until occupancy is removed from emission factors
            if not isinstance(v, int):
                v = str(v.value)
            if v is None or k not in self.column_names:
                continue

            selected_factors_new = selected_factors[selected_factors[k] == v]
            selected_factors = selected_factors_new
            if selected_factors_new.empty:
                raise EmissionFactorNotFound(
                    "No suitable emission factor found in database. Please adapt your query."
                )

        if len(selected_factors) > 1:
            raise EmissionFactorNotFound(
                f"{len(selected_factors)} emission factors found. Please provide more specific selection criteria."
            )
        else:
            return selected_factors["co2e"].values[0]


class Airports:
    def __init__(self):
        """Init"""
        self.airports = pd.read_csv(
            "https://davidmegginson.github.io/ourairports-data/airports.csv"
        )


class DetourFactors:
    def __init__(self):
        """Init"""
        self.detour_factors = pd.read_csv(f"{script_path}/../data/detour.csv")


class ConversionFactors:
    def __init__(self):
        """Init"""
        self.conversion_factors = pd.read_csv(
            f"{script_path}/../data/conversion_factors_heating.csv"
        )

    def get(self, fuel_type, unit):
        """
        Returns factors from the database
        :param parameters:
        :type parameters:
        :return:
        :rtype:
        """
        selected_factors = self.conversion_factors.query(
            f'fuel_type=="{fuel_type}" & unit=="{unit}"'
        )
        if selected_factors.empty:
            raise ConversionFactorNotFound(
                "No suitable conversion factor found in database. Please adapt your query."
            )
        else:
            return selected_factors["conversion_value"].values[0]
