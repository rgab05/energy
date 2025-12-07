import streamlit as st
from utils.data import load_data
from utils.theme import apply_theme
from pages import home, analytics, about

# --------------------
# PAGE CONFIG
# --------------------
st.set_page_config(page_title="Streamlit Dashboard", page_icon="📊", layout="wide")

# --------------------
# THEME TOGGLE
# --------------------
theme_mode = st.sidebar.radio("🌗 Theme Mode", ["Dark", "Light"])
apply_theme(theme_mode)

# --------------------
# LOAD DATA
# --------------------
df = load_data()

# --------------------
# NAVIGATION
# --------------------
st.sidebar.title("🚀 Navigation")
page = st.sidebar.radio("Go to", ["🏠 Home", "📈 Analytics", "ℹ️ About"])

# --------------------
# DISPLAY PAGE
# --------------------
if page == "🏠 Home":
    home.show(df)
elif page == "📈 Analytics":
    analytics.show(df)
elif page == "ℹ️ About":
    about.show()
