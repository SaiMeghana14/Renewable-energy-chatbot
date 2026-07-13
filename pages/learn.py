import streamlit as st


def show_learn():
    """
    Display educational information about renewable energy sources.
    """

    st.title("📚 Renewable Energy Learning Center")

    st.markdown("""
Explore different renewable energy sources, understand their benefits,
limitations, and discover which countries are leading the clean energy transition.
""")

    topic = st.radio(
        "Choose an Energy Source",
        [
            "☀️ Solar",
            "💨 Wind",
            "💧 Hydro",
            "🌿 Biomass",
            "🌋 Geothermal"
        ],
        horizontal=True
    )

    # ----------------------------------------------------
    # SOLAR
    # ----------------------------------------------------

    if "Solar" in topic:

        left, right = st.columns([1, 1.4])

        with left:
            st.image("assets/solar.png", use_container_width=True)

        with right:

            st.success(
                "Solar energy converts sunlight into electricity using photovoltaic cells."
            )

            st.metric("⚡ Efficiency", "20–25%")
            st.metric("🌍 CO₂ Emissions", "Very Low")

        c1, c2 = st.columns(2)

        with c1:

            st.markdown("""
### ✅ Advantages

- Renewable
- Clean energy
- Low maintenance
- Reduces electricity bills
- Zero fuel cost
""")

        with c2:

            st.markdown("""
### ⚠️ Disadvantages

- Weather dependent
- Initial installation cost
- Requires space
- No generation at night
""")

        st.markdown("""
### 🌍 Leading Countries

🇨🇳 China

🇺🇸 USA

🇮🇳 India

🇩🇪 Germany
""")

        st.info(
            "💡 **Interesting Fact:** The Sun provides enough energy to power the Earth thousands of times over."
        )

    # ----------------------------------------------------
    # WIND
    # ----------------------------------------------------

    elif "Wind" in topic:

        left, right = st.columns([1, 1.4])

        with left:
            st.image("assets/wind.png", use_container_width=True)

        with right:

            st.success(
                "Wind turbines convert moving air into electricity."
            )

            st.metric("⚡ Efficiency", "35–45%")
            st.metric("🌍 CO₂ Emissions", "Very Low")

        c1, c2 = st.columns(2)

        with c1:

            st.markdown("""
### ✅ Advantages

- Renewable

- Low operating cost

- No fuel required

- Clean electricity
""")

        with c2:

            st.markdown("""
### ⚠️ Disadvantages

- Noise

- Wildlife impact

- Depends on wind speed
""")

        st.markdown("""
### 🌍 Leading Countries

🇨🇳 China

🇺🇸 USA

🇩🇪 Germany

🇮🇳 India
""")

        st.info(
            "💡 **Interesting Fact:** One large wind turbine can power thousands of homes each year."
        )

    # ----------------------------------------------------
    # HYDRO
    # ----------------------------------------------------

    elif "Hydro" in topic:

        left, right = st.columns([1, 1.4])

        with left:
            st.image("assets/hydro.png", use_container_width=True)

        with right:

            st.success(
                "Hydropower converts flowing water into electricity."
            )

            st.metric("⚡ Efficiency", "90%")
            st.metric("🌍 CO₂ Emissions", "Low")

        c1, c2 = st.columns(2)

        with c1:

            st.markdown("""
### ✅ Advantages

- Reliable

- Clean

- High efficiency

- Long lifespan
""")

        with c2:

            st.markdown("""
### ⚠️ Disadvantages

- Expensive dams

- Environmental impact

- Ecosystem disruption
""")

        st.markdown("""
### 🌍 Leading Countries

🇨🇳 China

🇧🇷 Brazil

🇨🇦 Canada

🇮🇳 India
""")

        st.info(
            "💡 **Interesting Fact:** Hydropower is currently the world's largest renewable electricity source."
        )

    # ----------------------------------------------------
    # BIOMASS
    # ----------------------------------------------------

    elif "Biomass" in topic:

        left, right = st.columns([1, 1.4])

        with left:
            st.image("assets/biomass.png", use_container_width=True)

        with right:

            st.success(
                "Biomass energy uses organic materials like crop waste and wood."
            )

            st.metric("⚡ Efficiency", "25–35%")
            st.metric("🌍 CO₂ Emissions", "Moderate")

        c1, c2 = st.columns(2)

        with c1:

            st.markdown("""
### ✅ Advantages

- Uses agricultural waste

- Renewable

- Produces electricity and heat

- Supports rural economies
""")

        with c2:

            st.markdown("""
### ⚠️ Disadvantages

- Air pollution

- Large land requirement

- Transportation costs
""")

        st.markdown("""
### 🌍 Leading Countries

🇺🇸 USA

🇧🇷 Brazil

🇮🇳 India
""")

        st.info(
            "💡 **Interesting Fact:** Biomass helps convert waste into useful energy instead of sending it to landfills."
        )

    # ----------------------------------------------------
    # GEOTHERMAL
    # ----------------------------------------------------

    elif "Geothermal" in topic:

        left, right = st.columns([1, 1.4])

        with left:
            st.image("assets/geothermal.png", use_container_width=True)

        with right:

            st.success(
                "Geothermal energy comes from the Earth's internal heat."
            )

            st.metric("⚡ Efficiency", "10–20%")
            st.metric("🌍 CO₂ Emissions", "Very Low")

        c1, c2 = st.columns(2)

        with c1:

            st.markdown("""
### ✅ Advantages

- Reliable

- Available 24/7

- Very low emissions

- Small land footprint
""")

        with c2:

            st.markdown("""
### ⚠️ Disadvantages

- Expensive drilling

- Location dependent

- High initial investment
""")

        st.markdown("""
### 🌍 Leading Countries

🇮🇸 Iceland

🇺🇸 USA

🇮🇩 Indonesia

🇵🇭 Philippines
""")

        st.info(
            "💡 **Interesting Fact:** Iceland generates most of its heating from geothermal energy."
        )

    st.markdown("---")

    st.success(
        "🌱 Learning about renewable energy is the first step toward building a more sustainable future."
    )
