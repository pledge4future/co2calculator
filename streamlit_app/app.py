#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""streamlit app"""


import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import co2calculator as co2
from co2calculator.api.trip import Trip
from co2calculator.parameters import *

st.title("Co2claculator")
st.write("You can only enter cities in Germany")

# user input
start_input = st.text_input("Start of your trip", placeholder="z. B. Berlin")
end_input = st.text_input("Destination of your trip", placeholder="z. B. München")

# convert input to dict
start = {"locality": start_input, "country": "Germany"}
end = {"locality": end_input, "country": "Germany"}

if st.button("Calculate"):
    if start and end:
        trip = Trip(start=start, destination=end)
        car = trip.by_car().calculate_co2e()
        train = trip.by_train().calculate_co2e()
        # plane = trip.by_plane().calculate_co2e()
        co2e = car.co2e, train.co2e
        transportmode = ["car", "train"]

        fig, ax = plt.subplots()
        ax.bar(transportmode, co2e)
        ax.set_title(f"CO2-Emissions from {start_input} to {end_input}")
        ax.set_xlabel("Transport mode")
        ax.set_ylabel("CO2 in kg")

        st.pyplot(fig)
    else:
        st.warning("Bitte beide Felder ausfüllen.")
