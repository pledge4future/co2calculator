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
from typing import Dict
import pytest

from co2calculator import calculate as candidate


class TestCalculateBusinessTrip:
    """Functional testing of business trip calculation calls from backend"""

    @pytest.mark.parametrize(
        "transportation_mode, expected_emissions",
        [
            pytest.param("car", 9.03, id="transportation_mode: 'car'"),
            pytest.param("bus", 1.65, id="transportation_mode: 'bus'"),
            pytest.param("train", 1.38, id="transportation_mode: 'train'"),
        ],
    )
    def test_business_trip__distance_based(
        self, transportation_mode: str, expected_emissions: float
    ) -> None:
        """Scenario: Backend asks for business trip calculation with distance input.
        Test: co2 calculation for business trip
        Expect: Happy path
        """
        actual_emissions, _, _, _ = candidate.calc_co2_businesstrip(
            transportation_mode=transportation_mode,
            start=None,
            destination=None,
            distance=42.0,
            size=None,
            fuel_type=None,
            occupancy=None,
            seating=None,
            passengers=None,
            roundtrip=False,
        )

        assert round(actual_emissions, 2) == expected_emissions

    @pytest.mark.parametrize(
        "transportation_mode, start, destination, expected_emissions",
        [
            pytest.param(
                "car",
                {
                    "address": "Im Neuenheimer Feld 348",
                    "locality": "Heidelberg",
                    "country": "Germany",
                },
                {
                    "country": "Germany",
                    "locality": "Berlin",
                    "address": "Alexanderplatz 1",
                },
                134720.48,
                id="transportation_mode: 'car'",
            ),
        ],
    )
    def test_business_trip__stops_based(
        self,
        transportation_mode: str,
        start: Dict,
        destination: Dict,
        expected_emissions: float,
    ) -> None:
        """Scenario: Backend asks for business trip calculation with distance input.
        Test: co2 calculation for business trip
        Expect: Happy path
        """
        # NOTE: IMPORTANT - Test currently makes real web calls!
        # TODO: Mock!
        actual_emissions, _, _, _ = candidate.calc_co2_businesstrip(
            transportation_mode=transportation_mode,
            start=start,
            destination=destination,
            distance=None,
            size=None,
            fuel_type=None,
            occupancy=None,
            seating=None,
            passengers=None,
            roundtrip=False,
        )

        assert round(actual_emissions, 2) == expected_emissions
