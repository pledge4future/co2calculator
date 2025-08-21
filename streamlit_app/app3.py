#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""streamlit app"""

import streamlit as st
import seaborn as sns
import base64

import sys
import os

import pandas as pd
import matplotlib.pyplot as plt
from co2calculator.api.trip import Trip

project_path = os.path.abspath(
    "/Users/milenaschnitzler/Documents/originalCO2/co2calculator"
)
if project_path not in sys.path:
    sys.path.insert(0, project_path)


logo_pledge = "/Users/milenaschnitzler/Documents/originalCO2/Final_logo.png"
with open(logo_pledge, "rb") as image_file:
    encoded = base64.b64encode(image_file.read()).decode()

# import logo as HTML
st.markdown(
    f"""
    <style>
        .logo-container {{
            position: fixed;
            top: 10px;
            left: 10px;
            z-index: 100;
        }}
        .logo-container img {{
            width: 200px;
        }}
    </style>
    <div class="logo-container">
        <img src="data:image/png;base64,{encoded}" alt="Logo">
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<h1 style='color: #4A4A4A;'>CO2calculator</h1>", unsafe_allow_html=True)
st.write("You can only enter cities in Germany")

# user input
start_input = st.text_input("Start of your trip", placeholder="z. B. Berlin")
end_input = st.text_input("Destination of your trip", placeholder="z. B. München")

if st.button("Calculate"):
    if start_input.strip() and end_input.strip():

        start = {"locality": start_input, "country": "Germany"}
        end = {"locality": end_input, "country": "Germany"}

        trip = Trip(start=start, destination=end)
        car = trip.by_car().calculate_co2e()
        train = trip.by_train().calculate_co2e()
        plane = trip.by_plane().calculate_co2e()
        motorbike = trip.by_motorbike().calculate_co2e()

        co2e = car.co2e, train.co2e, plane.co2e, motorbike.co2e
        transportmode = ["Car", "Train", "Plane", "Motorbike"]

        df = pd.DataFrame({"Transport mode": transportmode, "CO2 in kg": co2e})

        logo_colors = ["#FF7518", "#283C92", "#49AFF1", "#FF1200"]

        fig, ax = plt.subplots(figsize=(8, 6))
        sns.barplot(
            data=df, x="Transport mode", y="CO2 in kg", palette=logo_colors, ax=ax
        )
        ax.set_title(f"CO2-Emissions for your trip from {start_input} to {end_input}")
        ax.set_xlabel("Transport mode")
        ax.set_ylabel("CO2 in kg")
        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.warning("Please enter input for both fields.")
