=====================
Distance calculations
=====================

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