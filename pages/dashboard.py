import streamlit as st
import plotly.express as px

def show_dashboard(df, row, year, country):

    st.title("🏠 Dashboard")

    st.metric(
        "Total Capacity",
        f"{row['Total_GW']:.1f} GW"
    )

    col1,col2,col3,col4=st.columns(4)

    cards=[
    ("⚡","Total Capacity",f"{row.Total_GW:.1f} GW","#2E7D32"),
    ("🌍","Population",f"{row.Population_M:.0f} M","#1976D2"),
    ("💰","GDP",f"${row.GDP_Billion_USD:.0f} B","#F9A826"),
    ("🌱","Green Score",f"{min(100,round(row.Total_GW/5))}/100","#43A047")
    ]
    
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
