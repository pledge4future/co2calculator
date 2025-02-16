#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Data handler class to handle and validate emission factors from csv file"""

from pathlib import Path
import pandas as pd
from .exceptions import EmissionFactorNotFound, ConversionFactorNotFound

script_path = str(Path(__file__).parent)


class EmissionFactors:
    def __init__(self, data_dir=script_path):
        """Initialize an EmissionFactors object

        :param data_dir: Path to the directory of the script
        :type data_dir: str
        """
        self.electricity = pd.read_csv(
            f"{data_dir}/data/emission_factors_electricity.csv"
        )
        self.heating = pd.read_csv(f"{data_dir}/data/emission_factors_heating.csv")
        self.transport = pd.read_csv(f"{data_dir}/data/emission_factors_transport.csv")

        self.databases = {
            "electricity": self.electricity,
            "heating": self.heating,
            "transport": self.transport,
        }

    def get(self, parameters: dict):
        """Returns emission factor from the database

        :param parameters: Parameters for searching suitable emission factor
        :type parameters: dict
        :return: co2e factor
        :rtype: float
        """
        assert (
            "category" in parameters
        ), "Please provide a category for the emission factor."
        assert parameters["category"] in [
            "electricity",
            "heating",
            "transport",
        ], "Please provide a valid emission factor category."

        # Search suitable emission factors
        selected_factors = self._search_factors(parameters, parameters["category"])

        if len(selected_factors) == 0:
            raise EmissionFactorNotFound(
                "No suitable emission factor found in database. Please adapt your query."
            )
        elif len(selected_factors) > 1:
            raise EmissionFactorNotFound(
                f"{len(selected_factors)} emission factors found. Please provide more specific selection criteria."
            )
        else:
            return selected_factors["co2e"].values[0]

    def _search_factors(self, parameters, emission_category):
        """Searches for emission factors in the database

        :param parameters: Search parameters
        :type parameters: dict
        :param emission_category: Category of emission factors
        :type emission_category: str
        """
        # Select table for emission category
        candidates = self.databases[emission_category]
        for k, v in parameters.items():
            if isinstance(v, int):
                continue
            if hasattr(v, "value"):
                v = str(v.value)
            if not isinstance(v, str):
                v = str(v)
            if v is None or k not in candidates.columns:
                continue
            new_candidates = candidates[candidates[k] == v]
            if new_candidates.empty:
                return new_candidates
            candidates = new_candidates

        return candidates


class Airports:
    def __init__(self):
        """Initialize Airports class"""
        self.airports = pd.read_csv(
            "https://davidmegginson.github.io/ourairports-data/airports.csv"
        )


class EUTrainStations:
    def __init__(self):
        """Initialize EUTrainStations class"""
        stations = pd.read_csv(
            "https://raw.githubusercontent.com/trainline-eu/stations/master/stations.csv",
            sep=";",
            low_memory=False,
            usecols=[0, 1, 2, 5, 6, 8],
        )
        # remove stations with no coordinates
        self.stations = stations.dropna(subset=["latitude", "longitude"])


class DetourFactors:
    def __init__(self, data_dir=script_path):
        """Initialize detour factor class"""
        self.detour_factors = pd.read_csv(f"{data_dir}/data/detour.csv")


class ConversionFactors:
    def __init__(self, data_dir=script_path):
        """Initialize conversion factor class

        :param data_dir: Path to the directory of the script
        :type data_dir: str
        """
        self.conversion_factors = pd.read_csv(
            f"{data_dir}/data/conversion_factors_heating.csv"
        )

    def get(self, fuel_type):
        """Returns conversion factors from the database

        :param fuel_type: Fuel type to be converted
        :return: Conversion factor from unit to kwh
        :rtype: float
        """
        selected_factors = self.conversion_factors.query(
            f'fuel_type == "{fuel_type.value}"'
        )
        if selected_factors.empty:
            raise ConversionFactorNotFound(
                "No suitable conversion factor found in database. Please adapt your query."
            )
        else:
            return selected_factors["conversion_value"].values[0]
