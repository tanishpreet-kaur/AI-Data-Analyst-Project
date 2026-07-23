import plotly.express as px

def build_chart(df, spec):

    if not spec.create_chart:
        return None

    if spec.chart_type == "bar":
        return px.bar(
            df,
            x=spec.x_column,
            y=spec.y_column,
            title=spec.title,
            labels={
                spec.x_column: spec.x_label,
                spec.y_column: spec.y_label,
            },
        )

    if spec.chart_type == "line":
        return px.line(
            df,
            x=spec.x_column,
            y=spec.y_column,
            title=spec.title,
            labels={
                spec.x_column: spec.x_label,
                spec.y_column: spec.y_label,
            },
        )

    if spec.chart_type == "pie":
        return px.pie(
            df,
            names=spec.x_column,
            values=spec.y_column,
            title=spec.title,
        )

    if spec.chart_type == "scatter":
        return px.scatter(
            df,
            x=spec.x_column,
            y=spec.y_column,
            title=spec.title,
            labels={
                spec.x_column: spec.x_label,
                spec.y_column: spec.y_label,
            },
        )

    if spec.chart_type == "histogram":
        return px.histogram(
            df,
            x=spec.x_column,
            title=spec.title,
        )

    return None