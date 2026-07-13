# ==========================================
# Renewable Energy Awareness Chatbot
# Modern Streamlit UI (Starter Version)
# ==========================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from gtts import gTTS
from io import BytesIO
import base64

st.set_page_config(page_title="Renewable Energy Awareness Chatbot",
                   page_icon="🌿",
                   layout="wide")

st.markdown("""
<div style="padding:25px;border-radius:18px;
background:linear-gradient(135deg,#2E7D32,#43A047,#81C784);
color:white;text-align:center;">
<h1>🌿 Renewable Energy Awareness Chatbot</h1>
<h4>Learn • Explore • Compare • Act</h4>
<p>AI-powered platform for renewable energy awareness and climate education.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="background:#F8FFF9;padding:15px;border-radius:15px;
text-align:center;font-size:26px;">
☀️ Solar &nbsp;&nbsp; 💨 Wind &nbsp;&nbsp; 💧 Hydro &nbsp;&nbsp;
🌿 Biomass &nbsp;&nbsp; 🌋 Geothermal
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("🌿 Renewable Energy Awareness Chatbot")
    st.markdown("---")
    st.markdown("""
🏠 Dashboard

💬 AI Chatbot

📚 Learn

🌍 Compare Countries

📈 Trends

🌱 Climate Impact
""")
    st.markdown("---")
    st.success("SDG 7 • Affordable & Clean Energy")

@st.cache_data
def load_data():
    df = pd.read_csv("renewables_enhanced_augmented.csv")
    cols=["Solar_GW","Wind_GW","Hydro_GW","Biomass_GW","Geothermal_GW"]
    df[cols]=df[cols].apply(pd.to_numeric)
    df["Total_GW"]=df[cols].sum(axis=1)
    return df

df=load_data()

country_flags={
"India":"🇮🇳 India","USA":"🇺🇸 USA","China":"🇨🇳 China",
"Germany":"🇩🇪 Germany","Brazil":"🇧🇷 Brazil",
"Australia":"🇦🇺 Australia","UK":"🇬🇧 UK",
"France":"🇫🇷 France","Canada":"🇨🇦 Canada",
"South Africa":"🇿🇦 South Africa"
}

tab1,tab2,tab3=st.tabs(["📊 Dashboard","💬 Chatbot","📚 Learn"])

with tab1:

    c1,c2=st.columns([2,1])

    with c1:
        country=st.selectbox("🌍 Select Country",
                             list(country_flags.keys()),
                             format_func=lambda x:country_flags[x])

    with c2:
        year=st.selectbox("📅 Year",
                          sorted(df.Year.unique(),reverse=True))

    data=df[(df.Country==country)&(df.Year==year)].iloc[0]

    k1,k2,k3,k4=st.columns(4)

    k1.metric("⚡ Total Capacity",f"{data['Total_GW']:.1f} GW")
    k2.metric("🌍 Population",f"{data['Population_M']:.0f} M")
    k3.metric("💰 GDP",f"${data['GDP_Billion_USD']:.0f} B")
    k4.metric("🌱 Green Score",
              f"{min(100,round(data['Total_GW']/5))}/100")

    energy=["Solar_GW","Wind_GW","Hydro_GW",
            "Biomass_GW","Geothermal_GW"]

    labels=["Solar","Wind","Hydro","Biomass","Geothermal"]

    colors=["#F9A826","#29B6F6","#1976D2",
            "#66BB6A","#8D6E63"]

    left,right=st.columns([1,1])

    with left:

        fig=go.Figure(go.Pie(
            labels=labels,
            values=data[energy],
            hole=.55,
            marker=dict(colors=colors)
        ))

        fig.update_layout(
            title="Renewable Energy Mix",
            height=500)

        st.plotly_chart(fig,use_container_width=True)

    with right:

        for emoji,col,color in zip(
            ["☀️","💨","💧","🌿","🌋"],
            energy,
            colors):

            st.markdown(f"""
<div style="padding:12px;border-left:8px solid {color};
background:white;border-radius:10px;
margin-bottom:10px;">
<h4>{emoji} {col.replace("_GW","")}</h4>
<h2>{data[col]:.1f} GW</h2>
</div>
""",unsafe_allow_html=True)

    trend=df[df.Country==country].sort_values("Year")

    fig2=px.area(
        trend,
        x="Year",
        y=["Solar_GW","Wind_GW","Hydro_GW"],
        title=f"{country} Renewable Growth")

    st.plotly_chart(fig2,use_container_width=True)

    growth=((trend.iloc[-1]["Solar_GW"]-
              trend.iloc[0]["Solar_GW"])
              /trend.iloc[0]["Solar_GW"])*100

    st.info(f"""
🤖 AI Insight

• Solar capacity increased by **{growth:.1f}%**

• Wind energy continues steady growth.

• Hydropower remains stable.

Recommendation:
Increase investment in renewable infrastructure.
""")

    st.subheader("🌱 Climate Impact")

    a,b,c,d=st.columns(4)

    co2=data["Total_GW"]*1200
    trees=int(co2/21)
    homes=int(data["Total_GW"]*500000)
    cars=int(co2/4600)

    a.metric("🌍 CO₂ Saved",f"{co2:,.0f} Tons")
    b.metric("🌳 Trees",f"{trees:,}")
    c.metric("🏠 Homes Powered",f"{homes:,}")
    d.metric("🚗 Cars Removed",f"{cars:,}")

    mapfig=px.choropleth(
        df[df.Year==year],
        locations="Country",
        locationmode="country names",
        color="Total_GW",
        hover_name="Country",
        color_continuous_scale="Greens")

    st.plotly_chart(mapfig,use_container_width=True)

with tab2:

    st.subheader("💬 AI Renewable Assistant")

    if "messages" not in st.session_state:
        st.session_state.messages=[]

    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.write(m["content"])

    q=st.chat_input("Ask about renewable energy...")

    if q:
        with st.chat_message("user"):
            st.write(q)

        response="Try asking about solar, wind, hydro, biomass, geothermal or total renewable capacity."

        if "solar" in q.lower():
            response=f"{country} has {data['Solar_GW']} GW of solar capacity."
        elif "wind" in q.lower():
            response=f"{country} has {data['Wind_GW']} GW of wind capacity."
        elif "hydro" in q.lower():
            response=f"{country} has {data['Hydro_GW']} GW of hydropower."
        elif "total" in q.lower():
            response=f"Total renewable capacity is {data['Total_GW']:.1f} GW."

        st.session_state.messages.append({"role":"user","content":q})
        st.session_state.messages.append({"role":"assistant","content":response})

        with st.chat_message("assistant"):
            st.write(response)

            tts=gTTS(response)
            mp3=BytesIO()
            tts.write_to_fp(mp3)
            mp3.seek(0)
            b64=base64.b64encode(mp3.read()).decode()
            st.audio(f"data:audio/mp3;base64,{b64}")

with tab3:

    st.subheader("📚 Renewable Energy Explorer")

    topic=st.radio(
        "Choose a topic",
        ["☀️ Solar","💨 Wind","💧 Hydro","🌿 Biomass","🌋 Geothermal"],
        horizontal=True)

    with st.expander("Learn More",expanded=True):

        if "Solar" in topic:
            st.write("☀️ Converts sunlight into electricity.")
            st.success("Advantages: Clean, abundant, low maintenance.")
            st.warning("Disadvantages: Weather dependent.")
        elif "Wind" in topic:
            st.write("💨 Generates electricity using wind turbines.")
        elif "Hydro" in topic:
            st.write("💧 Uses flowing water to generate electricity.")
        elif "Biomass" in topic:
            st.write("🌿 Uses organic matter as fuel.")
        else:
            st.write("🌋 Uses Earth's internal heat.")

st.markdown("---")
st.markdown(
"<center><b>❤️ Built for the 1M1B Green Internship | SDG 7 • Affordable & Clean Energy</b></center>",
unsafe_allow_html=True)
