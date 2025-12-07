import streamlit as st
import pandas as pd
import plotly.express as px
import os
from hashlib import sha256

# --------------------
# PAGE CONFIG
# --------------------
st.set_page_config(
    page_title="Streamlit Dashboard",
    page_icon="📊",
    layout="wide"
)

# --------------------
# LOAD CSS
# --------------------
def load_css(file_path="assets/styles.css"):
    try:
        with open(file_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("CSS file not found. Continue without custom styling.")

load_css()

# --------------------
# USER CREDENTIALS (ENVIRONMENT VARIABLES)
# --------------------
# Set these environment variables in your deployment platform or locally
# Example: export ADMIN_PASSWORD_HASH=$(echo -n "password123" | sha256sum | awk '{print $1}')
USER_CREDENTIALS = {
    "admin": os.getenv("ADMIN_PASSWORD_HASH"),
    "user": os.getenv("USER_PASSWORD_HASH")
}

# --------------------
# LOGIN LOGIC
# --------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def login(username, password):
    if username in USER_CREDENTIALS and USER_CREDENTIALS[username]:
        if sha256(password.encode()).hexdigest() == USER_CREDENTIALS[username]:
            st.session_state.authenticated = True
            st.success(f"Logged in as {username}")
            return True
    st.error("Invalid username or password")
    return False

# --------------------
# LOGIN PAGE
# --------------------
if not st.session_state.authenticated:
    st.title("🔒 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        login(username, password)
    st.stop()  # Stop the rest of the app until login
     
# --------------------
# THEME TOGGLE
# --------------------
theme_mode = st.sidebar.radio("🌗 Theme Mode", ["Dark", "Light"])
body_class = "dark-mode" if theme_mode == "Dark" else "light-mode"
st.markdown(f'<div class="{body_class}">', unsafe_allow_html=True)

# --------------------
# LOAD DATA
# --------------------
@st.cache_data
def load_data():
    return px.data.gapminder()

df = load_data()

# --------------------
# SIDEBAR NAVIGATION
# --------------------
st.sidebar.title("🚀 Navigation")
page = st.sidebar.radio("Go to", ["🏠 Home", "📈 Analytics", "ℹ️ About"])

# --------------------
# COUNTRY DRILL-DOWN
# --------------------
selected_country = None
if page in ["🏠 Home", "📈 Analytics"]:
    selected_country = st.sidebar.selectbox(
        "🔍 Select Country (Drill-down)",
        ["All"] + list(df["country"].unique()),
        index=0
    )

# ============================================================
# 🏠 HOME PAGE
# ============================================================
if page == "🏠 Home":

    st.title("🌍 Global Data Dashboard")
    st.markdown("Modern Streamlit template with **dark/light mode**, **maps**, and **analytics**.")

    # KPIs
    col1, col2, col3 = st.columns(3)
    if selected_country != "All":
        df_country = df[df["country"] == selected_country]
        col1.metric("🌎 Country", selected_country)
        col2.metric("❤️ Max Life Expectancy", round(df_country["lifeExp"].max(), 1))
        col3.metric("📊 Population (2007)", int(df_country[df_country["year"]==2007]["pop"].values[0]))
    else:
        col1.metric("🌎 Total Countries", df["country"].nunique())
        col2.metric("📊 Total Records", len(df))
        col3.metric("❤️ Max Life Expectancy", round(df["lifeExp"].max(), 1))

    st.divider()

    # MAP + BAR CHART
    left, right = st.columns([1.3, 1])

    with left:
        st.subheader("🗺️ Global Life Expectancy Map")

        if selected_country != "All":
            map_df = df[df["country"] == selected_country]
            map_fig = px.scatter_geo(
                map_df,
                locations="iso_alpha",
                color="lifeExp",
                hover_name="country",
                size="pop",
                projection="natural earth",
                title=f"Life Expectancy — {selected_country}",
                template="plotly_white",
                size_max=40
            )
        else:
            map_fig = px.scatter_geo(
                df,
                locations="iso_alpha",
                color="lifeExp",
                hover_name="country",
                size="pop",
                animation_frame="year",
                projection="natural earth",
                title="Life Expectancy by Country (1952–2007)",
                template="plotly_white",
                size_max=40
            )
        st.plotly_chart(map_fig, use_container_width=True)

    with right:
        st.subheader("📊 Life Expectancy by Continent / Country")
        df_2007 = df[df["year"] == 2007]
        if selected_country != "All":
            df_bar = df_2007[df_2007["country"] == selected_country]
            x_col = "country"
            color_col = "country"
        else:
            df_bar = df_2007
            x_col = "continent"
            color_col = "continent"

        bar_fig = px.bar(
            df_bar,
            x=x_col,
            y="lifeExp",
            color=color_col,
            title="Life Expectancy (2007)",
            template="plotly_white"
        )
        st.plotly_chart(bar_fig, use_container_width=True)

    st.divider()

    # DATA TABLE
    st.subheader("📄 Country Data Table (2007)")
    st.dataframe(df_bar[["country","continent","lifeExp","gdpPercap","pop"]], use_container_width=True)

# ============================================================
# 📈 ANALYTICS PAGE
# ============================================================
elif page == "📈 Analytics":
    st.title("📈 Advanced Analytics")
    if selected_country != "All":
        filtered = df[df["country"] == selected_country]

        fig1 = px.line(
            filtered,
            x="year",
            y="lifeExp",
            title=f"Life Expectancy Over Time — {selected_country}",
            markers=True,
            template="plotly_white"
        )
        st.plotly_chart(fig1, use_container_width=True)

        fig2 = px.line(
            filtered,
            x="year",
            y="pop",
            title=f"Population Over Time — {selected_country}",
            markers=True,
            template="plotly_white"
        )
        st.plotly_chart(fig2, use_container_width=True)

        fig3 = px.line(
            filtered,
            x="year",
            y="gdpPercap",
            title=f"GDP Per Capita Over Time — {selected_country}",
            markers=True,
            template="plotly_white"
        )
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("Select a country from the sidebar to view detailed analytics.")

# ============================================================
# ℹ️ ABOUT PAGE
# ============================================================
elif page == "ℹ️ About":
    st.title("ℹ️ About This Dashboard")
    st.markdown("""
    This is a **secure, production-ready Streamlit dashboard** with:

    ✅ Login authentication via environment variables  
    ✅ Multi-page navigation  
    ✅ Animated world maps  
    ✅ Interactive charts  
    ✅ Country drill-down analytics  
    ✅ Dark / Light mode toggle  
    ✅ External CSS styling  
    ✅ Google Fonts  
    """)

# --------------------
# CLOSE THEME WRAPPER
# --------------------
st.markdown("</div>", unsafe_allow_html=True)
