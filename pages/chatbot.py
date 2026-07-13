import random
import streamlit as st


def show_chatbot(df, row, country, year):
    """Render the Renewable Energy AI Chatbot page."""

    st.markdown(f"""
    <div style="
    background:linear-gradient(135deg,#2E7D32,#43A047,#66BB6A);
    padding:30px;
    border-radius:20px;
    color:white;">
        <h1>🤖 Renewable Energy Assistant</h1>
        <h4>Your AI Guide for Clean & Sustainable Energy</h4>
        <p><b>Currently Viewing:</b> {country} ({year})</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    m1, m2, m3 = st.columns(3)
    m1.metric("⚡ Total Capacity", f"{row['Total_GW']:.1f} GW")
    m2.metric("☀️ Solar", f"{row['Solar_GW']:.1f} GW")
    m3.metric("💨 Wind", f"{row['Wind_GW']:.1f} GW")

    st.markdown("## ⚡ Quick Questions")

    q1, q2, q3, q4 = st.columns(4)

    if q1.button("☀️ Solar"):
        st.session_state.quick_question = "What is the solar capacity?"

    if q2.button("💨 Wind"):
        st.session_state.quick_question = "What is the wind capacity?"

    if q3.button("💧 Hydro"):
        st.session_state.quick_question = "What is the hydro capacity?"

    if q4.button("⚡ Total"):
        st.session_state.quick_question = "What is the total renewable capacity?"

    st.markdown("## 🌿 What can I help you with?")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.info("""### ☀️ Renewable Sources

• Solar
• Wind
• Hydro
• Biomass
• Geothermal""")

    with c2:
        st.success("""### 📊 Country Insights

• Capacity
• GDP
• Population
• Growth
• Top Source""")

    with c3:
        st.warning("""### 💡 Sustainability

• Energy Saving Tips
• Climate Facts
• SDG 7
• Green Living""")

    st.markdown("### 💬 Suggested Questions")
    st.markdown("""
- What is the solar capacity?
- What is the total renewable capacity?
- Which renewable source is highest?
- Tell me about wind energy.
- What is India's GDP?
- Give me energy saving tips.
""")

    st.markdown("---")
    st.subheader("💬 Conversation")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "quick_question" in st.session_state:
        question = st.session_state.pop("quick_question")
        st.session_state.messages.append({"role": "user", "content": question})

    for msg in st.session_state.messages:
        avatar = "👤" if msg["role"] == "user" else "🤖"
        with st.chat_message(msg["role"], avatar=avatar):
            st.write(msg["content"])

    q = st.chat_input("Ask about renewable energy...")

    if q:
        st.session_state.messages.append({"role": "user", "content": q})

    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":

        query = st.session_state.messages[-1]["content"].lower()

        if any(x in query for x in ["solar", "sun", "photovoltaic"]):
            ans = f"☀️ **{country}** has **{row['Solar_GW']:.1f} GW** of installed solar capacity in **{year}**."

        elif any(x in query for x in ["wind", "turbine"]):
            ans = f"💨 **{country}** has **{row['Wind_GW']:.1f} GW** of installed wind capacity."

        elif any(x in query for x in ["hydro", "water", "dam"]):
            ans = f"💧 **{country}** has **{row['Hydro_GW']:.1f} GW** of hydropower."

        elif any(x in query for x in ["biomass", "organic"]):
            ans = f"🌿 **{country}** has **{row['Biomass_GW']:.1f} GW** of biomass capacity."

        elif any(x in query for x in ["geothermal", "earth", "heat"]):
            ans = f"🌋 **{country}** has **{row['Geothermal_GW']:.1f} GW** of geothermal capacity."

        elif "population" in query:
            ans = f"🌍 Population: **{row['Population_M']:.0f} Million**."

        elif "gdp" in query:
            ans = f"💰 GDP: **${row['GDP_Billion_USD']:.0f} Billion USD**."

        elif "highest" in query or "top" in query:
            energy = {
                "Solar": row["Solar_GW"],
                "Wind": row["Wind_GW"],
                "Hydro": row["Hydro_GW"],
                "Biomass": row["Biomass_GW"],
                "Geothermal": row["Geothermal_GW"],
            }
            top = max(energy, key=energy.get)
            ans = f"🏆 The highest renewable source is **{top} ({energy[top]:.1f} GW)**."

        elif "total" in query or "renewable" in query:
            ans = f"⚡ Total renewable capacity is **{row['Total_GW']:.1f} GW**."

        elif "tip" in query:
            tips = [
                "Turn off lights when not needed.",
                "Use LED bulbs.",
                "Install rooftop solar.",
                "Use energy-efficient appliances.",
                "Unplug idle chargers.",
            ]
            ans = "🌱 **Eco Tip:** " + random.choice(tips)

        else:
            ans = """🤖 I can answer questions about:

• Solar
• Wind
• Hydro
• Biomass
• Geothermal
• Population
• GDP
• Total Capacity
• Highest Renewable Source
• Energy Saving Tips"""

        with st.chat_message("assistant", avatar="🤖"):
            st.write(ans)

        st.session_state.messages.append(
            {"role": "assistant", "content": ans}
        )

    st.markdown("---")

    eco_tips = [
        "Switch to LED bulbs.",
        "Turn off unused appliances.",
        "Use natural daylight whenever possible.",
        "Support renewable energy projects.",
        "Reduce electricity waste.",
    ]

    st.success(f"🌱 **Eco Tip of the Day:** {random.choice(eco_tips)}")
