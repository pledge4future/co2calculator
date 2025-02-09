
=======
Energy
=======


Energy emissions are computed based on the consumption, 
the emission factors for a specified fuel type and a share (of the heated area or the used electricity).

.. autoclass:: co2calculator.api.energy::Energy
    :members:

For the emission factors, see :doc:`Emission factors <emission_factors>`


Heating
--------

Per default, the expected unit is kWh. For some fuel types, the consumption may also be specified using different units, e.g., litres of oil or kg of wood chips.
In these cases, it is possible to specify the `unit`. The consumption will then be converted from the specified unit to kWh, based on common conversion factors:

.. csv-table:: Conversion factors heating
    :file: ../../co2calculator/data/conversion_factors_heating.csv
    :header-rows: 1
    :stub-columns: 2
    :widths: 10 30 30 30

The parameter `own_share` accounts for the fact, that the heating energy consumption may often only be known for an entire building, 
while a person/group/etc. just occupies parts of the building.
In this case, the (approximate) share of the building floor space, that is occupied by the working group can be provided.
The `own_share` must be between 0.0 and 1.0 and is 1.0 by default.

Electricity
-----------

Electricity emissions are computed based on the consumption (in kWh) 
and the emission factors for a specified energy mix or energy source.
