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
        # Todo: check that co2e is positive, distance is positive, emission_factor is positive
        pass
