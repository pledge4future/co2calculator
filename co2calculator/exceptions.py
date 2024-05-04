#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Exceptions for the co2calculator package"""

__author__ = "Christina Ludwig, GIScience Research Group, Heidelberg University"
__email__ = "christina.ludwig@uni-heidelberg.de"


class ConversionFactorNotFound(Exception):
    def __init__(self, message):
        """Init"""
        self.message = message
