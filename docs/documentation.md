# Documentation of CO<sub>2</sub> calculations

The *co2calculator* can compute emissions caused by four big areas of the work live: Electricity, Heating, Business trips and Commuting. Emissions are given as CO<sub>2</sub> equivalents (CO<sub>2</sub>e). 

Business trips and field trips are assessed on an individual level whereas heating and electricity are assessed once for the entire research group.

The CO<sub>2</sub>e emissions are calculated using emission factors from different sources:
- [Probas](https://www.probas.umweltbundesamt.de/php/index.php): electricity, heating, most cars, buses, trains
- [UBA (2021). "Umweltfreundlich mobil"](https://www.umweltbundesamt.de/en/publikationen/umweltfreundlich-mobil): bicycles, pedelecs, trams
- [GOV.UK (2020). Greenhouse gas reporting: conversion factors 2020](https://www.gov.uk/government/publications/greenhouse-gas-reporting-conversion-factors-2020): planes, ferries, electric cars, motorbikes

The specific emission factors for different activities are collected in [this emission factor table](https://github.com/pledge4future/co2calculator/blob/dev/data/emission_factors.csv). 

The basic formula is:
`co2 emissions = consumption * emission factor` 


## 1 Electricity

For electricity the user can select between the German electricity mix or solar power. The German electricity mix applies, if the research institute has a regular electricity contract. Solar power is applicable, if the institute uses self-generated solar power. The user is asked for the annual electricity consumption c [kWh] which is then used to calculate the CO<sub>2</sub> equivalents [kg/TJ]. Since the emission factors for heating and electricity in the ProBas database apply for a consumption of 1 TJ, the consumption needs to be converted from kWh to TJ with a conversion factor of 277777.7778.

## 2 Heating

The user is asked about the annual consumption and the primary energy source for heating, based on which the CO2e emissions are determined. Heating consumption can be provided in kWh, or in other units, depending on the fuel type (see this [conversion table](https://github.com/pledge4future/co2calculator/blob/dev/data/conversion_factors_heating.csv)):
- Oil: l
- Liquid gas, Coal, Pellet, Woodchips: kg
- Gas: m<sup>3</sup>
The conversion factors are retrieved from:
- [BAFA (2020): Merkblatt zur Ermittlung des Gesamtenergieverbrauchs](https://www.bafa.de/SharedDocs/Downloads/DE/Energie/ea_ermittlung_gesamtenergieverbrauch.html)
- [Krajnc, N. (2015): Wood fuels handbook, FAO](https://agris.fao.org/agris-search/search.do?recordID=XF2017001919)

The emission factors depend on the fuel type. Fuel types may be oil, gas, liquid gas, electricity, coal, district heating, different types of heat pumps (ground, air, water), pellet, woodchips and solar.

## 3 Business trips

The `co2calculator` allows to quantify the emissions for individual business trips for different modes of transport. The CO<sub>2</sub> equivalent is a function of the distance travelled in km. This distance may either be directly provided, or it may be computed from given start and stop locations using [distances.py](https://github.com/pledge4future/co2calculator/blob/dev/co2calculator/distances.py). In the latter case, the coordinates of the locations have to be retrieved by geocoding and then the travel distance between the locations is computed. Next to the distance or the locations, the user defines the mode of transport and its specifica.

### Geocoding

Geocoding is done using the [openrouteservice](https://openrouteservice.org/dev/#/api-docs) geocoding service, which is built on top of the [Pelias](https://github.com/pelias/pelias), a modular, open-source search engine for the world.

To find airports [geocoding_airport](https://github.com/pledge4future/co2calculator/blob/ffc12ec577cb18bf7c67b628ff7d9d79ffeef25b/co2calculator/distances.py#L39), we use [Pelias search](https://github.com/pelias/documentation/blob/master/search.md) with the search text "Airplane" + **IATA-code**. For other modes of transport, we use [structured geocoding](https://github.com/pelias/documentation/blob/master/structured-geocoding.md) ([geocoding_structured](https://github.com/pledge4future/co2calculator/blob/ffc12ec577cb18bf7c67b628ff7d9d79ffeef25b/co2calculator/distances.py#L92)). The structured geocoding parameters are:
- country: highest-level administrative division supported in a search. Full country name or two-/three-letter abbreviations supported
    - e.g., Germany / "DE" / "DEU"
- region: first-level administrative divisions within countries, analogous to states and provinces in the US and Canada
    - e.g., Delaware, Ontario, Ardennes, Baden-Württemberg
- county: administrative divisions between localities and regions
    - e.g., Alb-Donau-Kreis
- locality: equivalent to what are commonly referred to as cities (also municipalities)
    - e.g., Bangkok, Caracas
- borough: mostly known in the context of NY, may exist in other cities like Mexico City
    - e.g. Manhatten in NY, Iztapalapa in Mexico City
- postalcode: postal code; note: This may not work for all countries!
    - e.g., it works for the US and the UK, but not for Germany (and other countries)
- address: street name, optionally also house number
- neighbourhood: vernacular geographic entities that may not necessarily be official administrative divisions but are important nonetheless
    - e.g. Notting Hill in London, Le Marais in Paris

### Distance computation

For cars and motorbikes, distances are computed with [openrouteservice](https://openrouteservice.org/dev/#/api-docs/directions) with the `profile='driving-car'`.

For other modes of transport (airplane, ferry, train, bus), the distances between the locations as the crow flies are computed with the [haversine formula](https://github.com/pledge4future/co2calculator/blob/ffc12ec577cb18bf7c67b628ff7d9d79ffeef25b/co2calculator/distances.py#L20). Then, different detour coefficients or constants are applied.
With the `roundtrip`-parameter (type: boolean), users can define if their trip is a roundtrip and if so, the distance will be doubled. 

#### Detour

Trips on earth will always make a detour, because it is usually not possible to travel in a straight line from start to destination. Therefore, we use coefficients and constants to account for this detour. These differ depending on the mode of travel. 

Mode of transport | Detour formula | Source 
------------ | ------------- | -------------
Bus | x 1.5 | Adapted from [GES 1point5](https://labos1point5.org/ges-1point5), who were advised by Frédéric Héran (economist and urban planner).
Train | x 1.2 | Adapted from [GES 1point5](https://labos1point5.org/ges-1point5), who were advised by Frédéric Héran (economist and urban planner).
Plane | + 95 km | CSN EN 16258 - Methodology for calculation and declaration of energy consumption and GHG emissions of transport services (freight and passengers), European Committee for Standardization, Brussels, November 2012, [Méthode pour la réalisation des bilans d’émissions de gaz à effet de , Version 4](https://www.ecologie.gouv.fr/sites/default/files/Guide%20m%C3%A9thodologique%20sp%C3%A9cifique%20pour%20les%20collectivit%C3%A9s%20pour%20la%20r%C3%A9alisation%20du%20bilan%20d%E2%80%99%C3%A9missions%20de%20GES.pdf), p. 53
Ferry | ??? | ???

### Specifica of the modes of transport

Mode of transport | Fuel type | Size | Occupancy | Seating | Passengers | Range 
------------ | ------------- | ------------- | ------------ | ------------- | ------------- | -------------
Car | [diesel, gasoline, cng, electric, average] | [small, medium, large, average] | - | - | [1..9] | -
Motorbike | - | [small, medium, large, average] | - | - | - | -
Train | [diesel, electric, average] | - | - | - | - | - (assumes "long-distance")
Bus | - | [medium, large, average] | in % [20, 50, 80, 100] | - | - | - (assumes "long-distance")
Plane | - | - | - | [average, Economy class, Business class, Premium economy class, First class] | - | - (determined from distance)
Ferry | - | - | - | [average, Foot passenger, Car passenger] | - | -

These specifica determine how high the emission factors (in kg CO<sub>2</sub>e/km) are. 

## 4 Commuting 

Emissions from commuting are also quantified individually for each mode of transport [calc_co2_commuting](https://github.com/pledge4future/co2calculator/blob/ffc12ec577cb18bf7c67b628ff7d9d79ffeef25b/co2calculator/calculate.py#L316). For a given mode of transport, the user provides the average weekly distance travelled in a given time period (`work_weeks`). Available transportation modes are:
- Car
- (Local) bus
- (Local) train
- Tram
- Motorbike
- Bicycle
- Pedelec

### Specifica of the modes of transport

Again, the characteristics of the modes of transport influence the specific emission factors.

Mode of transport | Fuel type | Size | Occupancy | Seating | Passengers | Range 
------------ | ------------- | ------------- | ------------ | ------------- | ------------- | -------------
Car | [diesel, gasoline, cng, electric, average] | [small, medium, large, average] | - | - | [1..9] | -
Motorbike | - | [small, medium, large, average] | - | - | - | -
Train | [diesel, electric, average] | - | - | - | - | - (assumes "local")
Bus | - | [medium, large, average] | in % [20, 50, 80, 100] | - | - | - (assumes "local")
Tram | - | [medium, large, average] | in % [20, 50, 80, 100] | - | - | - (assumes "local")
Bicycle | - | - | - | - | - | -
Pedelec | - | - | - | - | - | -

### Aggregating to the group's level

If we assume that a representative sample (`n_participants`) of the entire group (`n_member`) entered their commuting data, we can obtain an estimate of the commuting emissions for the entire group:

`group_co2e = aggr_co2 / n_participants * n_members` 
with `aggr_co2` the sum of the CO<sub>2</sub>e emissions of all participants.
