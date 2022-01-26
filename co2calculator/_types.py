#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Type definitions for type checking purposes."""

from typing import Union, TypedDict, Tuple, List

Kilometer = float
Kilograms = float
Coordinates = Union[Tuple[float, float], List[float, float]]  # NOTE: double check/test
# Python 3.9: Coordinates = tuple[float, float] | list[float, float]


class TrainStationDict(TypedDict):
    """Dictionary type for geocoding train stations"""

    country: str
    station_name: str


# StructuredLocDict = dict[str, str]
class StructuredLocDict(TypedDict, total=False):
    """Dictionary type for structured geocoding with Pelias"""

    country: str
    region: str
    county: str
    locality: str
    borough: str
    address: str
    neighbourhood: str
