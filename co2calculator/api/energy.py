#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Energy classes"""
from typing import Optional
from co2calculator.energy.calculate_energy import (
    calc_co2_electricity,
    calc_co2_heating,
)
from co2calculator.api.emission import EnergyEmissions


class Energy:
    def __init__(
        self,
        consumption: float,
        fuel_type: Optional[str] = None,
        own_share: float = 1.0,
    ):
        """Initialize an Energy object

        :param consumption: energy consumption
        :param fuel_type: energy (mix) used for electricity/heating
        (see HeatingFuel and ElectricityFuel in constants.py)
        :param own_share: the research group's approximate share of the
        total electricity energy consumption
        :type consumption: float
        :type fuel_type: str
        :type own_share: float
        """
        self.consumption = consumption
        self.fuel_type = fuel_type
        self.own_share = own_share

        self.__verify_parameters()

    def __verify_parameters(self):
        """Verifies whether the parameters passed by the user are valid"""
        if self.consumption <= 0:
            raise ValueError("Consumption must be greater than 0")
        if self.fuel_type is not None and not isinstance(self.fuel_type, str):
            raise ValueError("fuel_type must be a string")
        if not (0 <= self.own_share <= 1):
            raise ValueError("Own share must be between 0 and 1")

    def from_electricity(self, country_code: str):
        """Calculate emissions from electricity consumption

        :param country_code: 2-letter ISO country code
        :type country_code: str
        """
        if country_code is not None and not isinstance(country_code, str):
            raise ValueError("Invalid country code format. Must be a string.")
        return _EnergyFromElectricity(
            consumption=self.consumption,
            own_share=self.own_share,
            fuel_type=self.fuel_type,
            country_code=country_code,
        )

    def from_heating(self, unit: str):
        """Calculate emissions from heating consumption

        :param unit: unit of measurement for heating consumption
        :type unit: str
        """
        if unit is not None and not isinstance(unit, str):
            raise ValueError("unit must be a string")
        return _EnergyFromHeating(
            consumption=self.consumption,
            fuel_type=self.fuel_type,
            own_share=self.own_share,
            unit=unit,
        )


class _EnergyFromElectricity(Energy):
    """
    This is a hidden class which handles emissions from electricity.
    """

    def __init__(
        self,
        consumption: float,
        fuel_type: Optional[str] = None,
        own_share: float = 1.0,
        country_code: str = "DE",
    ):
        # initialize
        super(_EnergyFromElectricity, self).__init__(
            consumption=consumption, fuel_type=fuel_type, own_share=own_share
        )
        self.country_code = country_code

    def calculate_co2e(self):
        """
        Calculate the CO2e emissions for electricity.
        :return: EnergyEmissions object
        """

        # Calculate emissions
        options = {
            "fuel_type": self.fuel_type,
            "own_share": self.own_share,
            "country_code": self.country_code,
        }

        # Filter out items where value is None
        options = {k: v for k, v in options.items() if v is not None}

        co2e, emission_factor, emission_parameters = calc_co2_electricity(
            consumption=self.consumption, options=options
        )
        emissions = EnergyEmissions(
            co2e=co2e,
            emission_factor=emission_factor,
            emission_parameters=emission_parameters,
            consumption=self.consumption,
        )
        return emissions


class _EnergyFromHeating(Energy):
    """
    This is a hidden class which handles emissions from heating.
    """

    def __init__(
        self,
        consumption: float,
        fuel_type: Optional[str] = None,
        own_share: float = 1.0,
        unit: str = "kwh",
    ):
        # initialize
        super(_EnergyFromHeating, self).__init__(
            consumption=consumption, fuel_type=fuel_type, own_share=own_share
        )
        self.unit = unit

    def calculate_co2e(self):
        """
        Calculate the CO2e emissions for heating.
        :return: EnergyEmissions object
        """

        # Calculate emissions
        options = {
            "fuel_type": self.fuel_type,
            "own_share": self.own_share,
            "unit": self.unit,
        }

        # Filter out items where value is None
        options = {k: v for k, v in options.items() if v is not None}

        co2e, emission_factor, emission_parameters = calc_co2_heating(
            self.consumption, options=options
        )
        emissions = EnergyEmissions(
            co2e=co2e,
            emission_factor=emission_factor,
            emission_parameters=emission_parameters,
            consumption=self.consumption,
        )
        return emissions
