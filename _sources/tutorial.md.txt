# Tutorial

The co2calculator package is available via pip: 

```python
pip install co2calculator
```

For a simple and basic emission calculation, import the calculation function and define some emission cause: 

```python

from co2calculator import calculate_trip
from co2calculator.enums import TransportationMode

co2e = calculate_trip(distance=200,transportation_mode=TransportationMode.CAR)
```
