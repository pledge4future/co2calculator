"""Generic collection of util functions and maps."""

from co2calculator.constants import TransportationMode
from co2calculator.mobility.calculate_mobility import (
    calc_co2_bicycle,
    calc_co2_bus,
    calc_co2_car,
    #    calc_co2_ferry,
    calc_co2_motorbike,
    calc_co2_pedelec,
    calc_co2_train,
    calc_co2_tram,
)


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
