#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Energy classes"""
from co2calculator import (
    CountryCode2,
    CountryCode3,
    calc_co2_electricity,
    ElectricityFuel,
    calc_co2_heating,
)

from typing import Optional


class Energy:
    def __init__(
        self,
        consumption: float,
        fuel_type: Optional[str] = None,
        unit: Optional[str] = None,
        own_share: float = 1.0,
        country_code: Optional[str] = None,
    ):
        """Initialize an Energy object"""
        self.consumption = consumption
        self.fuel_type = fuel_type
        self.unit = unit
        self.own_share = own_share
        self.country_code = country_code

        self.__verify_parameters()

    def __verify_parameters(self):
        """Verifies whether the parameters passed by the user are valid"""
        if self.consumption <= 0:
            raise ValueError("Consumption must be greater than 0")
        if self.fuel_type is not None and not isinstance(self.fuel_type, str):
            raise ValueError("fuel_type must be a string")
        if self.unit is not None and not isinstance(self.unit, str):
            raise ValueError("unit must be a string")
        if not (0 <= self.own_share <= 1):
            raise ValueError("Own share must be between 0 and 1")
        if self.country_code is not None and not isinstance(self.country_code, str):
            raise ValueError("Invalid country code format. Must be a string.")

    def from_electricity(self):
        """Calculate emissions from electricity consumption"""
        return calc_co2_electricity(
            consumption=self.consumption,
            fuel_type=self.fuel_type,
            country_code=self.country_code,
            own_share=self.own_share,
        )

    def from_heating(self):
        """Calculate emissions from heating consumption"""
        return calc_co2_heating(
            consumption=self.consumption,
            fuel_type=self.fuel_type,
            unit=self.unit,
            own_share=self.own_share,
        )
