
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

Heating consumption is expected in different units, depending on the fuel type, e.g., litres of oil or kg of wood chips.
The consumption will first be converted to kWh, based on common conversion factors, and then be multiplied by the emission factor.
See the table below for the expected units per fuel type.
For all fuel types, the consumption can also be specified in kWh. In this case, the `in_kwh` flag must be set to `True`.

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
