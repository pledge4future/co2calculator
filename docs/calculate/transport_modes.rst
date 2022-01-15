====================
Transportation modes
====================

.. contents::

Business trips can be calculated for different modes of transport.
The overview here summarizes, which parameters influence the carbon emission intensity of a trip for the different transportation modes.
The specific emission factors for different configurations (e.g., vehicle size, fuel type, etc.) are documented under
:doc:`Emission factors <emission_factors>`.

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
