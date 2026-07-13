import streamlit as st
import plotly.express as px


def show_compare(df, year):
    """
    Compare renewable energy capacity between two countries.
    """

    st.title("🌍 Compare Renewable Energy")

    st.markdown("""
Compare renewable energy generation across countries for the selected year.
Analyze solar, wind, hydro, biomass, geothermal, and total renewable capacity.
""")

    col1, col2 = st.columns(2)

    countries = sorted(df["Country"].unique())

    with col1:
        country1 = st.selectbox(
            "🌍 Country 1",
            countries,
            key="compare_country1"
        )

    with col2:
        default_index = 1 if len(countries) > 1 else 0

        country2 = st.selectbox(
            "🌍 Country 2",
            countries,
            index=default_index,
            key="compare_country2"
        )

    if country1 == country2:
        st.warning("Please select two different countries.")
        return

    d1 = df[
        (df["Country"] == country1) &
        (df["Year"] == year)
    ]

    d2 = df[
        (df["Country"] == country2) &
        (df["Year"] == year)
    ]

    if d1.empty or d2.empty:
        st.error("Comparison data is unavailable.")
        return

    d1 = d1.iloc[0]
    d2 = d2.iloc[0]

    energy_sources = [
        "Solar",
        "Wind",
        "Hydro",
        "Biomass",
        "Geothermal"
    ]

    fig = px.bar(
        x=energy_sources,
        y=[
            d1["Solar_GW"],
            d1["Wind_GW"],
            d1["Hydro_GW"],
            d1["Biomass_GW"],
            d1["Geothermal_GW"],
        ],
        labels={
            "x": "Renewable Energy Source",
            "y": "Capacity (GW)"
        },
        color_discrete_sequence=["#43A047"],
        title=f"{country1} vs {country2} ({year})"
    )

    fig.add_bar(
        x=energy_sources,
        y=[
            d2["Solar_GW"],
            d2["Wind_GW"],
            d2["Hydro_GW"],
            d2["Biomass_GW"],
            d2["Geothermal_GW"],
        ],
        name=country2,
        marker_color="#1976D2"
    )

    fig.update_layout(
        template="plotly_white",
        barmode="group",
        height=550,
        legend_title="Country"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown("---")

    st.subheader("📊 Comparison Summary")

    m1, m2 = st.columns(2)

    with m1:
        st.metric(
            f"{country1} Total Capacity",
            f"{d1['Total_GW']:.1f} GW"
        )

    with m2:
        st.metric(
            f"{country2} Total Capacity",
            f"{d2['Total_GW']:.1f} GW"
        )

    difference = abs(
        d1["Total_GW"] - d2["Total_GW"]
    )

    if d1["Total_GW"] > d2["Total_GW"]:
        winner = country1
    else:
        winner = country2

    st.success(
        f"🏆 **{winner}** leads by **{difference:.1f} GW** in total renewable capacity for **{year}**."
    )

    st.markdown("---")

    st.info(f"""
### 🤖 AI Comparison Insight

**{country1}** has **{d1['Total_GW']:.1f} GW** of renewable capacity,
while **{country2}** has **{d2['Total_GW']:.1f} GW**.

The difference is **{difference:.1f} GW**.

Compare the energy mix above to identify which renewable sources contribute
most to each country's clean energy portfolio.
""")
