====================
Transportation modes
====================

.. contents::

Trips can be calculated for different modes of transport.
The overview here summarizes, which parameters influence the carbon emission intensity of a trip for the different transportation modes.
The specific emission factors for different configurations (e.g., vehicle size, fuel type, etc.) are documented under
:doc:`Emission factors <emission_factors>`.

Car trip
--------
The quantity of CO2e emitted by a car trip per km depends on the ``fuel_type`` (average, cng, diesel, electric, gasoline,
hybrid, plug-in_hybrid), car ``size`` (average, small, medium, large) and the number of ``passengers``.

Bus trip
--------
The quantity of CO2e emitted by a bus trip per km depends on the bus ``size`` (average, small, medium, large)
and the ``vehicle_range`` (local, long-distance).

Plane trip
----------
The quantity of CO2e emitted by a plane trip per km depends on the
``seating_class`` (average, economy_class, business_class, first_class) and on the 
``distance`` of the flight.

Ferry trip
----------
The quantity of CO2e emitted by a ferry trip per km depends on the
``ferry_class`` (average, foot_passenger, car_passenger).

Motorbike trip
--------------
The quantity of CO2e emitted by a motorbike trip per km depends on the ``size`` (average, small, medium, large) of the
motorbike.

Train, tram, bicycle or pedelec trip
--------------------------------------
For train, tram, bicylce or pedelec, no specifica have to be provided.
