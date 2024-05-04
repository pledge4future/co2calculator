#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Reader class to retrieve co2 factors from database"""
import warnings
from pathlib import Path
import pandas as pd
from .exceptions import ConversionFactorNotFound

script_path = str(Path(__file__).parent)


class EmissionFactors:
    def __init__(self):
        """Init"""
        self.emission_factors = pd.read_csv(
            f"{script_path}/../data/emission_factors.csv"
        )

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
            if v is None:
                continue
            selected_factors_new = selected_factors[
                selected_factors[k].astype("str") == str(v.value)
            ]
            selected_factors = selected_factors_new
            if selected_factors_new.empty:
                raise ConversionFactorNotFound(
                    "No suitable conversion factor found in database. Please adapt your query."
                )

        if len(selected_factors) > 1:
            raise ConversionFactorNotFound(
                f"{len(selected_factors)} co2 conversion factors found. Please provide more specific selection criteria."
            )
        else:
            return selected_factors["co2e"].values[0]


class Airports:
    pass


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
