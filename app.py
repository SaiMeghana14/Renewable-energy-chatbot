# app.py - Renewable Energy Awareness Chatbot using Streamlit

import streamlit as st

# Set page configuration
st.set_page_config(page_title="Renewable Energy Awareness Chatbot", page_icon="🌱")

# Title and instructions
st.title("🌿 Renewable Energy Awareness Chatbot")
st.write("💬 Ask me anything about renewable energy sources like **solar, wind, hydro, geothermal, and biomass.**")

# Chatbot response logic
def chatbot_response(user_input):
    user_input = user_input.lower()

    if "solar" in user_input:
        return "🌞 Solar energy is harnessed from sunlight using solar panels. It’s clean, abundant, and widely used for home and grid power."
    elif "wind" in user_input:
        return "🌬️ Wind energy uses wind turbines to generate electricity. It's efficient and commonly used in wind farms."
    elif "hydro" in user_input or "hydropower" in user_input:
        return "💧 Hydropower generates electricity from flowing water using dams or rivers. It’s reliable but may impact ecosystems."
    elif "geothermal" in user_input:
        return "🌋 Geothermal energy comes from the Earth’s internal heat. It’s used for electricity and heating in volcanic regions."
    elif "biomass" in user_input:
        return "🌾 Biomass energy is produced from organic materials like plants, wood, or waste. It’s renewable and supports waste management."
    elif "benefits" in user_input or "advantages" in user_input:
        return "✅ Renewable energy reduces carbon emissions, lowers pollution, promotes sustainability, and creates green jobs."
    elif "carbon" in user_input or "footprint" in user_input:
        return "🌍 You can reduce your carbon footprint by using public transport, saving energy, recycling, and supporting clean energy."
    elif "help me choose" in user_input:
        return "🧭 Please share your location, sunlight availability, and budget — I’ll suggest the best renewable option for you!"
    elif "hello" in user_input or "hi" in user_input:
        return "👋 Hello! I'm your Renewable Energy Awareness Bot. Ask me anything about solar, wind, hydro, geothermal, or biomass energy!"
    else:
        return "❓ I’m not sure about that. Try asking about solar, wind, hydro, geothermal, or biomass energy."

# Input and response
user_input = st.text_input("Type your question below:")

if user_input:
    response = chatbot_response(user_input)
    st.markdown(f"**Bot:** {response}")

# Footer
st.markdown("---")
st.caption("🌱 Created for 1M1B Green Internship | Deploy via Streamlit Cloud")
