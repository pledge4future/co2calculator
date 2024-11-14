#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Emission class"""

from dataclasses import dataclass
from pydantic import BaseModel


@dataclass
class Emissions:
    """Class for storing information on emissions"""

    co2e: float
    distance: float
    emission_factor: float
    emission_parameters: BaseModel | dict

    def __post_init__(self):
        """Validate the attribute values"""
        if self.co2e < 0:
            raise ValueError("co2e must be positive")
        elif self.distance < 0:
            raise ValueError("Distance must be positive")
        elif self.emission_factor < 0:
            raise ValueError("Emission factor must be positive")
