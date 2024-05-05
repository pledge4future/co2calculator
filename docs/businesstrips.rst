==============
Business trips
==============

.. toctree::
   :maxdepth: 2
   :caption: See also:
   :titlesonly:
   :includehidden:

   calculate/distances
   calculate/transport_modes

The calculation of emissions from business trips is currently supported for the following modes of transport:

* car
* bus
* train
* plane
* ferry

The user must specify either the distance of a trip or the location of departure and destination.
The distance (in km) may be used, when the user has the direct information of the distance travelled, e.g., from the speedometer of a car.
In other cases, the distance can be calculated from the given locations, see :ref:`Distance calculations <Distance calculations>`.
With the boolean paramter ``roundtrip``, users can indicate whether a trip was a roundtrip, in which case the distance wil be doubled.

Aside of the mode of transport, the user should provide the specifica of the trip, depending on the mode of transport
(see :doc'Transportation modes <calculate/transport_modes>' :doc:`Emission factors <calculate/emission_factors>`).

.. autofunction:: co2calculator.calculate.calc_co2_businesstrip
