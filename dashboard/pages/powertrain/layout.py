import dash 
from dash import html, dcc
import dash_bootstrap_components as dbc

from .visualizations.rpm_over_time import gc_rpm_over_time
from .visualizations.rpm_map_lambda import gc_rpm_map_lambda

dash.register_page(__name__, path="/powertrain", name="Powertrain")

layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(gc_rpm_over_time, width=12)
            ],
            align="center",
            style={"marginTop": ".5%"}
        ),
        dbc.Row(
            [
                dbc.Col(gc_rpm_map_lambda, width=6)
            ],
            align="center",
            style={"marginTop": ".5%"}
        ),
    ],
    fluid=True
)
