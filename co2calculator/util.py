"""Generic collection of util functions and maps."""

from co2calculator.constants import TransportationMode
from co2calculator.mobility.calculate_mobility import (
    calc_co2_bicycle,
    calc_co2_bus,
    calc_co2_car,
    calc_co2_motorbike,
    calc_co2_pedelec,
    calc_co2_train,
    calc_co2_tram,
)
import os
import openrouteservice
from .exceptions import InvalidORSApiKey, MissingORSApiKey

api_key_check_cords = ((8.34234, 48.23424), (8.34423, 48.26424))


def get_calc_function_from_transport_mode(
    transport_mode: TransportationMode,
) -> callable:
    transportation_mode_calc_function_map = {
        TransportationMode.CAR: calc_co2_car,
        TransportationMode.MOTORBIKE: calc_co2_motorbike,
        TransportationMode.BUS: calc_co2_bus,
        TransportationMode.TRAIN: calc_co2_train,
        TransportationMode.BICYCLE: calc_co2_bicycle,
        TransportationMode.TRAM: calc_co2_tram,
        #        TransportationMode.FERRY: calc_co2_ferry,
        TransportationMode.PEDELEC: calc_co2_pedelec,
    }
    return transportation_mode_calc_function_map[transport_mode]


def get_ors_api_key() -> str:
    """Utility to load and validate the ORS API key from environment."""
    api_key = os.environ.get("ORS_API_KEY")
    if api_key is None:
        raise MissingORSApiKey(
            "ORS API key is missing. Please set the ORS_API_KEY environment variable using the `co2calculator.set_ors_apikey` function."
        )
    return api_key


def get_ors_client():
    """Utility to load and validate the ORS API key and return a ready-to-use client."""
    api_key = get_ors_api_key()
    client = openrouteservice.Client(key=api_key)
    try:
        client.directions(api_key_check_cords)
        return client
    except Exception:
        raise InvalidORSApiKey(
            "Failed to create ORS client. This is most likely due to an invalid API key."
        )
