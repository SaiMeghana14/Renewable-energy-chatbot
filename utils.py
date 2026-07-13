from pathlib import Path

import pandas as pd
import streamlit as st


@st.cache_data
def load_data():
    """
    Load and preprocess the renewable energy dataset.
    """

    # Path to the CSV file
    csv_path = Path(__file__).parent / "data" / "renewables_enhanced_augmented.csv"

    # Read dataset
    df = pd.read_csv(csv_path)

    energy_cols = [
        "Solar_GW",
        "Wind_GW",
        "Hydro_GW",
        "Biomass_GW",
        "Geothermal_GW",
    ]

    numeric_cols = energy_cols + [
        "Population_M",
        "GDP_Billion_USD",
    ]

    # Convert numeric columns
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")

    # Calculate total renewable capacity
    df["Total_GW"] = df[energy_cols].sum(axis=1)

    # Remove rows with missing values (optional but recommended)
    df = df.dropna()

    return df
