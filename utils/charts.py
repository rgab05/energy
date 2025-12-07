import plotly.express as px

def create_map(df, country):
    if country != "All":
        map_df = df[df["country"] == country]
        fig = px.scatter_geo(
            map_df, locations="iso_alpha", color="lifeExp", hover_name="country",
            size="pop", animation_frame="year", projection="natural earth", title=f"Life Expectancy — {country}",
            size_max=40
        )
    else:
        fig = px.scatter_geo(
            df, locations="iso_alpha", color="lifeExp", hover_name="country",
            size="pop", animation_frame="year", projection="natural earth",
            title="Life Expectancy by Country (1952–2007)", size_max=40
        )
    return fig

def create_bar_chart(df, country):
    df_2007 = df[df["year"] == 2007]
    if country != "All":
        df_bar = df_2007[df_2007["country"] == country]
        x_col = "country"
        color_col = "country"
    else:
        df_bar = df_2007
        x_col = "continent"
        color_col = "continent"

    fig = px.bar(df_bar, x=x_col, y="lifeExp", color=color_col,
                 title="Life Expectancy (2007)", template="plotly_white")
    return fig
