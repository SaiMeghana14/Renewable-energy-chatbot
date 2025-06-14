import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from gtts import gTTS
import os
from io import BytesIO
import base64

st.set_page_config(page_title="Renewable Awareness Chatbot", layout="wide")
st.title("🌱 Renewable Awareness Chatbot + Insights")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("renewables_enhanced.csv")
    df["Total_GW"] = df[["Solar_GW", "Wind_GW", "Hydro_GW", "Biomass_GW", "Geothermal_GW"]].sum(axis=1)
    df["Region"] = df["Country"].map({
        "India": "Asia", "China": "Asia", "USA": "North America", "Germany": "Europe",
        "Brazil": "South America", "Australia": "Oceania", "South Africa": "Africa",
        "UK": "Europe", "France": "Europe", "Canada": "North America"
    }).fillna("Other")
    return df

df = load_data()

# Sidebar for selecting country and year
country = st.sidebar.selectbox("Select Country", sorted(df["Country"].unique()))
year = st.sidebar.selectbox("Select Year", sorted(df["Year"].unique(), reverse=True))

# Get specific row
data = df[(df["Country"] == country) & (df["Year"] == year)].iloc[0]

# Quick FAQ buttons
st.subheader("💡 Quick Questions")
faq = st.radio("Pick a question:", [
    f"What is the top renewable source in {country}?",
    f"Compare Wind and Solar in {country}",
    f"Show renewable mix for {country} in {year}"
])

# Generate a response for FAQ
def faq_response(faq):
    if "top renewable" in faq:
        max_source = data[["Solar_GW", "Wind_GW", "Hydro_GW", "Biomass_GW", "Geothermal_GW"]].idxmax()
        source_name = max_source.replace("_GW", "")
        value = data[max_source]
        return f"In {country}, the top renewable source is {source_name} with {value} GW capacity."
    elif "Compare Wind and Solar" in faq:
        return f"In {country}, Solar: {data['Solar_GW']} GW | Wind: {data['Wind_GW']} GW."
    elif "renewable mix" in faq:
        mix = ", ".join([f"{k.replace('_GW','')}: {v} GW" for k, v in data.items() if k.endswith("_GW")])
        return f"Here is the renewable mix for {country} in {year} → {mix}"

st.info(faq_response(faq))

# 🧠 Natural Language Chatbot Interface
st.subheader("🧠 Ask Your Own Question")
user_query = st.text_input("Type a question about renewable energy:")

def answer_query(query):
    query = query.lower()
    if country.lower() in query:
        if "solar" in query:
            return f"{country} has {data['Solar_GW']} GW of solar capacity in {year}."
        elif "wind" in query:
            return f"{country} has {data['Wind_GW']} GW of wind capacity in {year}."
        elif "hydro" in query:
            return f"{country} has {data['Hydro_GW']} GW of hydropower in {year}."
        elif "biomass" in query:
            return f"{country} has {data['Biomass_GW']} GW of biomass capacity."
        elif "geothermal" in query:
            return f"{country} has {data['Geothermal_GW']} GW of geothermal capacity."
        elif "total" in query or "overall" in query:
            return f"{country}'s total renewable capacity is {data['Total_GW']} GW."
    return "🤖 I'm still learning. Try asking about solar, wind, hydro, biomass, or geothermal."

if user_query:
    response = answer_query(user_query)
    st.success(response)

    # Optional Text-to-Speech
    tts = gTTS(text=response, lang='en')
    mp3_fp = BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    b64 = base64.b64encode(mp3_fp.read()).decode()
    st.audio(f"data:audio/mp3;base64,{b64}", format="audio/mp3")

# Footer
st.markdown("---")
st.info("This chatbot is part of the 1M1B Green Internship project. Type a question or choose from the FAQ!")
