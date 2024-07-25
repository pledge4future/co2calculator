
=======
Heating
=======

Heating emissions are computed based on the consumption (typically in kWh) and the emission factors for a specified fuel type.

.. autofunction:: co2calculator.calculate.calc_co2_heating

Per default, the expected unit is kWh. For some fuel types, the consumption may also be specified using different units, e.g., litres of oil or kg of wood chips.
In these cases, it is possible to specify the `unit`. The consumption will then be converted from the specified unit to kWh, based on common conversion factors:

.. csv-table:: Conversion factors heating
    :file: ../../data/conversion_factors_heating.csv
    :header-rows: 1
    :stub-columns: 2
    :widths: 10 30 30 30

The parameter `area_share` accounts for the fact, that the heating energy consumption may often only be known for an entire building, while a working group just occupies parts of the building.
In this case, the (approximate) share of the building floor space, that is occupied by the working group can be provided.
The `area_share` must be between 0.0 and 1.0 and is 1.0 by default.
