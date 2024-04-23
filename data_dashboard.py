from dash import Dash, dcc, html, Input, Output
import plotly.express as px


import pandas as pd

df = pd.DataFrame()

print(df.head())
app = Dash(__name__)


app.layout = html.Div([
    html.H4('ECU Data'),
    dcc.Graph(id="line-charts-x-graph"),
    dcc.Dropdown(
        id="line-charts-x-checklist",
        options=list(df.head()),
        value=["RPM"],
        multi=True
    ),
    dcc.Dropdown(
        id="line-charts-x-dropdown",
        options=list(df.head()),
        value=["timestamp"]
    )
])


@app.callback(
    Output("line-charts-x-graph", "figure"), 
    Input("line-charts-x-checklist", "value"),
    Input("line-charts-x-dropdown", "value"))
def update_line_chart(header_values, x_axis):
    fig = px.line(df, 
        x=x_axis, y=header_values)
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
