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
        # todo: check that factor is positive
        pass
