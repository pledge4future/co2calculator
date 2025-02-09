#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Trip classes"""
from typing import Optional
from co2calculator import CountryCode2, CountryCode3
from co2calculator.api.emission import TransportEmissions
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
from co2calculator.constants import TransportationMode


class Trip:
    def __init__(
        self,
        distance: float = None,
        start: str | dict = None,
        destination: str | dict = None,
        transport_mode: Optional[TransportationMode] = TransportationMode.CAR,
    ):
        """Initialize a trip object"""
        self.__verify_parameters(distance, start, destination)
        self.distance = distance
        self.start = start
        self.destination = destination
        self.transport_mode = transport_mode

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

    def calculate_distance(self):
        """Calculates travelled get_distance"""
        request = create_distance_request(
            transportation_mode=self.transport_mode,
            start=self.start,
            destination=self.destination,
        )
        self.distance = get_distance(request)
        return self.distance

    def by_car(self, fuel_type: str = None, size: str = None, passengers: int = 1):
        return _TripByCar(
            passengers=passengers,
            fuel_type=fuel_type,
            size=size,
            distance=self.distance,
            start=self.start,
            destination=self.destination,
        )

    # TODO: calculate_mobility and constants have 'fuel_type' but TrainEmissionParameters not
    def by_train(self, country_code: str = "global"):
        return _TripByTrain(
            country_code=country_code,
            distance=self.distance,
            start=self.start,
            destination=self.destination,
        )

    def by_plane(self, seating: str = None):
        return _TripByPlane(
            seating=seating,
            distance=self.distance,
            start=self.start,
            destination=self.destination,
        )

    def by_tram(self):
        return _TripByTram(
            distance=self.distance,
            start=self.start,
            destination=self.destination,
        )

    def by_ferry(self, ferry_class: str = None):
        return _TripByFerry(
            ferry_class=ferry_class,
            distance=self.distance,
            start=self.start,
            destination=self.destination,
        )

    def by_bus(
        self, fuel_type: str = None, size: str = None, vehicle_range: str = None
    ):
        return _TripByBus(
            fuel_type=fuel_type,
            size=size,
            vehicle_range=vehicle_range,
            distance=self.distance,
            start=self.start,
            destination=self.destination,
        )

    def by_motorbike(self, size: str = None):
        return _TripByMotorbike(
            size=size,
            distance=self.distance,
            start=self.start,
            destination=self.destination,
        )

    def by_bicycle(self):
        return _TripByBicycle(
            distance=self.distance,
            start=self.start,
            destination=self.destination,
        )

    def by_pedelec(self):
        return _TripByPedelec(
            distance=self.distance,
            start=self.start,
            destination=self.destination,
        )

    def by_custom(self, emission_factor: float, transport_mode: str = None):
        return _TripCustom(
            emission_factor=emission_factor,
            transport_mode=transport_mode,
            distance=self.distance,
            start=self.start,
            destination=self.destination,
        )


class _TripByCar(Trip):
    """
    This is a hidden class which handles car trips.
    :param fuel_type: The fuel type of the car
    :param size: The size of the car
    """

    transport_mode = TransportationMode.CAR

    def __init__(
        self,
        fuel_type: str = None,
        size: str = None,
        passengers: int = None,
        distance: float = None,
        start: dict | str = None,
        destination: dict | str = None,
    ):
        """Initialize a car trip"""
        super(_TripByCar, self).__init__(
            distance=distance,
            start=start,
            destination=destination,
            transport_mode=self.transport_mode,
        )
        self.fuel_type = fuel_type
        self.size = size
        self.passengers = passengers

    def calculate_co2e(self):
        """
        Calculate the CO2e emissions for a car trip.
        :return: Emissions object
        """
        if self.distance is None:
            self.calculate_distance()

        # Calculate emissions
        options = {
            "fuel_type": self.fuel_type,
            "size": self.size,
            "passengers": self.passengers,
        }
        # Filter out items where value is None
        options = {k: v for k, v in options.items() if v is not None}

        co2e, emission_factor, emission_parameters = calc_co2_car(
            self.distance, options=options
        )
        emissions = TransportEmissions(
            co2e=co2e,
            emission_factor=emission_factor,
            emission_parameters=emission_parameters,
            distance=self.distance,
        )
        return emissions

    def get_options(self):
        """
        Return available options for car trips.
        :return: Dictionary of available options
        """
        options = {
            "fuel_type": [
                "gasoline",
                "diesel",
                "electric",
                "hybrid",
                "plug-in_hybrid",
                "cng",
                "average",
            ],
            "size": ["small", "medium", "large", "average"],
            "passengers": "Enter the number of passengers (default is 1)",
        }
        return options


class _TripByTrain(Trip):
    """This is a hidden class which handles train trips.
    :param: CountryCode
    """

    transport_mode = TransportationMode.TRAIN

    def __init__(
        self,
        distance: float = None,
        start: dict | str = None,
        destination: dict | str = None,
        country_code: str | CountryCode2 | CountryCode3 = None,
    ):
        """Initialize a train trip"""
        super(_TripByTrain, self).__init__(
            distance=distance,
            start=start,
            destination=destination,
            transport_mode=self.transport_mode,
        )
        self.country_code = country_code

    def calculate_co2e(self):
        """
        Calculate the CO2e emissions for a train trip
        :return: Emissions object
        """
        # TODO: change for train
        if self.distance is None:
            self.calculate_distance()

        # Calculate emissions
        options = {"country_code": self.country_code}
        # Filter out items where value is None
        options = {k: v for k, v in options.items() if v is not None}

        co2e, emission_factor, emission_parameters = calc_co2_train(
            self.distance, options=options
        )
        emissions = TransportEmissions(
            co2e=co2e,
            emission_factor=emission_factor,
            emission_parameters=emission_parameters,
            distance=self.distance,
        )
        return emissions

    def get_options(self):
        # TODO: Implement options retrieval
        pass


class _TripByPlane(Trip):
    """
    This is a hidden class which handles plane trips.
    :param seating: The type of seating class
    """

    transport_mode = TransportationMode.PLANE

    def __init__(
        self,
        seating: str = None,
        distance: float = None,
        start: dict | str = None,
        destination: dict | str = None,
    ):
        """Initialize a plane trip"""
        super(_TripByPlane, self).__init__(
            distance=distance,
            start=start,
            destination=destination,
            transport_mode=self.transport_mode,
        )
        self.seating = seating

    def calculate_co2e(self):
        """
        Calculate the CO2e emissions for a plane trip
        :return Emissions object
        """
        if self.distance is None:
            self.calculate_distance()

        # Calculate emissions
        options = {"seating": self.seating}
        # Filter out items where value is None
        options = {k: v for k, v in options.items() if v is not None}

        co2e, emission_factor, emission_parameters = calc_co2_plane(
            self.distance, options=options
        )
        emissions = TransportEmissions(
            co2e=co2e,
            distance=self.distance,
            emission_factor=emission_factor,
            emission_parameters=emission_parameters,
        )
        return emissions

    def get_options(self):
        # TODO: Implement options retrieval
        pass


class _TripByTram(Trip):
    """This is a hidden class which handles tram trips."""

    transport_mode = TransportationMode.TRAM

    def __init__(
        self,
        distance: float = None,
        start: dict | str = None,
        destination: dict | str = None,
    ):
        """Initialue a tram trip"""
        super(_TripByTram, self).__init__(
            distance=distance,
            start=start,
            destination=destination,
            transport_mode=self.transport_mode,
        )

    def calculate_co2e(self):
        """
        Calculate the CO2e emissions for a tram trip.
        :return: Emissions object
        """
        if self.distance is None:
            self.calculate_distance()

        co2e, emission_factor, emission_parameters = calc_co2_tram(
            self.distance, options={}
        )
        emissions = TransportEmissions(
            co2e=co2e,
            distance=self.distance,
            emission_factor=emission_factor,
            emission_parameters=emission_parameters,
        )
        return emissions

    def get_options(self):
        # TODO: Implement options retrieval
        pass


class _TripByFerry(Trip):
    """
    This is a hidden class which handles ferry trips.
    :param ferry_class: The type of seating class
    """

    transport_mode = TransportationMode.FERRY

    def __init__(
        self,
        ferry_class: str = None,
        distance: float = None,
        start: dict | str = None,
        destination: dict | str = None,
    ):
        """Initialize a ferry trip"""
        super(_TripByFerry, self).__init__(
            distance=distance,
            start=start,
            destination=destination,
            transport_mode=self.transport_mode,
        )
        self.ferry_class = ferry_class

    def calculate_co2e(self):
        """
        Calculate the CO2e emissions for a ferry trip

        :return: Emissions object
        """
        if self.distance is None:
            self.calculate_distance()

        # Calculate emissions
        options = {"ferry_class": self.ferry_class}
        # Filter out items where value is None
        options = {k: v for k, v in options.items() if v is not None}

        co2e, emission_factor, emission_parameters = calc_co2_ferry(
            self.distance, options=options
        )
        emissions = TransportEmissions(
            co2e=co2e,
            distance=self.distance,
            emission_factor=emission_factor,
            emission_parameters=emission_parameters,
        )
        return emissions

    def get_options(self):
        # TODO: Implement options retrieval
        pass


class _TripByBus(Trip):
    """
    This is a hidden class which handles bus trips.
    :param fuel_type: The fuel type of the bus
    :param size: The size of the bus
    :param vehicle_range: The distance of the bus journey
    """

    transport_mode = TransportationMode.BUS

    def __init__(
        self,
        fuel_type: str = None,
        size: str = None,
        vehicle_range: str = None,
        distance: float = None,
        start: dict | str = None,
        destination: dict | str = None,
    ):
        """Initialize a car trip"""
        super(_TripByBus, self).__init__(
            distance=distance,
            start=start,
            destination=destination,
            transport_mode=self.transport_mode,
        )
        self.fuel_type = fuel_type
        self.size = size
        self.vehicle_range = vehicle_range

    def calculate_co2e(self):
        """
        Calculate the CO2e emissions for a bus trip

        :return: Emissions object
        """
        if self.distance is None:
            self.calculate_distance()

        # Calculate emissions
        options = {
            "fuel_type": self.fuel_type,
            "size": self.size,
            "vehicle_range": self.vehicle_range,
        }
        # Filter out items where value is None
        options = {k: v for k, v in options.items() if v is not None}

        co2e, emission_factor, emission_parameters = calc_co2_bus(
            self.distance, options=options
        )
        emissions = TransportEmissions(
            co2e=co2e,
            distance=self.distance,
            emission_factor=emission_factor,
            emission_parameters=emission_parameters,
        )
        return emissions

    def get_options(self):
        # TODO: Implement options retrieval
        pass


class _TripByMotorbike(Trip):
    """
    This is a hidden class which handles motorbike trips.
    :param size: The size of the motorbike
    """

    transport_mode = TransportationMode.MOTORBIKE

    def __init__(
        self,
        size: str = None,
        distance: float = None,
        start: dict | str = None,
        destination: dict | str = None,
    ):
        """Initialize a car trip"""
        super(_TripByMotorbike, self).__init__(
            distance=distance,
            start=start,
            destination=destination,
            transport_mode=self.transport_mode,
        )
        self.size = size

    def calculate_co2e(self):
        """
        Calculate the CO2e emissions for a bus trip

        :return: Emissions object
        """
        if self.distance is None:
            self.calculate_distance()

        # Calculate emissions
        options = {"size": self.size}
        # Filter out items where value is None
        options = {k: v for k, v in options.items() if v is not None}

        co2e, emission_factor, emission_parameters = calc_co2_motorbike(
            self.distance, options=options
        )
        emissions = TransportEmissions(
            co2e=co2e,
            distance=self.distance,
            emission_factor=emission_factor,
            emission_parameters=emission_parameters,
        )
        return emissions

    def get_options(self):
        # TODO: Implement options retrieval
        pass


class _TripByBicycle(Trip):
    """This is a hidden class which handles bicycle trips."""

    transport_mode = TransportationMode.BICYCLE

    def __init__(
        self,
        distance: float = None,
        start: dict | str = None,
        destination: dict | str = None,
    ):
        """Initialue a tram trip"""
        super(_TripByBicycle, self).__init__(
            distance=distance,
            start=start,
            destination=destination,
            transport_mode=self.transport_mode,
        )

    def calculate_co2e(self):
        """
        Calculate the CO2e emissions for a bicycle trip.
        :return: Emissions object
        """
        if self.distance is None:
            self.calculate_distance()

        co2e, emission_factor, emission_parameters = calc_co2_bicycle(
            self.distance, options={}
        )
        emissions = TransportEmissions(
            co2e=co2e,
            distance=self.distance,
            emission_factor=emission_factor,
            emission_parameters=emission_parameters,
        )
        return emissions

    def get_options(self):
        # TODO: Implement options retrieval
        pass


class _TripByPedelec(Trip):
    """This is a hidden class which handles pedelec trips."""

    transport_mode = TransportationMode.PEDELEC

    def __init__(
        self,
        distance: float = None,
        start: dict | str = None,
        destination: dict | str = None,
    ):
        """Initialue a tram trip"""
        super(_TripByPedelec, self).__init__(
            distance=distance,
            start=start,
            destination=destination,
            transport_mode=self.transport_mode,
        )

    def calculate_co2e(self):
        """
        Calculate the CO2e emissions for a pedelec trip.
        :return: Emissions object
        """
        if self.distance is None:
            self.calculate_distance()

        co2e, emission_factor, emission_parameters = calc_co2_pedelec(
            self.distance, options={}
        )
        emissions = TransportEmissions(
            co2e=co2e,
            distance=self.distance,
            emission_factor=emission_factor,
            emission_parameters=emission_parameters,
        )
        return emissions

    def get_options(self):
        # TODO: Implement options retrieval
        pass


class _TripCustom(Trip):
    """This is a hidden class which handles custom trips."""

    def __init__(
        self,
        emission_factor: float = None,
        transport_mode: str = None,
        distance: float = None,
        start: dict | str = None,
        destination: dict | str = None,
    ):
        """Initialize a custom trip"""
        assert emission_factor >= 0, "Emission factor must be >= 0"
        self.emission_factor = emission_factor
        if transport_mode is None and distance is None:
            raise ValueError(
                "Transport mode must be given, unless distance is provided."
            )
        if transport_mode is not None:
            self.transport_mode = TransportationMode(transport_mode)
        else:
            self.transport_mode = None
        super(_TripCustom, self).__init__(
            distance=distance,
            start=start,
            destination=destination,
            transport_mode=self.transport_mode,
        )

    def calculate_co2e(self):
        """
        Calculate the CO2e emissions for a custom trip.
        :return: Emissions object
        """
        if self.distance is None:
            self.calculate_distance()

        # calculate emissions
        emission_parameters = {"transport_mode": self.transport_mode}
        co2e = self.distance * self.emission_factor

        emissions = TransportEmissions(
            co2e=co2e,
            distance=self.distance,
            emission_factor=self.emission_factor,
            emission_parameters=emission_parameters,
        )
        return emissions
