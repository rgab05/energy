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
def load_css(file_path="assets/styles.css"):
    try:
        with open(file_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("CSS file not found. Continue without custom styling.")

load_css()

# --------------------
# DARK / LIGHT MODE TOGGLE
# --------------------
theme_mode = st.sidebar.toggle("🌗 Dark Mode", value=True)
mode_class = "dark-mode" if theme_mode else "light-mode"
st.markdown(f'<div class="{mode_class}">', unsafe_allow_html=True)

# --------------------
# LOAD PUBLIC DATA (GAPMINDER)
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
page = st.sidebar.radio("Go to", ["🏠 Home", "📈 Analytics", "ℹ️ About"])

# --------------------
# COUNTRY DRILL-DOWN SELECTION
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

    # --------------------
    # KPIs
    # --------------------
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

    # --------------------
    # MAP + BAR CHART
    # --------------------
    left, right = st.columns([1.3, 1])

    # Animated Map
    with left:
        st.subheader("🗺️ Global Life Expectancy Over Time")
        if selected_country != "All":
            map_df = df[df["country"] == selected_country]
            map_title = f"Life Expectancy Over Time — {selected_country}"
            anim_frame = None
        else:
            map_df = df
            map_title = "Life Expectancy by Country (1952–2007)"
            anim_frame = "year"

        map_fig = px.scatter_geo(
            map_df,
            locations="iso_alpha",
            color="lifeExp",
            hover_name="country",
            size="pop",
            animation_frame=anim_frame,
            projection="natural earth",
            title=map_title,
            template="plotly_white",
            size_max=40,
        )
        st.plotly_chart(map_fig, use_container_width=True)

    # Bar Chart
    with right:
        st.subheader("📊 Life Expectancy by Continent (2007)")
        df_2007 = df[df["year"] == 2007]
        if selected_country != "All":
            df_bar = df_2007[df_2007["country"] == selected_country]
        else:
            df_bar = df_2007

        fig = px.bar(
            df_bar,
            x="continent" if selected_country=="All" else "country",
            y="lifeExp",
            color="continent" if selected_country=="All" else "country",
            title="Life Expectancy",
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # --------------------
    # DATA TABLE
    # --------------------
    st.subheader("📄 Country Data Table (2007)")
    if selected_country != "All":
        st.dataframe(df_bar[["country","continent","lifeExp","gdpPercap","pop"]], use_container_width=True)
    else:
        st.dataframe(df_2007[["country","continent","lifeExp","gdpPercap","pop"]], use_container_width=True)

# ============================================================
# 📈 ANALYTICS PAGE
# ============================================================
elif page == "📈 Analytics":

    st.title("📈 Advanced Analytics")

    if selected_country != "All":
        filtered = df[df["country"] == selected_country]

        # Life Expectancy over time
        line_fig = px.line(
            filtered,
            x="year",
            y="lifeExp",
            title=f"Life Expectancy Over Time — {selected_country}",
            markers=True,
            template="plotly_white"
        )
        st.plotly_chart(line_fig, use_container_width=True)

        # Population over time
        pop_fig = px.line(
            filtered,
            x="year",
            y="pop",
            title=f"Population Over Time — {selected_country}",
            markers=True,
            template="plotly_white"
        )
        st.plotly_chart(pop_fig, use_container_width=True)

        # GDP per Capita over time
        gdp_fig = px.line(
            filtered,
            x="year",
            y="gdpPercap",
            title=f"GDP Per Capita Over Time — {selected_country}",
            markers=True,
            template="plotly_white"
        )
        st.plotly_chart(gdp_fig, use_container_width=True)

    else:
        st.info("Select a country from the sidebar to view detailed analytics.")

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
    ✅ Country drill-down analytics  
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
