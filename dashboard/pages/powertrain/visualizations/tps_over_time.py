from dash import html, dcc
import dash
import dash_mantine_components as dmc
from dash import callback
from dash.dependencies import Input, Output
import pandas as pd

from pages.utils.graph_utils import color_seq
import plotly.express as px

PAGE = "powertrain"
VIZ_ID = "tps-over-time"

gc_tps_over_time = dmc.Card(
    [
        dmc.Group(
            [
                html.H3(
                    "TPS vs timestamp",
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
def tps_over_time_graph(_time_range):
    df = pd.read_csv('./ecu_data.csv', header="infer")

    fig = px.line(
        df,
        x="timestamp",
        y="TPS (%)",
        labels={"value": "TPS", "timestamp": "Time"}
    )
    return fig
