#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Trip classes"""
from co2calculator import CountryCode2, CountryCode3
from co2calculator.api.emission import Emissions
from co2calculator.distances import get_distance, create_distance_request
from co2calculator.mobility.calculate_mobility import (
    calc_co2_car,
    calc_co2_train,
    calc_co2_plane,
    calc_co2_motorbike,
    calc_co2_tram,
    calc_co2_ferry,
    calc_co2_bus,
    calc_co2_bicycle,
    calc_co2_pedelec,
)
from co2calculator.constants import HeatingFuel, Unit


class Energy:
    def __init__(
        self,
        consumption: float,
        fuel_type: HeatingFuel,
        unit: Unit = None,
        own_share: float = 1.0,
    ):
        """Initialize a heating object"""
        self.__verify_parameters(consumption, fuel_type, unit, own_share)
        self.consumption = consumption
        self.fuel_type = fuel_type
        self.unit = unit
        self.own_share = own_share

    def __verify_parameters(
        self, consumption: float, fuel_type: HeatingFuel, unit: Unit, own_share: float
    ):
        """Verifies whether the parameters passed by the user are valid"""
        pass

    def from_electricity(self):
        """Calculate emissions from electricity"""
        pass

    def from_heating(self):
        """Calculate emissions from heating"""
        pass
