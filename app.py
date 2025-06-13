import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv("renewables_enhanced.csv")

st.set_page_config(page_title="Renewable Energy Chatbot", layout="centered")

st.title("🌱 Renewable Awareness Chatbot + Insights")

# Sidebar for country selection
country = st.sidebar.selectbox("Select a country", df["Country"].unique())

# Filter data for the selected country
data = df[df["Country"] == country].iloc[0]

st.header(f"🔍 Insights for {country} ({data['Year']})")

# Display data summary
st.markdown(f"""
- 🌞 **Solar**: {data['Solar_GW']} GW  
- 🌬️ **Wind**: {data['Wind_GW']} GW  
- 💧 **Hydro**: {data['Hydro_GW']} GW  
- 🌾 **Biomass**: {data['Biomass_GW']} GW  
- 🌋 **Geothermal**: {data['Geothermal_GW']} GW  
- 👥 **Population**: {data['Population_M']} million  
- 💰 **GDP**: ${data['GDP_Billion_USD']} billion
""")

# Pie chart of energy sources
labels = ['Solar', 'Wind', 'Hydro', 'Biomass', 'Geothermal']
sizes = [data['Solar_GW'], data['Wind_GW'], data['Hydro_GW'], data['Biomass_GW'], data['Geothermal_GW']]
colors = ['#FFD700', '#1E90FF', '#00CED1', '#8FBC8F', '#FF6347']

fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
ax1.axis('equal')
st.pyplot(fig1)

# Chatbot-style Q&A (simulated)
query = st.text_input("Ask something about renewable energy in this country:")

if query:
    if "solar" in query.lower():
        st.info(f"In {country}, solar energy contributes {data['Solar_GW']} GW to the total renewable capacity.")
    elif "wind" in query.lower():
        st.info(f"{country} has {data['Wind_GW']} GW of wind power.")
    elif "compare" in query.lower():
        st.info(f"{country}'s total renewable energy is {sum(sizes)} GW with GDP ${data['GDP_Billion_USD']} billion.")
    else:
        st.success("Thanks for your question! The bot is still learning more detailed responses.")
