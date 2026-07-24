import pandas as pd
import plotly.express as px

def create_plot(
    data: list[dict],
    chart_type: str,
    x_column: str,
    y_column: str,
    title: str,
):
    df = pd.DataFrame(data)

    if chart_type == "bar":
        fig = px.bar(
            df,
            x=x_column,
            y=y_column,
            title=title
        )

    elif chart_type == "line":
        fig = px.line(
            df,
            x=x_column,
            y=y_column,
            title=title
        )

    elif chart_type == "pie":
        fig = px.pie(
            df,
            names=x_column,
            values=y_column,
            title=title
        )

    elif chart_type == "scatter":
        fig = px.scatter(
            df,
            x=x_column,
            y=y_column,
            title=title
        )

    return fig.to_json()