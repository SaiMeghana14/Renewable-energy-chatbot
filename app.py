
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Renewable Awareness Chatbot", layout="wide")
st.title("🌿 Renewable Energy Awareness Chatbot + Insights")

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

# Sidebar selection
country = st.sidebar.selectbox("Select a Country", sorted(df["Country"].unique()))
year = st.sidebar.selectbox("Select a Year", sorted(df["Year"].unique(), reverse=True))

# Filter data
data = df[(df["Country"] == country) & (df["Year"] == year)]

if not data.empty:
    st.subheader(f"🔍 Overview for {country} ({year})")

    # Pie Chart for Renewable Mix
    energy_sources = ["Solar_GW", "Wind_GW", "Hydro_GW", "Biomass_GW", "Geothermal_GW"]
    sizes = data[energy_sources].values.flatten()
    labels = ["Solar", "Wind", "Hydro", "Biomass", "Geothermal"]

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140)
    ax.axis("equal")
    st.pyplot(fig)

    # Key Metrics
    st.metric("Population (Millions)", data["Population_M"].values[0])
    st.metric("GDP (Billion USD)", data["GDP_Billion_USD"].values[0])
    st.metric("Total Renewable Capacity (GW)", round(data["Total_GW"].values[0], 2))

# Trend over years
st.subheader("📈 Renewable Growth Over Years")
trend_df = df[df["Country"] == country].sort_values("Year")
plt.figure(figsize=(10, 4))
plt.plot(trend_df["Year"], trend_df["Solar_GW"], label="Solar")
plt.plot(trend_df["Year"], trend_df["Wind_GW"], label="Wind")
plt.plot(trend_df["Year"], trend_df["Hydro_GW"], label="Hydro")
plt.legend()
plt.xlabel("Year")
plt.ylabel("Capacity (GW)")
plt.title(f"{country} Renewable Growth Over Time")
st.pyplot(plt)

# Comparison Tool
st.subheader("🔄 Country Comparison")
col1, col2 = st.columns(2)
with col1:
    country1 = st.selectbox("Country 1", df["Country"].unique(), index=0)
with col2:
    country2 = st.selectbox("Country 2", df["Country"].unique(), index=1)

d1 = df[(df["Country"] == country1) & (df["Year"] == year)].iloc[0]
d2 = df[(df["Country"] == country2) & (df["Year"] == year)].iloc[0]

comparison_df = pd.DataFrame({
    "Source": labels,
    country1: d1[energy_sources].values,
    country2: d2[energy_sources].values
})
st.dataframe(comparison_df)

# Correlation Plot
st.subheader("📊 Correlation: GDP vs Total Renewable Energy")
st.scatter_chart(df[["GDP_Billion_USD", "Total_GW"]])

# Region-wise aggregation
st.subheader("🌍 Region-Wise Renewable Averages")
region_df = df[df["Year"] == year].groupby("Region")[energy_sources + ["Total_GW"]].mean()
st.bar_chart(region_df["Total_GW"])

# Download
st.download_button("📥 Download This Year’s Data", df[df["Year"] == year].to_csv(index=False), "yearly_renewables.csv", "text/csv")

# Closing
st.info("💡 Try interacting with the sidebar to explore more insights by year and country!")
