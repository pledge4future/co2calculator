#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Emission class"""

from dataclasses import dataclass
from typing import Optional

from pydantic import BaseModel


@dataclass
class Emissions:
    """Class for storing information on emissions"""

    co2e: float
    emission_factor: float
    emission_parameters: BaseModel | dict

    def __post_init__(self):
        """Validate the attribute values"""
        if self.co2e < 0:
            raise ValueError("co2e must be positive")
        elif self.emission_factor < 0:
            raise ValueError("Emission factor must be positive")


@dataclass
class EnergyEmissions(Emissions):
    """Class for storing information on energy emissions"""

    consumption: float
    unit: str = "kWh"

    def __post_init__(self):
        """Validate the attribute values"""
        super().__post_init__()
        if self.consumption < 0:
            raise ValueError("Consumption must be >= 0")


@dataclass
class TransportEmissions(Emissions):
    """Class for storing information on transport emissions"""

    distance: float

    def __post_init__(self):
        """Validate the attribute values"""
        super().__post_init__()
        if self.distance < 0:
            raise ValueError("Distance must be >= 0")
