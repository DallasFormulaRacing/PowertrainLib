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
VIZ_ID = "damper-velocity-vs-time"

damper_velocity_over_time = dmc.Card(
    [
        dmc.Group(
            [
                html.H3(
                    "Damper Velocity vs Time",
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
def damper_velocity_over_time_graph(data):
    df = pd.read_json(data, orient='split')
    print("read df: ", df)
    if df.empty:
        return px.line(title="No Data", labels={"value": "damper velocity", "timestamp": "Time"})
    client_instance = client(df)
    return client_instance.damper_velocity_vs_time_client()
