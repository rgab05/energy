import streamlit as st
import pandas as pd
import plotly.express as px
import pydeck as pdk

# --------------------
# PAGE CONFIG
# --------------------
st.set_page_config(
    page_title="Clean Streamlit Dashboard",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
[data-testid="stSidebar"] {
    background-color: #0f172a;
}
</style>
""", unsafe_allow_html=True)



# --------------------
# LOAD PUBLIC DATA (GAPMINDER)
# --------------------
@st.cache_data
def load_data():
    df = px.data.gapminder()
    return df

df = load_data()

# --------------------
# SIDEBAR NAVIGATION (NAV BAR)
# --------------------
st.sidebar.title("🚀 Navigation")
page = st.sidebar.radio(
    "Go to",
    ["🏠 Home", "📈 Analytics", "ℹ️ About"]
)

# --------------------
# 🏠 LANDING PAGE
# --------------------
if page == "🏠 Home":

    st.title("🌍 Global Data Dashboard")
    st.markdown("Clean UI starter template built with **Streamlit**.")

    # --- KPI ROW ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Countries", df["country"].nunique())
    col2.metric("Total Records", len(df))
    col3.metric("Max Life Expectancy", round(df["lifeExp"].max(), 1))

    st.divider()

    # --------------------
    # MAP + CHART ROW
    # --------------------
    left, right = st.columns([1.2, 1])

    with left:
        st.subheader("🗺️ Global Life Expectancy Map (2007)")
    
        df_2007 = df[df["year"] == 2007]
    
        map_fig = px.scatter_geo(
            df_2007,
            locations="iso_alpha",
            color="lifeExp",
            hover_name="country",
            size="pop",
            projection="natural earth",
            title="Life Expectancy by Country (2007)",
            template="plotly_white",
        )
    
        st.plotly_chart(map_fig, use_container_width=True)


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

# --------------------
# 📈 ANALYTICS PAGE
# --------------------
elif page == "📈 Analytics":

    st.title("📈 Advanced Analytics")

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

# --------------------
# ℹ️ ABOUT PAGE
# --------------------
elif page == "ℹ️ About":

    st.title("ℹ️ About This App")

    st.markdown("""
    This is a **clean Streamlit dashboard template** featuring:

    ✅ Navigation bar  
    ✅ Interactive maps  
    ✅ Data tables  
    ✅ Dynamic charts  
    ✅ Public dataset  
    ✅ Production-ready layout  

    **Built with:**
    - Streamlit
    - Plotly
    - PyDeck
    - Pandas

    Perfect for:
    - Data science dashboards
    - Business analytics
    - SaaS MVPs
    - ML demos
    """)

    st.success("You're ready to customize this for your own project 🚀")
