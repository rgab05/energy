import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------
# PAGE CONFIG
# --------------------
st.set_page_config(
    page_title="Clean Streamlit Dashboard",
    page_icon="📊",
    layout="wide"
)

# --------------------
# LOAD EXTERNAL CSS
# --------------------
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("assets/styles.css")

# --------------------
# THEME TOGGLE
# --------------------
theme_mode = st.sidebar.toggle("🌗 Dark Mode", value=True)
mode_class = "dark-mode" if theme_mode else "light-mode"

st.markdown(f"""<div class="{mode_class}">""", unsafe_allow_html=True)

# --------------------
# LOAD PUBLIC DATA
# --------------------
@st.cache_data
def load_data():
    df = px.data.gapminder()
    return df

df = load_data()

# --------------------
# SIDEBAR NAVIGATION
# --------------------
st.sidebar.title("🚀 Navigation")

page = st.sidebar.radio(
    "Go to",
    ["🏠 Home", "📈 Analytics", "ℹ️ About"]
)

# ============================================================
# 🏠 HOME PAGE
# ============================================================
if page == "🏠 Home":

    st.title("🌍 Global Data Dashboard")
    st.markdown("Modern Streamlit template with **dark/light mode**, **maps**, and **analytics**.")

    # --------------------
    # KPI ROW
    # --------------------
    col1, col2, col3 = st.columns(3)

    col1.metric("🌎 Total Countries", df["country"].nunique())
    col2.metric("📊 Total Records", len(df))
    col3.metric("❤️ Max Life Expectancy", round(df["lifeExp"].max(), 1))

    st.divider()

    # --------------------
    # MAP + CHART
    # --------------------
    left, right = st.columns([1.3, 1])

    # ✅ ANIMATED MAP
    with left:
        st.subheader("🗺️ Global Life Expectancy Over Time")

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
            size_max=40,
        )

        st.plotly_chart(map_fig, use_container_width=True)

    # ✅ BAR CHART
    with right:
        st.subheader("📊 Life Expectancy by Continent (2007)")

        df_2007 = df[df["year"] == 2007]

        fig = px.bar(
            df_2007,
            x="continent",
            y="lifeExp",
            color="continent",
            title="Life Expectancy by Continent",
            template="plotly_white"
        )

        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # --------------------
    # DATA TABLE
    # --------------------
    st.subheader("📄 Country Data Table (2007)")

    st.dataframe(
        df_2007[["country", "continent", "lifeExp", "gdpPercap", "pop"]],
        use_container_width=True
    )

# ============================================================
# 📈 ANALYTICS PAGE
# ============================================================
elif page == "📈 Analytics":

    st.title("📈 Advanced Country Analytics")

    country = st.selectbox("Select a Country", df["country"].unique())

    filtered = df[df["country"] == country]

    line_fig = px.line(
        filtered,
        x="year",
        y="lifeExp",
        title=f"Life Expectancy Over Time — {country}",
        markers=True,
        template="plotly_white"
    )

    st.plotly_chart(line_fig, use_container_width=True)

# ============================================================
# ℹ️ ABOUT PAGE
# ============================================================
elif page == "ℹ️ About":

    st.title("ℹ️ About This Dashboard")

    st.markdown("""
    This is a **clean, modern Streamlit dashboard template** with:

    ✅ Multi-page navigation  
    ✅ Animated world maps  
    ✅ Interactive charts  
    ✅ Data tables  
    ✅ Dark / Light mode toggle  
    ✅ External CSS styling  
    ✅ Google Fonts  
    ✅ Streamlit Cloud ready  

    **Built with:**
    - Python
    - Streamlit
    - Plotly
    - Pandas

    Perfect for:
    - 📊 Business dashboards  
    - 🤖 Machine learning demos  
    - 🌍 Public data apps  
    - 🚀 Startup MVPs  
    """)

    st.success("You're now running a fully production-ready Streamlit UI 🚀")

# --------------------
# CLOSE THEME WRAPPER
# --------------------
st.markdown("</div>", unsafe_allow_html=True)
