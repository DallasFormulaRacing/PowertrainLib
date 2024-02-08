from dash import html, dcc
import dash
import dash_bootstrap_components as dbc
from dash import callback
from dash.dependencies import Input, Output
import pandas as pd

from pages.utils.graph_utils import color_seq
import plotly.express as px

PAGE = "powertrain"
VIZ_ID = "rpm-over-time"

gc_rpm_over_time = dcc.Loading(
                    dcc.Graph(id=f"{PAGE}-{VIZ_ID}"),
                )

# callback for commits over time graph
@callback(
    Output(f"{PAGE}-{VIZ_ID}", "figure"),
    Input("time-range", "data")
)
def rpm_over_time_graph(_time_range):
    df = pd.read_csv('./ecu_data.csv', header="infer")

    
    fig = px.line(
        df,
        x="Time (sec)",
        y="RPM",
        title="RPM Over Time",
        labels={"value": "RPM", "timestamp": "Time"}
    )

    return fig
