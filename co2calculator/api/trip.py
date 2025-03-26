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
    #    calc_co2_ferry,
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
    ):
        """Initialize a trip object

        :param distance: Distance in kilometers
        :param start: Start location of the trip
        :param destination: Destination location of the trip
        :type distance: float
        :type start: str
        :type destination: str
        """
        self.__verify_parameters(distance, start, destination)
        self.distance = distance
        self.start = start
        self.destination = destination
        self.transportation_mode = None
        self._start_coords = None
        self._destination_coords = None

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
            transportation_mode=self.transportation_mode,
            start=self.start,
            destination=self.destination,
        )
        distance, coords = get_distance(request)
        self.distance = distance

        # get coordinates
        self._start_coords = coords[0]
        self._destination_coords = coords[1]

        return self.distance

    def by_car(self, fuel_type: str = None, size: str = None, passengers: int = 1):
        """Initialize a car trip object

        :param fuel_type: The fuel type of the car (see CarFuel in constants.py)
        :param size: The size of the car (see Size in constants.py)
        :param passengers: number of passengers (default value: 1)
        :type fuel_type: str
        :type size: str
        :type passengers: int
        :return: _TripByCar object
        """
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
        """Initialize a train trip object

        :param country_code: 2- or 3-letter ISO country code
        :type country_code: str
        :return: _TripByTrain object
        """
        return _TripByTrain(
            country_code=country_code,
            distance=self.distance,
            start=self.start,
            destination=self.destination,
        )

    def by_plane(self, seating: str = None):
        """Initialize a plane trip object

        :param seating: The type of seating class (see FlightClass in constants.py)
        :type seating: str
        :return: _TripByPlane object
        """
        return _TripByPlane(
            seating=seating,
            distance=self.distance,
            start=self.start,
            destination=self.destination,
        )

    def by_tram(self):
        """Initialize a tram trip object

        :return: _TripByTram object
        """
        return _TripByTram(
            distance=self.distance,
            start=self.start,
            destination=self.destination,
        )

    #    def by_ferry(self, ferry_class: str = None):
    #        """Initialize a ferry trip object
    #
    #        :param ferry_class: The type of seating class (see FerryClass in constants.py)
    #        :type ferry_class: str
    #        :return: _TripByFerry object
    #        """
    #        return _TripByFerry(
    #            ferry_class=ferry_class,
    #            distance=self.distance,
    #            start=self.start,
    #            destination=self.destination,
    #        )

    def by_bus(
        self, fuel_type: str = None, size: str = None, vehicle_range: str = None
    ):
        """Initialize a bus trip object

        :param fuel_type: The fuel type of the bus (see BusFuel in constants.py)
        :param size: The size of the bus
        :param vehicle_range: The distance of the bus journey (see BusTrainRange in constants.py)
        :type fuel_type: str
        :type size: str
        :type vehicle_range: str
        :return: _TripByBus object
        """
        return _TripByBus(
            fuel_type=fuel_type,
            size=size,
            vehicle_range=vehicle_range,
            distance=self.distance,
            start=self.start,
            destination=self.destination,
        )

    def by_motorbike(self, size: str = None):
        """Initialize a motorbike trip object

        :param size: The size of the motorbike
        :type size: str
        :return: _TripByMotorbike object
        """
        return _TripByMotorbike(
            size=size,
            distance=self.distance,
            start=self.start,
            destination=self.destination,
        )

    def by_bicycle(self):
        """Initialize a bicycle trip object

        :return: _TripByBicycle object
        """
        return _TripByBicycle(
            distance=self.distance,
            start=self.start,
            destination=self.destination,
        )

    def by_pedelec(self):
        """Initialize a pedelec trip object

        :return: _TripByPedelec object
        """
        return _TripByPedelec(
            distance=self.distance,
            start=self.start,
            destination=self.destination,
        )

    def by_custom(self, emission_factor: float, transportation_mode: str = None):
        return _TripCustom(
            emission_factor=emission_factor,
            transportation_mode=transportation_mode,
            distance=self.distance,
            start=self.start,
            destination=self.destination,
        )


class _TripByCar(Trip):
    """
    This is a hidden class which handles car trips.

    :param fuel_type: The fuel type of the car
    :param size: The size of the car
    :param passengers: number of passengers (default value: 1)
    :param distance: The distance of the car journey
    :param start: The start location of the car journey
    :param destination: The destination location of the car journey
    :type fuel_type: str
    :type size: str
    :type passengers: int
    :type distance: float
    :type start: dict | str
    :type destination: dict | str
    """

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
            distance=distance, start=start, destination=destination
        )
        self.fuel_type = fuel_type
        self.size = size
        self.passengers = passengers
        self.transportation_mode = TransportationMode.CAR

    def calculate_co2e(self):
        """Calculate the CO2e emissions for a car trip.

        :return: Emissions object
        """
        if self.distance is None:
            distance = self.calculate_distance()
        else:
            distance = self.distance

        # Calculate emissions
        options = {
            "fuel_type": self.fuel_type,
            "size": self.size,
            "passengers": self.passengers,
        }
        # Filter out items where value is None
        options = {k: v for k, v in options.items() if v is not None}

        co2e, emission_factor, emission_parameters = calc_co2_car(
            distance, options=options
        )
        emissions = TransportEmissions(
            co2e=co2e,
            emission_factor=emission_factor,
            emission_parameters=emission_parameters,
            distance=distance,
            start=self.start,
            start_coords=self._start_coords,
            destination=self.destination,
            destination_coords=self._destination_coords,
        )
        return emissions

    def get_options(self):
        """Return available options for car trips.

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

    :param distance: The distance of the train journey
    :param start: The start location of the train journey
    :param destination: The destination location of the train journey
    :param country_code: 2- or 3-letter ISO country code
    :type distance: float
    :type start: dict | str
    :type destination: dict | str
    :type country_code: str | CountryCode2 | CountryCode3
    """

    def __init__(
        self,
        distance: float = None,
        start: dict | str = None,
        destination: dict | str = None,
        country_code: str | CountryCode2 | CountryCode3 = None,
    ):
        """Initialize a train trip"""
        super(_TripByTrain, self).__init__(
            distance=distance, start=start, destination=destination
        )
        self.country_code = country_code
        self.transportation_mode = TransportationMode.TRAIN

    def calculate_co2e(self):
        """Calculate the CO2e emissions for a train trip

        :return: Emissions object
        """
        # TODO: change for train
        if self.distance is None:
            distance = self.calculate_distance()
        else:
            distance = self.distance

        # Calculate emissions
        options = {"country_code": self.country_code}
        # Filter out items where value is None
        options = {k: v for k, v in options.items() if v is not None}

        co2e, emission_factor, emission_parameters = calc_co2_train(
            distance, options=options
        )
        emissions = TransportEmissions(
            co2e=co2e,
            emission_factor=emission_factor,
            emission_parameters=emission_parameters,
            distance=distance,
            start=self.start,
            start_coords=self._start_coords,
            destination=self.destination,
            destination_coords=self._destination_coords,
        )
        return emissions

    def get_options(self):
        # TODO: Implement options retrieval
        pass


class _TripByPlane(Trip):
    """This is a hidden class which handles plane trips.

    :param seating: The type of seating class (see FlightClass in constants.py)
    :param distance: The distance of the plane journey
    :param start: The start location of the plane journey
    :param destination: The destination location of the plane journey
    :type seating: str
    :type distance: float
    :type start: dict | str
    :type destination: dict | str
    """

    def __init__(
        self,
        seating: str = None,
        distance: float = None,
        start: dict | str = None,
        destination: dict | str = None,
    ):
        """Initialize a plane trip"""
        super(_TripByPlane, self).__init__(
            distance=distance, start=start, destination=destination
        )
        self.seating = seating
        self.transportation_mode = TransportationMode.PLANE

    def calculate_co2e(self):
        """Calculate the CO2e emissions for a plane trip

        :return Emissions object
        """
        if self.distance is None:
            distance = self.calculate_distance()
        else:
            distance = self.distance

        # Calculate emissions
        options = {"seating": self.seating}
        # Filter out items where value is None
        options = {k: v for k, v in options.items() if v is not None}

        co2e, emission_factor, emission_parameters = calc_co2_plane(
            distance, options=options
        )
        emissions = TransportEmissions(
            co2e=co2e,
            distance=distance,
            emission_factor=emission_factor,
            emission_parameters=emission_parameters,
            start=self.start,
            start_coords=self._start_coords,
            destination=self.destination,
            destination_coords=self._destination_coords,
        )
        return emissions

    def get_options(self):
        # TODO: Implement options retrieval
        pass


class _TripByTram(Trip):
    """This is a hidden class which handles tram trips.

    :param distance: The distance of the train journey
    :param start: The start location of the train journey
    :param destination: The destination location of the train journey
    :type distance: float
    :type start: dict | str
    :type destination: dict | str
    """

    def __init__(
        self,
        distance: float = None,
        start: dict | str = None,
        destination: dict | str = None,
    ):
        """Initialize a tram trip"""
        super(_TripByTram, self).__init__(
            distance=distance, start=start, destination=destination
        )
        self.transportation_mode = TransportationMode.TRAM

    def calculate_co2e(self):
        """Calculate the CO2e emissions for a tram trip.

        :return: Emissions object
        """
        if self.distance is None:
            distance = self.calculate_distance()
        else:
            distance = self.distance

        co2e, emission_factor, emission_parameters = calc_co2_tram(distance, options={})
        emissions = TransportEmissions(
            co2e=co2e,
            distance=distance,
            emission_factor=emission_factor,
            emission_parameters=emission_parameters,
            start=self.start,
            start_coords=self._start_coords,
            destination=self.destination,
            destination_coords=self._destination_coords,
        )
        return emissions

    def get_options(self):
        # TODO: Implement options retrieval
        pass


# class _TripByFerry(Trip):
#    """This is a hidden class which handles ferry trips.
#
#    :param ferry_class: The type of seating class
#    :param distance: The distance of the ferry journey
#    :param start: The start location of the ferry journey
#    :param destination: The destination location of the ferry journey
#    :type ferry_class: str
#    :type distance: float
#    :type start: dict | str
#    :type destination: dict | str
#    """
#
#    def __init__(
#        self,
#        ferry_class: str = None,
#        distance: float = None,
#        start: dict | str = None,
#        destination: dict | str = None,
#    ):
#        """Initialize a ferry trip"""
#        super(_TripByFerry, self).__init__(
#            distance=distance, start=start, destination=destination
#        )
#        self.ferry_class = ferry_class
#        self.transportation_mode = TransportationMode.FERRY
#
#    def calculate_co2e(self):
#        """Calculate the CO2e emissions for a ferry trip
#
#        :return: Emissions object
#        """
#        if self.distance is None:
#            self.calculate_distance()
#
#        # Calculate emissions
#        options = {"ferry_class": self.ferry_class}
#        # Filter out items where value is None
#        options = {k: v for k, v in options.items() if v is not None}
#
#        co2e, emission_factor, emission_parameters = calc_co2_ferry(
#            self.distance, options=options
#        )
#        emissions = TransportEmissions(
#            co2e=co2e,
#            distance=self.distance,
#            emission_factor=emission_factor,
#            emission_parameters=emission_parameters,
#        )
#        return emissions
#
#    def get_options(self):
#        # TODO: Implement options retrieval
#        pass


class _TripByBus(Trip):
    """This is a hidden class which handles bus trips.

    :param fuel_type: The fuel type of the bus (see BusFuel in constants.py)
    :param size: The size of the bus
    :param vehicle_range: The distance of the bus journey (see BusTrainRange in constants.py)
    :param distance: The distance of the bus journey
    :param start: The start location of the bus journey
    :param destination: The destination location of the bus journey
    :type fuel_type: str
    :type size: str
    :type vehicle_range: str
    :type distance: float
    :type start: dict | str
    :type destination: dict | str
    """

    def __init__(
        self,
        fuel_type: str = None,
        size: str = None,
        vehicle_range: str = None,
        distance: float = None,
        start: dict | str = None,
        destination: dict | str = None,
    ):
        """Initialize a bus trip"""
        super(_TripByBus, self).__init__(
            distance=distance, start=start, destination=destination
        )
        self.fuel_type = fuel_type
        self.size = size
        self.vehicle_range = vehicle_range
        self.transportation_mode = TransportationMode.BUS

    def calculate_co2e(self):
        """Calculate the CO2e emissions for a bus trip

        :return: Emissions object
        """
        if self.distance is None:
            distance = self.calculate_distance()
        else:
            distance = self.distance

        # Calculate emissions
        options = {
            "fuel_type": self.fuel_type,
            "size": self.size,
            "vehicle_range": self.vehicle_range,
        }
        # Filter out items where value is None
        options = {k: v for k, v in options.items() if v is not None}

        co2e, emission_factor, emission_parameters = calc_co2_bus(
            distance, options=options
        )
        emissions = TransportEmissions(
            co2e=co2e,
            distance=distance,
            emission_factor=emission_factor,
            emission_parameters=emission_parameters,
            start=self.start,
            start_coords=self._start_coords,
            destination=self.destination,
            destination_coords=self._destination_coords,
        )
        return emissions

    def get_options(self):
        # TODO: Implement options retrieval
        pass


class _TripByMotorbike(Trip):
    """This is a hidden class which handles motorbike trips.

    :param size: The size of the motorbike
    :param distance: The distance of the motorbike journey
    :param start: The start location of the motorbike journey
    :param destination: The destination location of the motorbike journey
    :type size: str
    :type distance: float
    :type start: dict | str
    :type destination: dict | str
    """

    def __init__(
        self,
        size: str = None,
        distance: float = None,
        start: dict | str = None,
        destination: dict | str = None,
    ):
        """Initialize a motorbike trip"""
        super(_TripByMotorbike, self).__init__(
            distance=distance, start=start, destination=destination
        )
        self.size = size
        self.transportation_mode = TransportationMode.MOTORBIKE

    def calculate_co2e(self):
        """Calculate the CO2e emissions for a motorbike trip

        :return: Emissions object
        """
        if self.distance is None:
            distance = self.calculate_distance()
        else:
            distance = self.distance

        # Calculate emissions
        options = {"size": self.size}
        # Filter out items where value is None
        options = {k: v for k, v in options.items() if v is not None}

        co2e, emission_factor, emission_parameters = calc_co2_motorbike(
            distance, options=options
        )
        emissions = TransportEmissions(
            co2e=co2e,
            distance=distance,
            emission_factor=emission_factor,
            emission_parameters=emission_parameters,
            start=self.start,
            start_coords=self._start_coords,
            destination=self.destination,
            destination_coords=self._destination_coords,
        )
        return emissions

    def get_options(self):
        # TODO: Implement options retrieval
        pass


class _TripByBicycle(Trip):
    """This is a hidden class which handles bicycle trips.

    :param distance: The distance of the bicycle journey
    :param start: The start location of the bicycle journey
    :param destination: The destination location of the bicycle journey
    :type distance: float
    :type start: dict | str
    :type destination: dict | str
    """

    def __init__(
        self,
        distance: float = None,
        start: dict | str = None,
        destination: dict | str = None,
    ):
        """Initialize a bicycle trip"""
        super(_TripByBicycle, self).__init__(
            distance=distance, start=start, destination=destination
        )
        self.transportation_mode = TransportationMode.BICYCLE

    def calculate_co2e(self):
        """Calculate the CO2e emissions for a bicycle trip.

        :return: Emissions object
        """
        if self.distance is None:
            distance = self.calculate_distance()
        else:
            distance = self.distance

        co2e, emission_factor, emission_parameters = calc_co2_bicycle(
            distance, options={}
        )
        emissions = TransportEmissions(
            co2e=co2e,
            distance=distance,
            emission_factor=emission_factor,
            emission_parameters=emission_parameters,
            start=self.start,
            start_coords=self._start_coords,
            destination=self.destination,
            destination_coords=self._destination_coords,
        )
        return emissions

    def get_options(self):
        # TODO: Implement options retrieval
        pass


class _TripByPedelec(Trip):
    """This is a hidden class which handles pedelec trips.

    :param distance: The distance of the pedelec journey
    :param start: The start location of the pedelec journey
    :param destination: The destination location of the pedelec journey
    :type distance: float
    :type start: dict | str
    :type destination: dict | str
    """

    def __init__(
        self,
        distance: float = None,
        start: dict | str = None,
        destination: dict | str = None,
    ):
        """Initialize a pedelec trip"""
        super(_TripByPedelec, self).__init__(
            distance=distance, start=start, destination=destination
        )
        self.transportation_mode = TransportationMode.PEDELEC

    def calculate_co2e(self):
        """Calculate the CO2e emissions for a pedelec trip.

        :return: Emissions object
        """
        if self.distance is None:
            distance = self.calculate_distance()
        else:
            distance = self.distance

        co2e, emission_factor, emission_parameters = calc_co2_pedelec(
            distance, options={}
        )
        emissions = TransportEmissions(
            co2e=co2e,
            distance=distance,
            emission_factor=emission_factor,
            emission_parameters=emission_parameters,
            start=self.start,
            start_coords=self._start_coords,
            destination=self.destination,
            destination_coords=self._destination_coords,
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
        transportation_mode: str = None,
        distance: float = None,
        start: dict | str = None,
        destination: dict | str = None,
    ):
        """Initialize a custom trip"""
        super(_TripCustom, self).__init__(
            distance=distance, start=start, destination=destination
        )
        assert emission_factor >= 0, "Emission factor must be >= 0"
        self.emission_factor = emission_factor
        if transportation_mode is None and distance is None:
            raise ValueError(
                "Transport mode must be given, unless distance is provided."
            )
        if transportation_mode is not None:
            self.transportation_mode = TransportationMode(transportation_mode)
        else:
            self.transportation_mode = None

    def calculate_co2e(self):
        """
        Calculate the CO2e emissions for a custom trip.
        :return: Emissions object
        """
        if self.distance is None:
            distance = self.calculate_distance()
        else:
            distance = self.distance

        # calculate emissions
        emission_parameters = {"transportation_mode": self.transportation_mode}
        co2e = distance * self.emission_factor

        emissions = TransportEmissions(
            co2e=co2e,
            distance=distance,
            emission_factor=self.emission_factor,
            emission_parameters=emission_parameters,
            start=self.start,
            start_coords=self._start_coords,
            destination=self.destination,
            destination_coords=self._destination_coords,
        )
        return emissions
