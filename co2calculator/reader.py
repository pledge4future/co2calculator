#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Reader class to retrieve co2 factors from database"""
import warnings
from pathlib import Path
import pandas as pd

from .exceptions import ConversionFactorNotFound

script_path = str(Path(__file__).parent)


class Reader:

    def __init__(self):
        """Init"""
        self.emission_factors = pd.read_csv(f"{script_path}/../data/emission_factors.csv")
        self.conversion_factors = pd.read_csv(
            f"{script_path}/../data/conversion_factors_heating.csv"
        )
        self.detour_factors = pd.read_csv(f"{script_path}/../data/detour.csv")

    def get_emission_factor(self, parameters: dict):
        """
        Returns factors from the database
        :param parameters:
        :type parameters:
        :return:
        :rtype:
        """
        message = "Success"
        selected_factors = self.emission_factors
        for k, v in parameters.items():
            selected_factors_new = selected_factors[selected_factors[k].astype("str") == str(v.value)]
            if len(selected_factors_new) == 0:
                warnings.warn("No suitable conversion factor found in database. Returning average value.")
                continue
            selected_factors = selected_factors_new
        if len(selected_factors) == 0:
            raise ConversionFactorNotFound(f"No suitable conversion factor found in database. Please adapt your query.")
        elif len(selected_factors) > 1:
            raise ConversionFactorNotFound(f"{len(selected_factors)} co2 conversion factors found. Please provide more specific selection criteria.")
        else:
            return selected_factors["co2e"].values[0]



