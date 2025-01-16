#!/usr/bin/env python
# coding: utf-8
"""WePledge has a python backend which uses co2calculator to number crunching.
To ensure that the backend never has problems making existing calls, functional
testing happens here.
Functional testing should test all methods called at lower levels. External calls
shall be mocked.
Overview of used methods form backend:
    - calc_co2_businesstrip,
    - calc_co2_commuting,
    - calc_co2_electricity,
    - calc_co2_heating,
"""

import pytest
from co2calculator import calculate as candidate


class TestCalculateCommuting:
    """Functional testing of `calc_co2_commuting` calls from backend"""

    @pytest.mark.parametrize(
        "transportation_mode,expected_emissions",
        [
            pytest.param("car", 9.03, id="transportation_mode: 'car'"),
            pytest.param("bus", 1.65, id="transportation_mode: 'bus'"),
            pytest.param("train", 1.38, id="transportation_mode: 'train'"),
            pytest.param("bicycle", 0.38, id="transportation_mode: 'bicycle'"),
            pytest.param("pedelec", 0.63, id="transportation_mode: 'pedelec'"),
            pytest.param("motorbike", 4.77, id="transportation_mode: 'motorbike'"),
            pytest.param("tram", 2.3, id="transportation_mode: 'tram'"),
        ],
    )
    def test_calc_co2_commuting(
        self, transportation_mode: str, expected_emissions: float
    ) -> None:
        """SCENARIO: pledge4future's backend calls `calc_co2_commuting`
        TEST: Main interface calls do not fail, return emissions
        """

        actual_emissions = candidate.calc_co2_commuting(
            transportation_mode=transportation_mode, weekly_distance=42
        )

        assert isinstance(actual_emissions[0], float)
