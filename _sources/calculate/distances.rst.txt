=====================
Distance calculations
=====================

Geocoding
---------

The first step in calculating the distance between two locations is to obtain the geographic coordinates of
these locations, which is called *geocoding*. For this, we use the open-source geocoder `Pelias <https://pelias.io/>`_,
as well as a database of train stations.

a) Geocoding for air travel
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Most airports around the world can be identified by a unique code, assigned by the International Air Transport Association (`IATA <https://www.iata.org/>`_).
To retrieve the location of airports, we use `Pelias <https://pelias.io/>`_ and search for the IATA code in combination with the keyword "Airport".

.. autofunction:: co2calculator.distances.geocoding_airport

In the ``calc_co2_businesstrip()`` function, the user only needs to provide the IATA codes for start and destination, e.g.::

    emissions, distance, range_category, range_description = calc_co2_businesstrip(
        transportation_mode: "plane",
        start="FRA",
        destination="SCQ",
        seating = "economy_class",
        roundtrip: bool = False)

b) Geocoding for train trips
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To obtain the coordinates of train stations within Europe, we use the `train station database <https://github.com/trainline-eu/stations>`_
by `Trainline <https://www.thetrainline.com/de?redirected=true>`_.

.. autofunction:: co2calculator.distances.geocoding_train_stations

As you can see above, a dictionary with the keys `country` and `station_name` has to be provided for both start and destination.
Calculating a train trip may thus look like this::

    start_dict = {
                  "country": "DE",
                  "station_name: "Heidelberg Hauptbahnhof"
                  }
    dest_dict = {
                  "country": "DE",
                  "station_name: "Hamburg Hauptbahnhof"
                  }
    emissions, distance, range_category, range_description = calc_co2_businesstrip(
        transportation_mode: "train",
        start=start_dict,
        destination=dest_dict
        roundtrip: bool = False)

We use the fuzzy string matching package `thefuzz <https://github.com/seatgeek/thefuzz>`_ to find the train station in the database which best matches the
user input.

c) Geocoding for other trips
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For other trips (e.g., car or bus), we use `Pelias structured geocoding <https://github.com/pelias/documentation/blob/master/structured-geocoding.md>`_
as included in `openrouteservice <https://openrouteservice.org/>`_.
This means that the user has different predefined fields to specify an address.

.. autofunction:: co2calculator.distances.geocoding_structured

Good results can be achieved by specifying `country`, `locality` and `address`. Further specifications
are usually not needed and can sometimes even negatively affect the geocoding results.

Distance computation
--------------------

For the computation of distances between places of departure and destination, we use two different approaches,
depending on the specified mode of transport:

a) Distance as the crow flies + detour
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Calculating the distance as the crow flies (great circle distance) and multiplying by a detour coefficient or adding
a detour constant.

The distance as the crow flies is calculated using the haversine formula:

.. autofunction:: co2calculator.distances.haversine

The transport modes for which this approach is used are listed in the table below, together with their detour parameters.

.. csv-table:: Detour parameters
    :file: ../../data/detour.csv
    :header-rows: 1
    :stub-columns: 2
    :widths: 10 30 30 30

b) Road distance
^^^^^^^^^^^^^^^^

Calculating the road distance using `openrouteservice <https://openrouteservice.org/>`_.

This approach is only used for the transport mode ``car``.

Here is an example of how this works using the ``openrouteservice`` `Python library <https://pypi.org/project/openrouteservice/>`_).
::

    import openrouteservice
    from openrouteservice.directions import directions

    clnt = openrouteservice.Client(key=ors_api_key)

    # coords: list/tuple of locations [lat,long]
    route = directions(clnt, coords, profile="driving-car")
    distance = route["routes"][0]["summary"]["distance"]
