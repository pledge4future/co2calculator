#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Energy classes"""
from typing import Optional
import pandas as pd

from co2calculator import ConversionFactors

from co2calculator.energy.calculate_energy import (
    calc_co2_electricity,
    calc_co2_heating,
)
from co2calculator.api.emission import EnergyEmissions
from co2calculator.energy.calculate_energy import conversion_factors


class Energy:
    def __init__(
        self,
    ):
        """Initialize an Energy object"""

    def from_electricity(
        self,
        consumption: float,
        country_code: str,
        fuel_type: Optional[str] = None,
        own_share: float = 1.0,
    ):
        """Calculate emissions from electricity consumption

        :param consumption: energy consumption
        :param country_code: 2-letter ISO country code
        :type country_code: str
        :param fuel_type: energy mix used for electricity (see ElectricityFuel in constants.py)
        :param own_share: the research group's approximate share of the total electricity energy consumption. Value range 0 to 1.
        """
        if consumption <= 0:
            raise ValueError("Consumption must be greater than 0")
        if country_code is not None and not isinstance(country_code, str):
            raise ValueError("Invalid country code format. Must be a string.")
        if fuel_type is not None and not isinstance(fuel_type, str):
            raise ValueError("fuel_type must be a string")
        if not (0 <= own_share <= 1):
            raise ValueError("Own share must be between 0 and 1")

        return _EnergyFromElectricity(
            consumption=consumption,
            own_share=own_share,
            fuel_type=fuel_type,
            country_code=country_code,
        )

    def from_heating(
        self,
        consumption: float,
        in_kwh: bool = False,
        fuel_type: Optional[str] = None,
        own_share: float = 1.0,
    ):
        """Calculate emissions from heating consumption

        :param consumption: energy consumption
        :param in_kwh: if True, consumption is in kWh
        :param fuel_type: energy mix used for heating (see HeatingFuel in constants.py)
        :param own_share: the research group's approximate share of the total heating energy consumption. Value range 0 to 1.
        """
        if consumption <= 0:
            raise ValueError("Consumption must be greater than 0")
        if fuel_type is None and not in_kwh:
            raise ValueError("Please provide a fuel type or set in_kwh to True")
        if fuel_type is not None and not isinstance(fuel_type, str):
            raise ValueError("fuel_type must be a string")
        if not (0 <= own_share <= 1):
            raise ValueError("Own share must be between 0 and 1")

        return _EnergyFromHeating(
            consumption=consumption,
            fuel_type=fuel_type,
            own_share=own_share,
            in_kwh=in_kwh,
        )


class _EnergyFromElectricity(Energy):
    """This is a hidden class which handles emissions from electricity.

    :param consumption: energy consumption
    :param fuel_type: energy mix used for electricity (see ElectricityFuel in constants.py)
    :param own_share: the research group's approximate share of the total electricity energy consumption. Value range 0 to 1.
    :param country_code: 2-letter ISO country code
    :type consumption: float
    :type fuel_type: str
    :type own_share: float
    :type country_code: str
    """

    def __init__(
        self,
        consumption: float,
        fuel_type: Optional[str] = None,
        own_share: float = None,
        country_code: str = "DE",
    ):
        # initialize
        super(_EnergyFromElectricity, self).__init__()
        self.consumption = consumption
        self.fuel_type = fuel_type
        self.own_share = own_share
        self.country_code = country_code

    def calculate_co2e(self):
        """Calculate the CO2e emissions from electricity.

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
    """This is a hidden class which handles emissions from heating.

    :param consumption: energy consumption
    :param fuel_type: energy mix used for heating (see HeatingFuel in constants.py)
    :param own_share: the research group's approximate share of the total heating energy consumption. Value range 0 to 1.
    :param in_kwh: if True, consumption is in kWh
    :type consumption: float
    :type fuel_type: str
    :type own_share: float
    :type in_kwh: bool
    """

    def __init__(
        self,
        consumption: float,
        fuel_type: Optional[str] = None,
        own_share: float = None,
        in_kwh: bool = False,
    ):
        # initialize
        super(_EnergyFromHeating, self).__init__()
        self.consumption = consumption
        self.fuel_type = fuel_type
        self.own_share = own_share
        self.in_kwh = in_kwh

    def calculate_co2e(self):
        """Calculate the CO2e emissions from heating.

        :return: EnergyEmissions object
        """

        # Calculate emissions
        options = {
            "fuel_type": self.fuel_type,
            "own_share": self.own_share,
            "in_kwh": self.in_kwh,
        }
        # Filter out items where value is None
        options = {k: v for k, v in options.items() if v is not None}

        co2e, emission_factor, emission_parameters = calc_co2_heating(
            self.consumption, options=options
        )
        # Get the unit
        if self.in_kwh:
            unit = "kWh"
        else:
            unit = conversion_factors.get_unit()

        # Remove in_kwh from emission_parameters to avoid repetition in output
        delattr(emission_parameters, "in_kwh")

        emissions = EnergyEmissions(
            co2e=co2e,
            emission_factor=emission_factor,
            emission_parameters=emission_parameters,
            consumption=self.consumption,
            unit=unit,
        )
        return emissions

    def get_options(self):
        """Return fuel type options and their corresponding units as a table."""

        options = {
            "fuel_type": [
                "oil",
                "liquid gas",
                "coal",
                "wood pellets",
                "wood chips",
                "gas",
            ],
            "unit": ["l", "kg", "kg", "kg", "kg", "m^3"],
        }
        return pd.DataFrame(options)
