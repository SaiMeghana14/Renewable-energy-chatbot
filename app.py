import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from utils import load_data

from pages.dashboard import show_dashboard
from pages.chatbot import show_chatbot
from pages.learn import show_learn
from pages.compare import show_compare
from pages.climate import show_climate
from pages.quiz import show_quiz
from pages.report import show_report
from pages.tableau import show_tableau

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Renewable Energy Awareness Chatbot",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

.main{
    background:#F8FFF9;
}

.block-container{
    padding-top:1rem;
    padding-bottom:1rem;
}

.metric-card{
    background:white;
    padding:18px;
    border-radius:18px;
    border:1px solid #D9EAD3;
    box-shadow:0 4px 12px rgba(0,0,0,.08);
}

.energy-card{
    padding:18px;
    border-radius:16px;
    color:white;
    text-align:center;
    font-weight:bold;
}

.footer{
    text-align:center;
    color:#555;
    padding:25px;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# LOAD DATA
# ==========================================

df = load_data()

# ==========================================
# COUNTRY FLAGS
# ==========================================

flags = {
    "India": "🇮🇳 India",
    "USA": "🇺🇸 USA",
    "China": "🇨🇳 China",
    "Germany": "🇩🇪 Germany",
    "Brazil": "🇧🇷 Brazil",
    "Australia": "🇦🇺 Australia",
    "UK": "🇬🇧 UK",
    "France": "🇫🇷 France",
    "Canada": "🇨🇦 Canada",
    "South Africa": "🇿🇦 South Africa"
}

# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.image(
        "assets/renewable.png",
        width=100
    )

    st.title("🌿 Renewable Energy Awareness Chatbot")

    st.caption("Version 1.0")

    st.markdown("---")

    page = st.radio(

        "Navigation",

        [

            "🏠 Dashboard",

            "💬 AI Chatbot",

            "📚 Learn",

            "🌍 Compare",

            "📊 Tableau Analytics",

            "🌱 Climate Impact",

            "🎮 Green Quiz",

            "📄 Report"

        ]

    )

    st.markdown("---")

    country = st.selectbox(

        "🌍 Select Country",

        list(flags.keys()),

        format_func=lambda x: flags[x]

    )

    year = st.select_slider(

        "📅 Select Year",

        options=sorted(df["Year"].unique()),

        value=max(df["Year"].unique())

    )

    st.markdown("---")

    st.success("SDG 7 • Affordable & Clean Energy")

# ==========================================
# HERO BANNER
# ==========================================

st.markdown("""

<div style="
padding:35px;
border-radius:24px;
background:linear-gradient(135deg,#1B5E20,#43A047,#81C784);
color:white;
text-align:center;
">

<h1>🌿 Renewable Energy Awareness Chatbot</h1>

<h3>
AI-Powered Renewable Energy Dashboard
</h3>

<p>

Learn • Explore • Compare • Act

</p>

</div>

""", unsafe_allow_html=True)

# ==========================================
# RENEWABLE ENERGY BANNER
# ==========================================

st.markdown("""

<div style="
background:#F8FFF9;
padding:15px;
border-radius:18px;
text-align:center;
font-size:28px;
">

☀️ Solar

&nbsp;&nbsp;&nbsp;

💨 Wind

&nbsp;&nbsp;&nbsp;

💧 Hydro

&nbsp;&nbsp;&nbsp;

🌿 Biomass

&nbsp;&nbsp;&nbsp;

🌋 Geothermal

</div>

""", unsafe_allow_html=True)

# ==========================================
# FILTER DATA
# ==========================================

filtered = df[

    (df["Country"] == country)

    &

    (df["Year"] == year)

]

if filtered.empty:

    st.error("No data available.")

    st.stop()

row = filtered.iloc[0]

# ==========================================
# CLIMATE IMPACT CALCULATIONS
# ==========================================

co2 = row["Total_GW"] * 1200

trees = int(co2 / 21)

homes = int(row["Total_GW"] * 500000)

cars = int(co2 / 4600)

# ==========================================
# AI RECOMMENDATION
# ==========================================

if row["Solar_GW"] > row["Wind_GW"]:

    recommendation = (

        "Expand solar farms and rooftop solar installations."

    )

elif row["Wind_GW"] > row["Solar_GW"]:

    recommendation = (

        "Increase investments in wind farms and modern turbine technology."

    )

else:

    recommendation = (

        "Maintain a balanced renewable energy portfolio."

    )

C

# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.markdown(
    """
<div class="footer">

<h3>❤️ Built for the 1M1B Green Internship</h3>

<p>
Promoting
<b>SDG 7 • Affordable & Clean Energy</b>
</p>

</div>
""",
    unsafe_allow_html=True,
)
