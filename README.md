# CO<sub>2</sub> Calculator 

Python package to calculate CO2 emissions of business trips, heating and electricity consumption.

## Description

This package is part of Pledge4Future, a project to quantify, monitor and reduce work-related emissions collectively and sustainably. [more info, Link to Website]

## How to Use

[...]

The CO<sub>2</sub> Calculator uses the [OpenRouteService (ORS) API](https://openrouteservice.org/dev/#/api-docs) to obtain distances between the locations provided by the user to calculate CO<sub>2</sub> emissions of business trips. This requires an API key, which is read from an `.env` file.

### Create an ORS API key and save it in your .env file

1) Go to https://openrouteservice.org/dev/#/signup and create an account (or sign up with GitHub).
2) In the Dev dashboard, switch to the tab `TOKENS` and request a free token.
3) Once you have the key, click on it to copy it to clipboard.
4) Insert the key into [sample.env](https://github.com/pledge4future/co2calculator/blob/dev_ors/sample.env) and rename the file to `.env`.

## References

### Emission factors

- [Probas](https://www.probas.umweltbundesamt.de/php/index.php)
- [UBA - "Umweltfreundlich mobil"](https://www.umweltbundesamt.de/en/publikationen/umweltfreundlich-mobil)

### Detour coefficients and constants

- Detour constant of 95 km for plane trips:
    - CSN EN 16258 - Methodology for calculation and declaration of energy consumption and GHG emissions of transport services (freight and passengers), European Committee for Standardization, Brussels, November 2012
    - [Méthode pour la réalisation des bilans d’émissions de gaz à effet de , Version 4](https://www.ecologie.gouv.fr/sites/default/files/Guide%20m%C3%A9thodologique%20sp%C3%A9cifique%20pour%20les%20collectivit%C3%A9s%20pour%20la%20r%C3%A9alisation%20du%20bilan%20d%E2%80%99%C3%A9missions%20de%20GES.pdf), p. 53
- Detour coefficients for train trips (1.2) and bus trips (1.5):
    - Adapted from [GES 1point5](https://labos1point5.org/ges-1point5), who were advised by Frédéric Héran (economist and urban planner).

## Project partners

[...]
