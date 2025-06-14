import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from gtts import gTTS
from io import BytesIO
import base64

st.set_page_config(page_title="Renewable Awareness Chatbot", layout="wide")
st.title("🌿 Renewable Awareness Chatbot + Dashboard")

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

tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "💬 Chatbot", "📚 Learn"])

# === TAB 1: Dashboard ===
with tab1:
    country = st.selectbox("Select Country", sorted(df["Country"].unique()))
    year = st.selectbox("Select Year", sorted(df["Year"].unique(), reverse=True))
    data = df[(df["Country"] == country) & (df["Year"] == year)].iloc[0]

    st.subheader(f"🔍 Overview for {country} ({year})")
    energy_sources = ["Solar_GW", "Wind_GW", "Hydro_GW", "Biomass_GW", "Geothermal_GW"]
    labels = [s.replace("_GW", "") for s in energy_sources]
    sizes = data[energy_sources].values.flatten()

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140)
    ax.axis("equal")
    st.pyplot(fig)

    st.metric("Population (Millions)", data["Population_M"])
    st.metric("GDP (Billion USD)", data["GDP_Billion_USD"])
    st.metric("Total Renewable Capacity (GW)", round(data["Total_GW"], 2))

    st.subheader("📈 Renewable Trends")
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

    st.subheader("🔄 Country Comparison")
    col1, col2 = st.columns(2)
    with col1:
        country1 = st.selectbox("Country 1", df["Country"].unique(), index=0, key="c1")
    with col2:
        country2 = st.selectbox("Country 2", df["Country"].unique(), index=1, key="c2")

    d1 = df[(df["Country"] == country1) & (df["Year"] == year)].iloc[0]
    d2 = df[(df["Country"] == country2) & (df["Year"] == year)].iloc[0]

    comparison_df = pd.DataFrame({
        "Source": labels,
        country1: d1[energy_sources].values,
        country2: d2[energy_sources].values
    })
    st.dataframe(comparison_df)

    df["Green_Investment_BillionUSD"] = df["Total_GW"] * 0.1
    st.subheader("💰 GDP vs Green Investment")
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=df, x="GDP_Billion_USD", y="Green_Investment_BillionUSD", hue="Country", ax=ax2)
    ax2.set_xlabel("GDP (Billion USD)")
    ax2.set_ylabel("Green Investment (Billion USD)")
    ax2.set_title("Green Investment vs GDP")
    st.pyplot(fig2)

    st.subheader("🌍 Region-Wise Renewable Averages")
    region_df = df[df["Year"] == year].groupby("Region")[energy_sources + ["Total_GW"]].mean()
    st.bar_chart(region_df["Total_GW"])

    st.download_button("📥 Download This Year’s Data", df[df["Year"] == year].to_csv(index=False), "yearly_renewables.csv", "text/csv")

# === TAB 2: Chatbot ===
with tab2:
    st.subheader("💬 Ask the Chatbot")
    faq = st.radio("Quick Questions", [
        f"What is the top renewable source in {country}?",
        f"Compare Wind and Solar in {country}",
        f"Show renewable mix for {country} in {year}"
    ])

    def faq_response(q):
        if "top renewable" in q:
            max_source = data[energy_sources].idxmax()
            return f"🌟 {country}'s top renewable source is {max_source.replace('_GW','')} with {data[max_source]} GW."
        elif "Compare" in q:
            return f"{country} → Solar: {data['Solar_GW']} GW | Wind: {data['Wind_GW']} GW"
        else:
            mix = ", ".join([f"{k.replace('_GW','')}: {v} GW" for k, v in data.items() if k.endswith('_GW')])
            return f"{country} ({year}) → {mix}"

    st.info(faq_response(faq))

    user_query = st.text_input("Ask anything about renewable energy:")

    def answer_query(query):
        query = query.lower()
        if country.lower() in query:
            if "solar" in query:
                return f"{country} has {data['Solar_GW']} GW of solar."
            elif "wind" in query:
                return f"{country} has {data['Wind_GW']} GW of wind."
            elif "hydro" in query:
                return f"{country} has {data['Hydro_GW']} GW of hydropower."
            elif "biomass" in query:
                return f"{country} has {data['Biomass_GW']} GW of biomass."
            elif "geothermal" in query:
                return f"{country} has {data['Geothermal_GW']} GW of geothermal."
            elif "total" in query:
                return f"{country}'s total is {data['Total_GW']} GW."
        return "🤖 I'm still learning! Try asking about solar, wind, hydro, etc."

    if user_query:
        response = answer_query(user_query)
        st.success(response)

        tts = gTTS(response)
        mp3 = BytesIO()
        tts.write_to_fp(mp3)
        mp3.seek(0)
        b64 = base64.b64encode(mp3.read()).decode()
        st.audio(f"data:audio/mp3;base64,{b64}", format="audio/mp3")

# === TAB 3: Learn ===
with tab3:
    st.subheader("📚 Learn About Renewable Energy")
    energy_topic = st.text_input("Type a renewable energy type to learn more:")

    if energy_topic:
        et = energy_topic.lower()
        if "solar" in et:
            st.info("☀️ Solar Energy: Converts sunlight into electricity via photovoltaic cells.")
        elif "wind" in et:
            st.info("💨 Wind Energy: Uses turbines to generate electricity from wind.")
        elif "hydro" in et:
            st.info("💧 Hydropower: Uses water flow to spin turbines and generate power.")
        elif "biomass" in et:
            st.info("🌾 Biomass: Organic matter like wood or crop waste used for fuel.")
        elif "geothermal" in et:
            st.info("🌋 Geothermal: Heat from below Earth’s surface is used to generate electricity.")
        else:
            st.warning("Try Solar, Wind, Hydro, Biomass, or Geothermal.")

st.markdown("---")
st.info("This app is created for the 1M1B Green Internship Project.")
