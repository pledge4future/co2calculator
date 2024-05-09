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
