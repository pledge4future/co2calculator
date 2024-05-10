# CO<sub>2</sub>Calculator

[![status: experimental](https://github.com/GIScience/badges/raw/master/status/experimental.svg)](https://github.com/GIScience/badges#experimental)

Python package to calculate work related CO2 emissions from heating and electricity consumption as well as business trips and commuting.

## ℹ️  Description

This package is part of [Pledge4Future](https://pledge4future.org/), a project to quantify, monitor and reduce work-related emissions collectively and sustainably. 

## :computer:  Installation

### With pip (recommended)

PyPi release coming soon!

<!--The recommended way to install this package is with pip from the Python Package Index ([PyPi](https://pypi.org/)):

```
pip install -U co2calculator
```-->

### From source

To install this package from source, clone the repository as usual, for example with:

``` 
git clone https://github.com/pledge4future/co2calculator.git
cd co2calculator
```

This package requires Python 3.10, 3.11 or 3.12 and can be installed using [poetry](https://python-poetry.org/). You can install it in your (virtual) environment with:

```
$ pip install -U poetry
$ poetry install --no-root
```


## ⌨  How to Use

Learn how to use `co2calculator` in our detailed [documentation](https://github.com/pledge4future/co2calculator/blob/dev/docs/documentation.md). [...]

The CO<sub>2</sub> Calculator uses the [OpenRouteService (ORS) API](https://openrouteservice.org/dev/#/api-docs) to obtain distances between the locations provided by the user to calculate CO<sub>2</sub> emissions of business trips. This requires an API key, which is read from an `.env` file.

### Create an ORS API key and save it in your .env file

1) Go to https://openrouteservice.org/dev/#/signup and create an account (or sign up with GitHub).
2) In the Dev dashboard, switch to the tab `TOKENS` and request a free token.
3) Once you have the key, click on it to copy it to clipboard.
4) Insert the key into [sample.env](sample.env) and rename the file to `.env`.

## :couple:  Contribution guidelines

If you want to contribute to this project, please fork this repository and create a pull request with your suggested changes.


### Install pre-commit hooks

To ensure coding style we use pre-commit hooks. Install them locally using

```
$ pre-commit install
```

They will be run automatically every time you try to create a commit. `black` will adapt the code automatically to
conform to PEP8 code style. After this has been done you may need to add the file again to the staging area.

### Run tests

After you have made changes to the code, run the units tests by executing

```
$ pytest
```

## 📄 References

### Emission factors

- [Carbon footprint (2023). International electricity factors](https://www.carbonfootprint.com/international_electricity_factors.html)
- [GOV.UK (2023). Greenhouse gas reporting: conversion factors 2023](https://www.gov.uk/government/publications/greenhouse-gas-reporting-conversion-factors-2023)
- [mobitoool (2023). mobitool-Faktoren v3.0](https://www.mobitool.ch/de/tools/mobitool-faktoren-v2-1-25.html)

### Conversion factors

- [BAFA (2020): Merkblatt zur Ermittlung des Gesamtenergieverbrauchs](https://www.bafa.de/SharedDocs/Downloads/DE/Energie/ea_ermittlung_gesamtenergieverbrauch.html)
- [Krajnc, N. (2015): Wood fuels handbook, FAO](http://large.stanford.edu/courses/2017/ph240/timcheck1/docs/fao-krajnc-2015.pdf)

### Detour coefficients and constants

- Detour constant of 95 km for plane trips:
    - CSN EN 16258 - Methodology for calculation and declaration of energy consumption and GHG emissions of transport services (freight and passengers), European Committee for Standardization, Brussels, November 2012
    - [Méthode pour la réalisation des bilans d’émissions de gaz à effet de , Version 4](https://www.ecologie.gouv.fr/sites/default/files/Guide%20m%C3%A9thodologique%20sp%C3%A9cifique%20pour%20les%20collectivit%C3%A9s%20pour%20la%20r%C3%A9alisation%20du%20bilan%20d%E2%80%99%C3%A9missions%20de%20GES.pdf), p. 53
- Detour coefficients for train trips (1.2) and bus trips (1.5):
    - Adapted from [GES 1point5](https://labos1point5.org/ges-1point5), who were advised by Frédéric Héran (economist and urban planner).

### Airports and Train Stations

- [OurAirports](https://ourairports.com/data/)
- [Stations - A Database of European Train Stations (Trainline EU)](https://github.com/trainline-eu/stations)

## 🤝 Project partners

- [openrouteservice](https://openrouteservice.org/)

## ⚖️ License

See [License](LICENSE)
