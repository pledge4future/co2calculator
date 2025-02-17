========
Mobility
========

.. toctree::
   :maxdepth: 2
   :caption: See also:
   :titlesonly:
   :includehidden:

   calculate/distances
   calculate/transport_modes

Trips
-----

The calculation of emissions from trips is currently supported for the following modes of transport:

* train
* bus
* tram
* plane
* ferry
* bicycle
* pedelec
* car
* motorbike

The user must specify either the distance of a trip or the location of departure and destination.
The distance (in km) may be used when the user has the direct information of the distance travelled, e.g., from the speedometer of a car.
In other cases, the distance can be calculated from the given locations, see :ref:`Distance calculations <Distance calculations>`.

Aside of the mode of transport, the user should provide the specifica of the trip, depending on the mode of transport
(see :doc:`Transportation modes <calculate/transport_modes>` and :doc:`Emission factors <calculate/emission_factors>`).


See also:

.. autoclass:: co2calculator.api.trip::Trip
   :members:

In addition, the user can specify a custom ``emission_factor`` for the trip using the `.by_custom()` method.
If no `distance` is provided, but a `start` and `destination`, then a `transport_mode` is required
to calculate the distance between the two locations in the appropriate way.
