==============
Business trips
==============

.. contents::

The calculation of emissions from business trips is currently supported for the following modes of transport:

* car
* bus
* train
* plane
* ferry

Their specific emission factors for different configurations (e.g., vehicle size, fuel type, etc.) are documented under
:doc:`Emission factors <calculate/emission_factors>`.

The user must specify either the distance of a trip of the location of departure and destination.
The distance (in km) may be used, when the user has the direct information of the distance travelled, e.g., from the speedometer of a car.
In other cases, the distance can be calculated from the given locations, see :ref:`Distance calculations <Distance calculations>`.
With the boolean paramter ``roundtrip``, users can indicate whether a trip was a roundtrip, in which case the distance wil be doubled, or not.

Aside of the mode of transport, the user should provide the specifica of the trip, depending on the mode of transport
(see :doc:`Emission factors <calculate/emission_factors>`).

.. autofunction:: co2calculator.calculate.calc_co2_businesstrip


Car trip
--------

The quantity of CO2e emitted by a car trip depends on the ``fuel_type`` (average, cng, diesel, electric, gasoline,
hybrid, hydrogen, plug-in_hybrid), car ``size`` (average, small, medium, large) and the number of ``passengers``.

Bus trip
--------
The quantity of CO2e emitted by a bus trip depends on the
bus ``size`` (average, medium, large) and the ``occupancy`` in % (20, 50, 80, 100).


Distance calculations
---------------------

For the computation of distances between places of departure and destination, we use two different approaches,
depending on the specified mode of transport:

a) Distance as the crow flies + detour
""""""""""""""""""""""""""""""""""""""
Calculating the distance as the crow flies (great circle distance) and multiplying by a detour coefficient or adding
a detour constant.

The distance as the crow flies is calculated using the haversine formula:

.. autofunction:: co2calculator.distances.haversine

The transport modes for which this approach is used are listed in the table below, together with their detour parameters.

.. csv-table:: Detour parameters
    :file: ../data/detour.csv
    :header-rows: 1
    :stub-columns: 2
    :widths: 10 30 30 30

b) Road distance
""""""""""""""""
Calculating the road distance using `openrouteservice <https://openrouteservice.org/>`_.

This approach is only used for the transport mode ``car``.
