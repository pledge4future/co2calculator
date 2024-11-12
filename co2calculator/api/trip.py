#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Trip classes"""

from co2calculator.api.emission import Emissions
from co2calculator.distances import get_distance, create_distance_request
from co2calculator.mobility.calculate_mobility import calc_co2_car, calc_co2_train
from co2calculator.constants import CarFuel, Size, TransportationMode


class Trip:
    def __init__(
        self, distance: float = None, start: str = None, destination: str = None
    ):
        """Initialize a trip object"""
        self.__verify_parameters(distance, start, destination)
        self.distance = distance
        self.start = start
        self.destination = destination

    def __verify_parameters(self, distance: float, start: str, destination: str):
        """Verifies whether the parameters passed by the user are valid"""
        if distance is not None:
            assert isinstance(distance, (int, float)), "Distance must be a number"
            assert distance > 0, "Distance must be greater than 0"
            assert (
                start is None and destination is None
            ), "If distance is not given, start and destination must be given."
        else:
            assert (
                start is not None and destination is not None
            ), "If distance is given, start and destination must be None."

    def by_car(self, fuel_type: str = None, size: str = None):
        return _TripByCar(
            fuel_type=fuel_type,
            size=size,
            distance=self.distance,
            start=self.start,
            destination=self.destination,
        )

    def by_train(self, country_code: str = "global"):
        return _TripByTrain(
            country_code=country_code,
            distance=self.distance,
            start=self.start,
            destination=self.destination,
        )


class _TripByCar(Trip):
    """This is a hidden class which handles car trips."""

    transport_mode = TransportationMode.CAR

    def __init__(
        self,
        fuel_type: str = None,
        size: str = None,
        distance: float = None,
        start: dict | str = None,
        destination: dict | str = None,
    ):
        """Initialize a car trip"""
        super(_TripByCar, self).__init__(
            distance=distance, start=start, destination=destination
        )
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
            self.calculate_distance()

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
        """Calculates travelled get_distance"""
        request = create_distance_request(
            transportation_mode=self.transport_mode,
            start=self.start,
            destination=self.destination,
        )
        self.distance = get_distance(request)
        return self.distance

    def get_options(self):
        # TODO: Implement options retrieval
        pass


class _TripByTrain(Trip):
    """This is a hidden class which handles car trips."""

    transport_mode = TransportationMode.TRAIN

    def __init__(
        self,
        distance: float = None,
        start: dict | str = None,
        destination: dict | str = None,
        country_code: str = None,
    ):
        """Initialize a car trip"""
        super(_TripByTrain, self).__init__(
            distance=distance, start=start, destination=destination
        )
        self.country_code = country_code

    def calculate_co2e(self):
        """
        Calculate the CO2e emissions for a car trip

        :param fuel_type: The fuel type of the car
        :param size: The size of the car
        :return: Emissions object
        """
        if self.distance is None:
            self.calculate_distance()

        # Calculate emissions
        options = {"country_code": self.country_code}
        # Filter out items where value is None
        options = {k: v for k, v in options.items() if v is not None}

        co2e, emission_factor, emission_parameters = calc_co2_train(
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
        """Calculates travelled get_distance"""
        request = create_distance_request(
            transportation_mode=self.transport_mode,
            start=self.start,
            destination=self.destination,
        )
        self.distance = get_distance(request)
        return self.distance

    def get_options(self):
        # TODO: Implement options retrieval
        pass
