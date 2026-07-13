import streamlit as st

def show_climate(row, country, year):
    """
    Display the Climate Impact Calculator page.
    """

    st.title("🌱 Climate Impact Calculator")

    st.markdown("""
Estimate the positive environmental impact of renewable energy generation
based on the selected **country** and **year**.
""")

    # =====================================
    # Climate Impact Calculations
    # =====================================

    co2 = row["Total_GW"] * 1200          # Approx. tonnes of CO₂ avoided annually
    trees = int(co2 / 21)                 # Approx. trees equivalent
    homes = int(row["Total_GW"] * 500000) # Approx. homes powered
    cars = int(co2 / 4600)                # Approx. cars removed

    # =====================================
    # KPI Cards
    # =====================================

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "🌍 CO₂ Saved",
            f"{co2:,.0f} Tons"
        )

    with c2:
        st.metric(
            "🌳 Equivalent Trees",
            f"{trees:,}"
        )

    with c3:
        st.metric(
            "🏠 Homes Powered",
            f"{homes:,}"
        )

    with c4:
        st.metric(
            "🚗 Cars Removed",
            f"{cars:,}"
        )

    st.markdown("---")

    # =====================================
    # Progress Indicators
    # =====================================

    st.subheader("📈 Environmental Impact Indicators")

    st.write("🌍 CO₂ Reduction")
    st.progress(min(co2 / 500000, 1.0))

    st.write("🌳 Forest Impact")
    st.progress(min(trees / 50000, 1.0))

    st.write("🏠 Clean Energy Coverage")
    st.progress(min(homes / 1000000, 1.0))

    st.markdown("---")

    # =====================================
    # Summary
    # =====================================

    st.info(f"""
### 🌿 Environmental Impact Summary

For **{country} ({year})**, the estimated renewable energy capacity of
**{row['Total_GW']:.1f} GW** could:

- 🌍 Avoid approximately **{co2:,.0f} tonnes of CO₂ emissions** annually.
- 🌳 Have an environmental impact equivalent to planting **{trees:,} trees**.
- 🏠 Supply clean electricity to approximately **{homes:,} homes**.
- 🚗 Offset the annual emissions of about **{cars:,} passenger vehicles**.

These values are educational estimates based on commonly used renewable
energy conversion factors.
""")

    st.success(
        "🌱 Increasing renewable energy adoption helps reduce greenhouse gas "
        "emissions and supports a cleaner, more sustainable future."
    )
