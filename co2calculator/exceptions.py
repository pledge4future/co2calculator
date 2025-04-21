#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Exceptions for the co2calculator package"""


class EmissionFactorNotFound(Exception):
    def __init__(self, message):
        """Init"""
        self.message = message


class ConversionFactorNotFound(Exception):
    def __init__(self, message):
        """Init"""
        self.message = message


# Module's exceptions
class InvalidSpatialInput(Exception):
    """Raised when consumer inputs invalid spatial information"""
