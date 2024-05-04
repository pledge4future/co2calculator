# Documentation of CO<sub>2</sub> calculations

The *co2calculator* can compute emissions caused by mobility, heating and electricity consumption. Emissions are given as CO<sub>2</sub> equivalents (CO<sub>2</sub>e). 

## 1 General information
### What are CO2 e-emissions?

Anthropogenic climate change is caused by greenhouse gases, such as carbon dioxide ($CO_2$), methane ($CH_4$), nitrous oxides ($N_2O$) and others. The molecules of these gases contribute differently to global warming. For example, the impact of one methane molecule is 21 times higher than the impact caused by one carbon dioxide molecule [(Moss et al. 2000)](https://animres.edpsciences.org/articles/animres/abs/2000/03/z0305/z0305.html). This is why the impact of different greenhouse gases is usually converted to the equivalent impact that carbon dioxide molecules would have, resulting in $CO_2$ equivalents as a standard unit [(Gohar & Shine 2007)](https://rmets.onlinelibrary.wiley.com/doi/10.1002/wea.103). The basic formula for a consumption value $c$ and an emission factor $\epsilon$ is:

```{math}
y_{CO^2} = \epsilon \cdot c
```

### Emission factor sources

The CO<sub>2</sub>e emissions are calculated using emission factors from different sources:
- Electricity: [carbon footprint (2023). International electricity factors.](https://www.carbonfootprint.com/international_electricity_factors.html)
- Mobility: [mobitoool (2023). mobitool-Faktoren v3.0](https://www.mobitool.ch/de/tools/mobitool-faktoren-v2-1-25.html)
- Heating: [GOV.UK (2023). Greenhouse gas reporting: conversion factors 2023](https://www.gov.uk/government/publications/greenhouse-gas-reporting-conversion-factors-2023)

The specific emission factors for different activities are collected in [this emission factor table](https://github.com/pledge4future/co2calculator/blob/dev/data/emission_factors.csv).

(heading-target)=
### Compliance with the GHG Protocols

The Greenhouse Gas (GHG) Protocol Corporate Standards provide a globally used framework to measure greenhouse gas emissions [(Greenhouse Gas Protocol 2024)](https://ghgprotocol.org/). They account for three scopes:
* Scope 1 emissions are direct emissions from sources that are owned or controlled by the reporting entity, such as emissions from combustion in owned vehicles or boilers. 
* Scope 2 emissions are indirect emissions caused by the generation of purchased or consumed electricity, heating, cooling or steam.
* Scope 3 emissions are indirect emissions other than those captured in scope 3. These include all other emissions generated in the life cycle of the product, including production and disposal.

For electricity and mobility, the *co2calculator* computes emissions based on the whole life cycle of a product, i.e. including scope 3 emissions. For heating, scope 1 emissions are caculated.


## 1 Electricity

Electricity CO<sub>2</sub>e emissions are calculated from country-specific production mixes [(carbon footprint 2023)](https://www.carbonfootprint.com/international_electricity_factors.html). These are the mix of fuels used by local power stations and, therefore, the basis for location-based reporting. Emission factors rely on total production fuel mixes, which include scope 2 and scope 3 emissions of the GHG protocol (for details, see [Compliance with the GHG Protocols](#heading-target)). 


### Calculation of a share of electricity use

If the electricity consumption is only known for a building or building complex and emissions should only be computed for parts of the building, the total consumption and an estimate of the share of energy use (approximated from the share of the building area) can be provided.


## 2 Heating

Heating CO<sub>2</sub>e emissions depend on the type of burned fuel. Fuel types may be, for example, oil, gas, coal or biogas. The emissions are calculated using emission factors from [(GOV.UK 2023)](https://www.gov.uk/government/publications/greenhouse-gas-reporting-conversion-factors-2023). The provided emission factors reflect scope 1 emissions of the GHG protocol (for details, see [Compliance with the GHG Protocols](#heading-target)).

### Calculation of a share of heating consumption

If the heating consumption is only known for a building or building complex and emissions should only be computed for parts of the building, the total consumption and an estimate of the share of energy use (approximated from the share of the building area) can be provided.


## 3 Mobility

CO<sub>2</sub>e emissions from the mobility sector are calculated using emission factors from [(mobitoool 2023)](https://www.mobitool.ch/de/tools/mobitool-faktoren-v2-1-25.html). The emissions include scope 3 emissions of the GHG protocol (for details, see [Compliance with the GHG Protocols](#heading-target)). 

Mobility emissions depend on the mode of transport, such as car or bicycle, and the distance travelled. This distance may either be directly provided, or it may be computed from given start and stop locations using [distances.py](https://github.com/pledge4future/co2calculator/blob/dev/co2calculator/distances.py). In the latter case, the coordinates of the locations are retrieved using geocoding before the travel distance between the locations is computed (for details, see [Geocoding](#heading-target)).

(heading-target)=
### Geocoding

Geocoding is done using the [openrouteservice](https://openrouteservice.org/dev/#/api-docs) geocoding service, which is built on top of [Pelias](https://github.com/pelias/pelias), a modular open-source search engine for the world.

To find airports [geocoding_airport](https://github.com/pledge4future/co2calculator/blob/5ac4e624f742f404299276e013f0f0194e5ba6da/co2calculator/distances.py#L45), we use [Pelias search](https://github.com/pelias/documentation/blob/master/search.md) with the search text "Airplane" + **IATA-code**. To find train stations inside the EU [geocoding_train_stations](https://github.com/pledge4future/co2calculator/blob/5ac4e624f742f404299276e013f0f0194e5ba6da/co2calculator/distances.py#L156), we use the train station database of [Trainline EU](https://github.com/trainline-eu/stations). For train trips outside of the EU and other modes of transport, we use [structured geocoding](https://github.com/pelias/documentation/blob/master/structured-geocoding.md) ([geocoding_structured](https://github.com/pledge4future/co2calculator/blob/5ac4e624f742f404299276e013f0f0194e5ba6da/co2calculator/distances.py#L98)). The structured geocoding parameters are:
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
