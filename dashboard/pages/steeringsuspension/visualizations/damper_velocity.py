from dash import html, dcc
import dash
import dash_mantine_components as dmc
from dash import callback
from dash.dependencies import Input, Output
import pandas as pd
from ..SuspensionSteeringLib.client import client
from pages.utils.graph_utils import color_seq
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
    Input("time-range", "data")
)
def damper_velocity_over_time_graph(_time_range):
    client_instance = client()
    client_instance.damper_velocity_vs_time_client()

    return client_instance.damper_velocity_vs_time_client()
