#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Trip classes"""


from dataclasses import dataclass
from pydantic import BaseModel

from co2calculator.api.emission import Emissions
from co2calculator.mobility.calculate_mobility import calc_co2_car
from co2calculator.constants import CarFuel, Size, TransportationMode


class Trip:
    def __init__(self, distance=None, start=None, end=None):
        """Initialize a trip object"""
        self.__verify_parameters(distance, start, end)
        self.distance = distance
        self.start = start
        self.end = end

    def __verify_parameters(self, distance, start, end):
        """Verifies whether the parameters passed by the user are valid"""
        assert distance > 0, "Distance must be greater than 0"
        if distance is None:
            assert (
                start is not None and end is not None
            ), "If distance is given, start and end must be None."
        elif distance is not None:
            assert (
                start is None and end is None
            ), "If distance is not given, start and end must be given."

    def by_car(self, fuel_type: str = None, size: str = None):
        return _TripByCar(
            fuel_type=fuel_type,
            size=size,
            distance=self.distance,
            start=self.start,
            end=self.end,
        )


class _TripByCar(Trip):
    """This is a hidden class which handles car trips. It is not meant to be used by the user directly, instead it is only called from other classes of the module."""

    transport_mode = TransportationMode.CAR

    def __init__(
        self,
        fuel_type: str = None,
        size: str = None,
        distance=None,
        start=None,
        end=None,
    ):
        """Initialize a car trip"""
        super(_TripByCar, self).__init__(distance=distance, start=start, end=end)
        self.fuel_type = fuel_type
        self.size = size

    def calculate_co2e(self):
        """
        Calculate the CO2e emissions for a car trip

        :param fuel_type: The fuel type of the car
        :param size: The size of the car
        :return: Emissions object
        """

        if self.distance is None:
            distance = self.calculate_distance()

        # Calculate emissions
        options = {"fuel_type": self.fuel_type, "size": self.size}
        # Filter out items where value is None
        options = {k: v for k, v in options.items() if v is not None}

        co2e, emission_factor, emission_parameters = calc_co2_car(
            self.distance, options=options
        )
        emissions = Emissions(
            co2e=co2e,
            distance=self.distance,
            emission_factor=emission_factor,
            emission_parameters=emission_parameters,
        )
        return emissions

    def calculate_distance(self):
        # TODO: Implement distance calculation
        pass

    def get_options(self):
        # TODO: Implement options retrieval
        pass
