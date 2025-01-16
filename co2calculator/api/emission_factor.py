#!/usr/bin/env python
# coding: utf-8
"""Emission factor class"""

from dataclasses import dataclass


@dataclass
class EmissionFactor:
    """Stores information on emission factors"""

    factor: float
    source: str = None

    def __post_init__(self):
        """Validate the attribute values"""
        if not isinstance(self.factor, (int, float)):
            raise TypeError("Emission factor must be a number")
        elif self.factor < 0:
            raise ValueError("Emission factor must be positive")
