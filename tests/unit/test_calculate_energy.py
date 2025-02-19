"""tests for energy calculation"""

import co2calculator.energy.calculate_energy as energy
import pytest


@pytest.mark.parametrize(
    "consumption,func_options,co2e_kg_expected",
    [
        pytest.param(250, {"fuel_type": "wood chips", "in_kwh": True}, 2.685),
        pytest.param(250, {"fuel_type": "wood chips"}, 13.962),
    ],
)
def test_heating_woodchips(
    consumption: float, func_options: dict, co2e_kg_expected: float
):
    """Test co2e calculation for heating: wood chips"""

    # Calculate co2e
    co2e, _, _ = energy.calc_co2_heating(consumption=consumption, options=func_options)

    # Check if expected result matches calculated result
    assert co2e == pytest.approx(co2e_kg_expected, rel=0.01)


@pytest.mark.parametrize(
    "consumption_kwh,func_options,co2e_kg_expected",
    [
        pytest.param(
            10000, {"fuel_type": "production fuel mix", "country_code": "DE"}, 4491.2
        ),
        pytest.param(
            10000, {"fuel_type": "production fuel mix", "country_code": "FR"}, 620.7
        ),
    ],
)
def test_electricity(
    consumption_kwh: float, func_options: dict, co2e_kg_expected: float
):
    """Test co2e calculation for electricity"""

    # Calculate co2e
    co2e, _, _ = energy.calc_co2_electricity(
        consumption=consumption_kwh, options=func_options
    )

    # Check if expected result matches calculated result
    assert co2e == pytest.approx(co2e_kg_expected, rel=0.01)
