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
VIZ_ID = "acceleration-vs-time"


acceleration_vs_time = dmc.Card(
  [
      dmc.Group(
          [
              html.H3(
                  "Acceleration vs Time (g)",
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
def acceleration_vs_time_graph(_time_range):
    client_instance = client()
    return client_instance.accel_vs_time_client()
