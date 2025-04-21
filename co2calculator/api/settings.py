#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Base Settings"""
import os


def set_ors_apikey(apikey: str):
    """Set the ORS API key as an environment variable.
    :param apikey: API key for openrouteservice
    """
    # Set environment variable ORS_API_KEY to value of apikey
    os.environ["ORS_API_KEY"] = apikey
