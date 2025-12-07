import streamlit as st
import plotly.express as px

def show(df):
    st.title("📈 Advanced Analytics")

    selected_country = st.sidebar.selectbox(
        "🔍 Select Country (Drill-down)",
        ["All"] + list(df["country"].unique())
    )

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
