import streamlit as st
import streamlit.components.v1 as components


def show_tableau():
    """Display the Tableau Analytics dashboard."""

    st.title("📊 Renewable Energy Analytics Dashboard")

    st.markdown("""
Explore renewable energy investments, renewable percentages,
GDP vs Investment, and global renewable trends through an
interactive Tableau dashboard.
""")

    st.info(
        "💡 Tip: Use the Tableau filters and interactive charts "
        "to explore renewable energy trends across countries."
    )

    components.iframe(
        "https://public.tableau.com/views/Renewableawarenesschatbot/Dashboard1?:showVizHome=no",
        height=950,
        scrolling=True,
    )

    st.markdown("---")

    st.success(
        "Data Source: Tableau Public • Renewable Energy Awareness Chatbot"
    )
