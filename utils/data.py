import plotly.express as px
import streamlit as st

@st.cache_data
def load_data():
    return px.data.gapminder()
