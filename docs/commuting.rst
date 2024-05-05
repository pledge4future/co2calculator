=========
Commuting
=========

.. contents::

The calculation of emissions from commuting is currently supported for the following modes of transport:

* car
* bus
* train
* motorbike
* tram
* bicycle
* pedelec

Their specific emission factors for different configurations (e.g., vehicle size, fuel type, etc.) are documented under
:doc:`Emission factors <calculate/emission_factors>`.

For each mode of transport used for the commute, the user must provide the average ``weekly_distance`` (in km) travelled during
a given time period. The users are asked to enter their usual commuting behaviour and should estimate the distance as
accurately as possible. If they often use a different mode of transport if there is bad weather or in the cold season,
they should account for this by estimating the mean distance for each transportation mode over the entire year. The
commuting data may also be entered separately for each month or once for the summer months and for the winter months
(e.g., April-October and November-March).

Aside of the mode of transport and the weekly distance, the user should provide the specifica of the commute, depending on
the mode of transport (see :doc:`Emission factors <calculate/emission_factors>`).

.. autofunction:: co2calculator.calculate.calc_co2_commuting


Car commute
-----------
The quantity of CO2e emitted by a car commute depends on the ``fuel_type`` (average, cng, diesel, electric, gasoline,
hybrid, hydrogen, plug-in_hybrid), car ``size`` (average, small, medium, large) and the number of ``passengers``.

Bus commute
-----------
The quantity of CO2e emitted by a bus commute depends on the bus ``size`` (average, medium, large) and the
``occupancy`` in % (20, 50, 80, 100). The ``vehicle_range`` is set to local automatically.

Train commute
-------------
The quantity of CO2e emitted by a train commute depends on the ``fuel_type`` (average, electric, diesel).
The ``vehicle_range`` is set to local automatically.

Motorbike commute
-----------------
The quantity of CO2e emitted by a motorbike commute depends on the ``size`` (average, small, medium, large) of the
motorbike.

Tram, bicycle or pedelec commute
--------------------------------
For tram, bicylce or pedelec, no specifica have to be provided.
