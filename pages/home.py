import streamlit as st
from utils.charts import create_map, create_bar_chart

def show(df):
    st.title("Global Data Dashboard")

    selected_country = st.sidebar.selectbox(
        "🔍 Select Country (Drill-down)",
        ["All"] + list(df["country"].unique())
    )

    # KPIs
    col1, col2, col3 = st.columns(3)
    if selected_country != "All":
        df_country = df[df["country"] == selected_country]
        col1.metric("Country", selected_country)
        col2.metric("Max Life Expectancy", round(df_country["lifeExp"].max(), 1))
        col3.metric("Population (2007)", int(df_country[df_country["year"]==2007]["pop"].values[0]))
    else:
        col1.metric("Total Countries", df["country"].nunique())
        col2.metric("Total Records", len(df))
        col3.metric("Max Life Expectancy", round(df["lifeExp"].max(), 1))

    st.divider()

    # MAP + BAR CHART
    left, right = st.columns([1.3, 1])
    with left:
        st.subheader("Global Life Expectancy Map")
        st.plotly_chart(create_map(df, selected_country), use_container_width=True)
    with right:
        st.subheader("Life Expectancy by Continent / Country")
        st.plotly_chart(create_bar_chart(df, selected_country), use_container_width=True)

    st.divider()
    st.subheader("📄 Country Data Table (2007)")
    df_2007 = df[df["year"] == 2007]
    if selected_country != "All":
        st.dataframe(df_2007[df_2007["country"] == selected_country], use_container_width=True)
    else:
        st.dataframe(df_2007, use_container_width=True)
