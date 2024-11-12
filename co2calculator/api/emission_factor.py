#!/usr/bin/env python
# coding: utf-8
"""Emission factor class"""

from dataclasses import dataclass


@dataclass
class EmissionFactor:
    """Stores information on emission factors"""

    factor: float
    source: str

    def __post_init__(self):
        """Validate the attribute values"""
        if isinstance(self.factor, (int, float)):
            assert self.factor >= 0, "Emission factor must be positive"
        elif self.factor < 0:
            raise ValueError("Emission factor must be positive")
        pass
