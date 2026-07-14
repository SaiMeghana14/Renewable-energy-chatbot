import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

st.set_page_config(
    page_title="Renewable Energy Awareness Chatbot",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

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
padding:20px;
border-radius:20px;
border:1px solid #D9EAD3;
box-shadow:0 6px 20px rgba(0,0,0,.08);
transition:.3s;
}

.metric-card:hover{
transform:translateY(-6px);
box-shadow:0 12px 25px rgba(0,0,0,.15);
}

.energy-card{
padding:18px;
border-radius:18px;
color:white;
text-align:center;
font-weight:bold;
}

.ai-box{
background:#EDF7ED;
padding:20px;
border-left:8px solid #2E7D32;
border-radius:15px;
}

.footer{
text-align:center;
padding:25px;
color:#555;
}

</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.image(
    "assets/renewable.png",
    width=90
    )
    st.title("🌿 Renewable Energy Awareness Chatbot")
    st.markdown("### Navigation")
    page = st.radio("",[
        "🏠 Dashboard",
        "💬 AI Chatbot",
        "📚 Learn",
        "🌍 Compare",
        "📊 Tableau Analytics",
        "🌱 Climate Impact",
        "🎮 Green Quiz",
        "📄 Report"
    ])
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.write(
        "An AI-powered educational platform that promotes renewable energy awareness "
        "through interactive visualizations, a chatbot, climate impact estimates, "
        "and learning resources."
    )

st.markdown("""
<div style="
padding:35px;
border-radius:25px;
background:linear-gradient(135deg,#1B5E20,#43A047,#81C784);
color:white;
text-align:center;
box-shadow:0px 10px 30px rgba(0,0,0,.15);">

<h1>🌿 Renewable Energy Awareness Chatbot</h1>

<h3>AI-Powered Renewable Energy Dashboard</h3>

<p>
Discover • Learn • Compare • Save the Planet
</p>

</div>
""",unsafe_allow_html=True)

st.markdown(
"<div style='text-align:center;font-size:28px;padding:12px'>☀️ Solar &nbsp; 💨 Wind &nbsp; 💧 Hydro &nbsp; 🌿 Biomass &nbsp; 🌋 Geothermal</div>",
unsafe_allow_html=True)

@st.cache_data
def load():
    df = pd.read_csv("data/renewables_enhanced_augmented.csv")
    energy_cols=[
    "Solar_GW",
    "Wind_GW",
    "Hydro_GW",
    "Biomass_GW",
    "Geothermal_GW"
    ]
    numeric_cols=energy_cols+[
    "Population_M",
    "GDP_Billion_USD"
    ]
    df[numeric_cols]=df[numeric_cols].apply(pd.to_numeric)
    df["Total_GW"]=df[energy_cols].sum(axis=1)
    return df

with st.spinner("🌿 Loading Renewable Energy Dashboard..."):
    df = load()

flags={
"India":"🇮🇳 India","USA":"🇺🇸 USA","China":"🇨🇳 China","Germany":"🇩🇪 Germany",
"Brazil":"🇧🇷 Brazil","Australia":"🇦🇺 Australia","UK":"🇬🇧 UK",
"France":"🇫🇷 France","Canada":"🇨🇦 Canada","South Africa":"🇿🇦 South Africa"
}

# =====================================
# Global Country & Year Selection
# =====================================

st.sidebar.markdown("---")

country = st.sidebar.selectbox(
    "🌍 Select Country",
    list(flags.keys()),
    format_func=lambda x: flags[x]
)

year = st.sidebar.select_slider(
    "📅 Select Year",
    options=sorted(df["Year"].unique()),
    value=max(df["Year"].unique())
)

filtered = df[
    (df["Country"] == country) &
    (df["Year"] == year)
]

if filtered.empty:
    st.error("No data available for this selection.")
    st.stop()

row = filtered.iloc[0]

# =====================================
# Climate Impact Calculations
# =====================================

co2 = row["Total_GW"] * 1200          # Estimated CO₂ saved (tons/year)
trees = int(co2 / 21)                 # Equivalent trees
homes = int(row["Total_GW"] * 500000) # Homes powered
cars = int(co2 / 4600)                # Cars removed

# =====================================
# AI Recommendation
# =====================================

if row["Solar_GW"] > row["Wind_GW"]:
    recommendation = (
        "Expand solar farms and rooftop solar installations "
        "to maximize clean energy generation."
    )

elif row["Wind_GW"] > row["Solar_GW"]:
    recommendation = (
        "Increase investments in wind farms and modern turbine technology."
    )

else:
    recommendation = (
        "Maintain a balanced renewable energy portfolio across all sources."
    )

# ==========================================
# 🏠 DASHBOARD
# ==========================================

if page=="🏠 Dashboard":

    col1,col2,col3,col4=st.columns(4)

    col1.metric(
        "⚡ Total Capacity",
        f"{row['Total_GW']:.1f} GW",
        "+5.4%"
    )
    
    col2.metric(
        "🌍 Population",
        f"{row['Population_M']:.0f} M",
        "+1.2%"
    )
    
    col3.metric(
        "💰 GDP",
        f"${row['GDP_Billion_USD']:.0f} B",
        "+3.8%"
    )
    
    col4.metric(
        "🌱 Green Score",
        f"{min(100,round(row['Total_GW']/5))}/100",
        "+4%"
    )
    
    for col,(icon,title,value,color) in zip([col1,col2,col3,col4],cards):
    
        with col:
    
            st.markdown(f"""
    <div class="metric-card"> 
    <h4>{icon} {title}</h4>   
    <h2 style="color:{color};">{value}</h2>
    </div>
    """,unsafe_allow_html=True)
            
    left,right=st.columns([1.1,0.9])
    
    with left:
        fig=go.Figure(go.Pie(
            labels=["Solar","Wind","Hydro","Biomass","Geothermal"],
            values=[row.Solar_GW,row.Wind_GW,row.Hydro_GW,row.Biomass_GW,row.Geothermal_GW],
            hole=.58,
            pull=[0.04,0,0,0,0],
            marker=dict(colors=["#F9A826","#29B6F6","#1976D2","#66BB6A","#8D6E63"])
        ))

        fig.update_traces(
        hovertemplate=       
        "<b>%{label}</b><br>"       
        "Capacity: %{value} GW"     
        "<extra></extra>"
        )
        
        fig.update_layout(
        title="Renewable Energy Mix",        
        template="plotly_white", 
        height=500,      
        legend_orientation="h",      
        font=dict(size=16),       
        paper_bgcolor="#F8FFF9",     
        plot_bgcolor="#F8FFF9" 
        )
        st.plotly_chart(fig,use_container_width=True)

    with right:
        growths=[8,5,3,2,1]

        for (icon,label,val,color),g in zip(
        [
        ("☀️","Solar",row.Solar_GW,"#F9A826"),
        ("💨","Wind",row.Wind_GW,"#29B6F6"),
        ("💧","Hydro",row.Hydro_GW,"#1976D2"),
        ("🌿","Biomass",row.Biomass_GW,"#66BB6A"),
        ("🌋","Geothermal",row.Geothermal_GW,"#8D6E63")
        ],growths):
        
            st.markdown(f"""     
        <div class="metric-card">    
        <h3>{icon} {label}</h3>
        <h2>{val:.1f} GW</h2>      
        <p style="color:green;">⬆ {g}% Growth</p>     
        </div> 
        """,unsafe_allow_html=True)

    trend=df[df.Country==country].sort_values("Year")
    fig2=px.area(

    trend,
    x="Year",    
    y=["Solar_GW","Wind_GW","Hydro_GW"],    
    title=f"{country} Renewable Growth",    
    color_discrete_sequence=[   
    "#F9A826",    
    "#29B6F6",    
    "#1976D2"   
    ]
    )
    
    fig2.update_layout(   
    template="plotly_white",    
    hovermode="x unified",    
    paper_bgcolor="#F8FFF9",  
    plot_bgcolor="#F8FFF9"   
    )
    st.plotly_chart(fig2,use_container_width=True)

    st.download_button(
        "📥 Download Dataset",
        filtered.to_csv(index=False),
        "renewable_data.csv",
        "text/csv"
    )

    growth=(trend.iloc[-1].Solar_GW-trend.iloc[0].Solar_GW)/trend.iloc[0].Solar_GW*100
    
    st.markdown(f"""
    <div class="ai-box">
    
    <h3>🤖 AI Insight</h3>
    
    Solar Growth
    
    <b>{growth:.1f}%</b>
    
    <br><br>
    
    {recommendation}
    
    </div>
    
    """,unsafe_allow_html=True)

    st.subheader("🌍 Global Renewable Capacity")
    mapfig = px.choropleth(
        df[df.Year==year],
        locations="Country",
        locationmode="country names",
        color="Total_GW",
        projection="natural earth",
        hover_name="Country",
        hover_data={
            "Total_GW":True,
            "Population_M":True,
            "GDP_Billion_USD":True
        },
        color_continuous_scale=[
            "#D7F5DC",
            "#A5D6A7",
            "#66BB6A",
            "#43A047",
            "#1B5E20"
        ]
    )
    
    mapfig.update_layout(    
        template="plotly_white",  
        height=650,
        paper_bgcolor="#F8FFF9",
        margin=dict(l=0,r=0,t=40,b=0)
    )
    
    st.plotly_chart(mapfig,use_container_width=True)

# ==========================================
# 💬 AI CHATBOT
# ==========================================

elif page == "💬 AI Chatbot":

    st.markdown(f"""
    <div style="
    background:linear-gradient(135deg,#2E7D32,#43A047,#66BB6A);
    padding:30px;
    border-radius:20px;
    color:white;
    ">
    
    <h1>🤖 Renewable Energy Assistant</h1>
    
    <h4>Your AI Guide for Clean & Sustainable Energy</h4>
    
    <p>
    Currently viewing:
    <b>{country}</b> |
    <b>{year}</b>
    </p>
    
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## ⚡ Quick Questions")
    st.caption("Click a button to instantly ask the AI assistant.")
    
    # Clear Chat Button
    top_left, top_right = st.columns([6, 1])
    
    with top_right:
        if st.button("🗑 Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    
    # Quick Question Buttons
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("☀️ Solar", use_container_width=True):
            st.session_state.quick_question = "What is the solar capacity?"
    
    with col2:
        if st.button("💨 Wind", use_container_width=True):
            st.session_state.quick_question = "What is the wind capacity?"
    
    with col3:
        if st.button("🌍 GDP", use_container_width=True):
            st.session_state.quick_question = "What is the GDP?"
    
    with col4:
        if st.button("⚡ Total", use_container_width=True):
            st.session_state.quick_question = "What is the total renewable capacity?"
            

    st.markdown("## 🌿 What can I help you with?")

    col1,col2,col3 = st.columns(3)
    
    with col1:
        st.info("""
    ☀️ **Renewable Sources**
    
    Solar
    
    Wind
    
    Hydro
    
    Biomass
    
    Geothermal
    """)
    
    with col2:
        st.success("""
    📊 **Country Statistics**
    
    Renewable Capacity
    
    GDP
    
    Population
    
    Growth Trends
    """)
    
    with col3:
        st.warning("""
    💡 **Energy Tips**
    
    Save Electricity
    
    Green Habits
    
    Climate Facts
    
    Sustainability
    """)
        
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar="👤" if msg["role"]=="user" else "🌿"):
            st.write(msg["content"])

    # Chat Input
    q = st.chat_input("Ask about renewable energy...")

    # Use quick question if selected
    if "quick_question" in st.session_state:
        q = st.session_state.pop("quick_question")

    if q:

        # Show user message
        with st.chat_message("user", avatar="👤"):
            st.write(q)

        # Save user message
        st.session_state.messages.append({
            "role": "user",
            "content": q
        })

        query = q.lower()

        # AI Responses

        if any(word in query for word in ["solar", "sun", "photovoltaic"]):
            ans = (
                f"☀️ **{country}** currently has **{row['Solar_GW']:.1f} GW** "
                f"of installed solar capacity in **{year}**."
            )

        elif any(word in query for word in ["wind", "turbine"]):
            ans = (
                f"💨 **{country}** currently has **{row['Wind_GW']:.1f} GW** "
                f"of installed wind capacity in **{year}**."
            )

        elif any(word in query for word in ["hydro", "water", "dam"]):
            ans = (
                f"💧 **{country}** currently has **{row['Hydro_GW']:.1f} GW** "
                f"of hydropower capacity in **{year}**."
            )

        elif any(word in query for word in ["biomass", "organic"]):
            ans = (
                f"🌿 **{country}** currently has **{row['Biomass_GW']:.1f} GW** "
                f"of biomass energy capacity in **{year}**."
            )

        elif any(word in query for word in ["geothermal", "earth", "heat"]):
            ans = (
                f"🌋 **{country}** currently has **{row['Geothermal_GW']:.1f} GW** "
                f"of geothermal energy capacity in **{year}**."
            )

        elif "population" in query:
            ans = (
                f"🌍 The estimated population of **{country}** in **{year}** "
                f"is **{row['Population_M']:.0f} million**."
            )

        elif "gdp" in query:
            ans = (
                f"💰 The GDP of **{country}** in **{year}** "
                f"is approximately **${row['GDP_Billion_USD']:.0f} Billion USD**."
            )

        elif "total" in query or "renewable" in query:
            ans = (
                f"⚡ **{country}** has a total renewable energy capacity of "
                f"**{row['Total_GW']:.1f} GW** in **{year}**."
            )

        elif "highest" in query or "top" in query:
            energy = {
                "Solar": row["Solar_GW"],
                "Wind": row["Wind_GW"],
                "Hydro": row["Hydro_GW"],
                "Biomass": row["Biomass_GW"],
                "Geothermal": row["Geothermal_GW"]
            }

            highest = max(energy, key=energy.get)

            ans = (
                f"🏆 The largest renewable energy source in **{country}** "
                f"is **{highest}**, with **{energy[highest]:.1f} GW**."
            )

        elif "help" in query:
            ans = (
                "🌿 You can ask me questions like:\n\n"
                "• Solar capacity\n"
                "• Wind energy\n"
                "• Hydro power\n"
                "• Biomass\n"
                "• Geothermal\n"
                "• Total renewable capacity\n"
                "• GDP\n"
                "• Population\n"
                "• Highest renewable source"
            )

        else:
            ans = (
                "🤖 Sorry, I couldn't understand that.\n\n"
                "Try asking:\n"
                "- What is the solar capacity?\n"
                "- What is the total renewable capacity?\n"
                "- What is the GDP?\n"
                "- Which is the highest renewable source?\n"
                "- What is the wind capacity?"
            )

        # Show assistant response
        with st.chat_message("assistant", avatar="🌿"):
            st.write(ans)

        # Save assistant response
        st.session_state.messages.append({
            "role": "assistant",
            "content": ans
        })

# ==========================================
# 📚 LEARN
# ==========================================

elif page=="📚 Learn":
    topic=st.radio("Choose an Energy Source",["☀️ Solar","💨 Wind","💧 Hydro","🌿 Biomass","🌋 Geothermal"],horizontal=True)
    
    if "Solar" in topic:
        st.image("assets/solar.png",use_container_width=True)
        st.success("Solar energy converts sunlight into electricity using photovoltaic cells.")
        st.info("""
        💡 Did You Know?
        
        The Sun provides more energy to Earth in one hour than humanity uses in an entire year.
        """)

        col1,col2=st.columns(2)

        with col1:
            st.markdown("""
### ✅ Advantages

- Renewable
- Clean energy
- Low maintenance
- Reduces electricity bills
- No greenhouse gas emissions
""")

        with col2:
            st.markdown("""
### ⚠️ Disadvantages

- Weather dependent
- Initial installation cost
- Requires space
- Lower efficiency at night
""")

        st.markdown("""
### 🌍 Leading Countries

🇨🇳 China
🇺🇸 USA
🇮🇳 India
🇩🇪 Germany
""")

    elif "Wind" in topic:

        st.image("assets/wind.png",use_container_width=True)
        st.success("Wind turbines convert wind energy into electricity.")
        st.info("""
        💡 Did You Know?
        
        Modern offshore wind turbines can power thousands of homes.
        """)

        col1,col2=st.columns(2)

        with col1:
            st.markdown("""
### ✅ Advantages

- Renewable
- Low operating cost
- No fuel needed
- Clean electricity
""")

        with col2:
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

    elif "Hydro" in topic:

        st.image("assets/hydro.png",use_container_width=True)
        st.success("Hydropower generates electricity from flowing water.")
        st.info("""
        💡 Did You Know?
        
        Hydropower supplies around 16% of the world's electricity.
        """)

        st.markdown("""
### ✅ Advantages

- Reliable
- Clean
- Long lifespan

### ⚠️ Disadvantages

- Expensive dams
- Environmental impact

### 🌍 Leading Countries

🇨🇳 China
🇧🇷 Brazil
🇨🇦 Canada
🇮🇳 India
""")

    elif "Biomass" in topic:

        st.image("assets/biomass.png",use_container_width=True)
        st.success("Biomass uses organic materials like crop waste and wood.")
        st.info("""
        💡 Did You Know?
        
        Agricultural waste can be converted into clean electricity.
        """)

        st.markdown("""
### ✅ Advantages

- Uses waste
- Renewable
- Produces heat and electricity

### ⚠️ Disadvantages

- Air pollution
- Large land requirement

### 🌍 Leading Countries

🇺🇸 USA
🇧🇷 Brazil
🇮🇳 India
""")

    elif "Geothermal" in topic:

        st.image("assets/geothermal.png",use_container_width=True)
        st.success("Geothermal energy comes from heat inside the Earth.")
        st.info("""
        💡 Did You Know?
        
        Geothermal plants can generate electricity 24 hours a day.
        """)

        st.markdown("""
### ✅ Advantages

- Reliable
- Available 24/7
- Very low emissions

### ⚠️ Disadvantages

- Expensive drilling
- Location dependent

### 🌍 Leading Countries

🇮🇸 Iceland
🇺🇸 USA
🇮🇩 Indonesia
🇵🇭 Philippines
""")

# ==========================================
# 🌍 COMPARE COUNTRIES
# ==========================================

elif page == "🌍 Compare":

    st.title("🌍 Compare Renewable Energy")

    col1, col2 = st.columns(2)

    with col1:
        country1 = st.selectbox(
            "Country 1",
            df["Country"].unique(),
            key="compare1"
        )

    with col2:
        country2 = st.selectbox(
            "Country 2",
            df["Country"].unique(),
            index=1,
            key="compare2"
        )

    d1 = df[
        (df["Country"] == country1) &
        (df["Year"] == year)
    ].iloc[0]

    d2 = df[
        (df["Country"] == country2) &
        (df["Year"] == year)
    ].iloc[0]

    compare = px.bar(

        x=[
            "Solar",
            "Wind",
            "Hydro",
            "Biomass",
            "Geothermal"
        ],

        y=[
            d1["Solar_GW"],
            d1["Wind_GW"],
            d1["Hydro_GW"],
            d1["Biomass_GW"],
            d1["Geothermal_GW"]
        ],

        color_discrete_sequence=["#43A047"],

        labels={"x": "Energy Source", "y": "GW"},

        title=f"{country1} vs {country2}"
    )

    compare.add_bar(

        x=[
            "Solar",
            "Wind",
            "Hydro",
            "Biomass",
            "Geothermal"
        ],

        y=[
            d2["Solar_GW"],
            d2["Wind_GW"],
            d2["Hydro_GW"],
            d2["Biomass_GW"],
            d2["Geothermal_GW"]
        ],

        name=country2,

        marker_color="#1976D2"

    )

    compare.update_layout(
        template="plotly_white",
        barmode="group",
        height=550
    )

    st.plotly_chart(compare, use_container_width=True)

    st.markdown("### 📊 Summary")

    c1, c2 = st.columns(2)

    with c1:
        st.metric(
            f"{country1} Total Capacity",
            f"{d1['Total_GW']:.1f} GW"
        )

    with c2:
        st.metric(
            f"{country2} Total Capacity",
            f"{d2['Total_GW']:.1f} GW"
        )

    if d1["Total_GW"] > d2["Total_GW"]:
        winner = country1
    else:
        winner = country2

    st.markdown(f"""
    <div class="metric-card">
    
    <h2>🏆 Winner</h2>
    
    <h1>{winner}</h1>
    
    <h3>Total Capacity</h3>
    
    <h2>{max(d1['Total_GW'],d2['Total_GW']):.1f} GW</h2>
    
    </div>
    """,unsafe_allow_html=True)

# ==========================================
# 📊 TABLEAU ANALYTICS
# ==========================================

elif page=="📊 Tableau Analytics":

    st.title("📊 Renewable Energy Analytics Dashboard")

    st.markdown("""
Explore renewable energy investments, renewable percentages,
GDP vs Investment, and global renewable trends through
an interactive Tableau dashboard.
""")

    st.components.v1.iframe(
        "https://public.tableau.com/views/Renewableawarenesschatbot/Dashboard1?:showVizHome=no",
        height=850,
        scrolling=True
    )
    
# ==========================================
# 🌱 CLIMATE IMPACT
# ==========================================

elif page == "🌱 Climate Impact":

    st.title("🌱 Climate Impact Calculator")

    st.markdown("""
    Estimate the positive environmental impact of renewable energy generation
    based on the selected **country** and **year**.
    """)

    # Calculate impact based on Total Renewable Capacity
    co2 = row["Total_GW"] * 1200          # Approx. tonnes of CO₂ avoided per GW/year
    trees = int(co2 / 21)                # Approx. CO₂ absorbed by one tree per year
    homes = int(row["Total_GW"] * 500000) # Approx. homes powered
    cars = int(co2 / 4600)               # Approx. cars' annual emissions offset

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

    st.info(f"""
### 🌿 Environmental Impact Summary

For **{country} ({year})**, the estimated renewable energy capacity of **{row['Total_GW']:.1f} GW** could:

- 🌍 Avoid approximately **{co2:,.0f} tonnes of CO₂ emissions** annually.
- 🌳 Have an environmental impact equivalent to planting **{trees:,} trees**.
- 🏠 Supply clean electricity to approximately **{homes:,} homes**.
- 🚗 Offset the annual emissions of about **{cars:,} passenger vehicles**.

*These values are educational estimates based on commonly used conversion factors.*
""")

# ==========================================
# 🎮 GREEN QUIZ
# ==========================================

elif page == "🎮 Green Quiz":

    st.title("🎮 Green Energy Challenge")

    st.markdown("""
Test your knowledge of renewable energy and see how green you are!
""")

    questions = [
        {
            "question": "Which renewable energy source uses sunlight to generate electricity?",
            "options": ["Wind", "Solar", "Hydro", "Biomass"],
            "answer": "Solar"
        },
        {
            "question": "Which energy source uses flowing water to produce electricity?",
            "options": ["Solar", "Hydro", "Wind", "Geothermal"],
            "answer": "Hydro"
        },
        {
            "question": "Which renewable energy source comes from heat inside the Earth?",
            "options": ["Wind", "Biomass", "Geothermal", "Solar"],
            "answer": "Geothermal"
        },
        {
            "question": "Which gas is mainly reduced by using renewable energy?",
            "options": ["Nitrogen", "Oxygen", "Carbon Dioxide", "Hydrogen"],
            "answer": "Carbon Dioxide"
        },
        {
            "question": "Which country currently has one of the world's largest solar energy capacities?",
            "options": ["India", "China", "Brazil", "Australia"],
            "answer": "China"
        }
    ]

    score = 0

    for i, q in enumerate(questions):

        answer = st.radio(
            q["question"],
            q["options"],
            key=i
        )

        if answer == q["answer"]:
            score += 1
            st.progress(score/len(questions))

    if st.button("✅ Submit Quiz"):

        st.success(f"Your Score: {score} / {len(questions)}")
        stars="⭐"*score+"☆"*(5-score)
        st.markdown(f"""
        ## {stars}
        ### Eco Score
        # {score}/5
        """)
        percentage = score / len(questions) * 100
        st.progress(percentage / 100)

        if percentage == 100:
            st.balloons()
            st.success("🏆 Excellent! You're a Renewable Energy Champion!")

        elif percentage >= 80:
            st.success("🌱 Great Job! You have strong knowledge of renewable energy.")

        elif percentage >= 60:
            st.info("👍 Good effort! Keep learning about clean energy.")

        else:
            st.warning("📚 Keep exploring renewable energy to improve your score!")

# ==========================================
# 📄 REPORT
# ==========================================

elif page == "📄 Report":

    st.title("📄 Sustainability Report")

    st.markdown(f"""
## Renewable Energy Summary

**Country:** {country}

**Year:** {year}

### Key Statistics

- ⚡ **Total Renewable Capacity:** {row['Total_GW']:.1f} GW
- 🌍 **Population:** {row['Population_M']:.0f} Million
- 💰 **GDP:** ${row['GDP_Billion_USD']:.0f} Billion

### Renewable Energy Breakdown

- ☀️ Solar: {row['Solar_GW']:.1f} GW
- 💨 Wind: {row['Wind_GW']:.1f} GW
- 💧 Hydro: {row['Hydro_GW']:.1f} GW
- 🌿 Biomass: {row['Biomass_GW']:.1f} GW
- 🌋 Geothermal: {row['Geothermal_GW']:.1f} GW

### Environmental Benefits

- 🌍 CO₂ Saved: **{co2:,.0f} Tons**
- 🌳 Equivalent Trees: **{trees:,}**
- 🏠 Homes Powered: **{homes:,}**
- 🚗 Cars Removed: **{cars:,}**

---

**Generated by Renewable Energy Awareness Chatbot**

*Built for the 1M1B Green Internship.*
""")

    report = f"""
Renewable Energy Awareness Chatbot

Country: {country}
Year: {year}

Total Capacity: {row['Total_GW']:.1f} GW
Population: {row['Population_M']:.0f} Million
GDP: ${row['GDP_Billion_USD']:.0f} Billion

Solar: {row['Solar_GW']:.1f} GW
Wind: {row['Wind_GW']:.1f} GW
Hydro: {row['Hydro_GW']:.1f} GW
Biomass: {row['Biomass_GW']:.1f} GW
Geothermal: {row['Geothermal_GW']:.1f} GW

CO₂ Saved: {co2:,.0f} Tons
Equivalent Trees: {trees:,}
Homes Powered: {homes:,}
Cars Removed: {cars:,}

Recommendation:
{recommendation}

Generated by Renewable Energy Awareness Chatbot
"""

    from io import BytesIO

    buffer = BytesIO()
    
    doc = SimpleDocTemplate(buffer)
    
    styles = getSampleStyleSheet()
    
    story = []
    
    story.append(Paragraph("<b>Renewable Energy Report</b>", styles["Title"]))
    
    story.append(Paragraph(f"Country: {country}", styles["BodyText"]))
    
    story.append(Paragraph(f"Year: {year}", styles["BodyText"]))
    
    story.append(Paragraph(f"Total Capacity: {row['Total_GW']:.1f} GW", styles["BodyText"]))
    
    story.append(Paragraph(f"Solar: {row['Solar_GW']:.1f} GW", styles["BodyText"]))
    story.append(Paragraph(f"Wind: {row['Wind_GW']:.1f} GW", styles["BodyText"]))
    story.append(Paragraph(f"Hydro: {row['Hydro_GW']:.1f} GW", styles["BodyText"]))
    story.append(Paragraph(f"Biomass: {row['Biomass_GW']:.1f} GW", styles["BodyText"]))
    story.append(Paragraph(f"Geothermal: {row['Geothermal_GW']:.1f} GW", styles["BodyText"]))
    
    story.append(Paragraph(f"Population: {row['Population_M']:.0f} Million", styles["BodyText"]))
    story.append(Paragraph(f"GDP: ${row['GDP_Billion_USD']:.0f} Billion", styles["BodyText"]))
    
    story.append(Paragraph(f"CO₂ Saved: {co2:,.0f} Tons", styles["BodyText"]))
    story.append(Paragraph(f"Equivalent Trees: {trees:,}", styles["BodyText"]))
    story.append(Paragraph(f"Homes Powered: {homes:,}", styles["BodyText"]))
    story.append(Paragraph(f"Cars Removed: {cars:,}", styles["BodyText"]))

    story.append(
        Paragraph(
            f"<b>AI Recommendation:</b> {recommendation}",
            styles["BodyText"]
        )
    )
    doc.build(story)
    
    st.download_button(
        "📄 Download PDF Report",
        buffer.getvalue(),
        "Renewable_Report.pdf",
        mime="application/pdf"
    )

st.markdown("---")
st.markdown("""
<div class="footer">
st.markdown("""
<div class="footer">

<h2>🌍 Renewable Energy Awareness Chatbot</h2>

Built with ❤️ for the <b>1M1B Green Internship</b>

<br>

Supporting <b>SDG 7 – Affordable & Clean Energy</b>

</div>
""",unsafe_allow_html=True)
