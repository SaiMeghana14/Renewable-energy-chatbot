import pandas as pd
import streamlit as st

@st.cache_data
def load_data():

    df = pd.read_csv("data/renewables_enhanced_augmented.csv")

    energy_cols = [
        "Solar_GW",
        "Wind_GW",
        "Hydro_GW",
        "Biomass_GW",
        "Geothermal_GW"
    ]

    numeric_cols = energy_cols + [
        "Population_M",
        "GDP_Billion_USD"
    ]

    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric)

    df["Total_GW"] = df[energy_cols].sum(axis=1)

    return df
