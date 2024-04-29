from dash import html, dcc
import dash
import dash_mantine_components as dmc
from dash import callback
from dash.dependencies import Input, Output
import pandas as pd
from ..SuspensionSteeringLib2.client import client
import plotly.express as px
import timeit

PAGE = "SuspensionSteering"
VIZ_ID = "wheel-load-over-time"

wheel_load_over_time = dmc.Card(
    [
        dmc.Group(
            [
                html.H3(
                    "Wheel Load vs Time (lbf)",
                    className="card-title",
                    style={"textAlign": "center"},
                ),
                dcc.Loading(
                    dcc.Graph(id=f"{PAGE}-{VIZ_ID}"),
                ),
            ]
        ),
    ],
)


# callback for commits over time graph
@callback(
    Output(f"{PAGE}-{VIZ_ID}", "figure"),
    Input("linpot-data", "data")
)
def wheel_load_over_time_graph(data):
    df = pd.read_json(data, orient='split')
    print("read df: ", df)
    if df.empty:
        return px.line(title="No Data", labels={"value": "Wheel Load", "timestamp": "Time"})
    clientInstance = client(df)
    return clientInstance.wheel_load_client()
