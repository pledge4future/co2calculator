"""tests for energy calculation"""
import co2calculator.energy.calculate_energy as energy
import pytest


def test_heating_woodchips():
    """Test co2e calculation for heating: woodchips"""
    # Given parameters
    consumption = 250
    co2e_kg_expected = 43.63

    func_options = {
        # Given parameters
        "heating_emission_parameters": {
            "fuel_type": "wood chips"  # emission factor: 9322 kg/TJ
        },
        "unit": "kg",  # conversion factor to kWh = 5.4
    }

    # Calculate co2e
    co2e = energy.calc_co2_heating(consumption=consumption, options=func_options)

    # Check if expected result matches calculated result
    assert co2e == pytest.approx(co2e_kg_expected, rel=0.01)


def test_electricity():
    """Test co2e calculation for electricity"""
    # Given parameters
    fuel_type = "german_energy_mix"
    consumption_kwh = 10000
    co2e_kg_expected = 3942.65  # emission factor: 109518 kg/TJ

    func_options = {
        "electricity_emission_parameters": {
            "fuel_type": "german_energy_mix"  # emission factor: 109518 kg/TJ
        }
    }

    # Calculate co2e
    co2e = energy.calc_co2_electricity(
        consumption=consumption_kwh, options=func_options
    )

    # Check if expected result matches calculated result
    assert co2e == pytest.approx(co2e_kg_expected, rel=0.01)
