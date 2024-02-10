import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

from .visualizations.rpm_over_time import gc_rpm_over_time
from .visualizations.rpm_map_lambda import gc_rpm_map_lambda
from .visualizations.tps_over_time import gc_tps_over_time

dash.register_page(__name__, path="/powertrain", name="Powertrain")


layout = dbc.Container(
    [
        dmc.Header(
            "Powertrain",
            height=60,
            style={"marginBottom": "20px",
                   "fontSize": "24px",
                   "textAlign": "center",
                   "color": "white",
                   "backgroundColor": "black"},
            fixed=False,  # Set to True if you want the header to be fixed at the top
        ),
        dbc.Row(
            [
                dbc.Col(gc_rpm_over_time, width=6, lg=6),  # Using half of the container width
                dbc.Col(gc_tps_over_time, width=6, lg=6),  # Using the other half of the container width
            ],
            className="mb-4",  # Adding a bit of margin bottom for spacing
        ),
        dbc.Row(
            [
                dbc.Col(gc_rpm_map_lambda, width=12),  # takes up the full row
            ]
        ),
    ],
    fluid=True,
    style={
        'padding-top': '30px',
        'padding-right': '15px',
        'padding-bottom': '20px',
        'padding-left': '25px'
    }
)
