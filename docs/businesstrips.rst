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

The user must specify either the distance of a trip or the location of departure and destination.
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
The quantity of CO2e emitted by a bus trip depends on the bus ``size`` (average, medium, large) and the
``occupancy`` in % (20, 50, 80, 100). The ``vehicle_range`` is set to long-distance automatically.

Train trip
----------
The quantity of CO2e emitted by a train trip depends on the ``fuel_type`` (average, electric, diesel).
The ``vehicle_range`` is set to long-distance automatically.

Plane trip
----------
The quantity of CO2e emitted by a plane trip depends on the
``seating_class`` (average, economy_class, business_class, premium_economy_class, first_class).

Ferry trip
----------
The quantity of CO2e emitted by a ferry trip depends on the
``seating_class`` (average, Foot passenger, Car passenger).