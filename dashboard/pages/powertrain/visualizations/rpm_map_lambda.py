from dash import html, dcc
import dash
import dash_bootstrap_components as dbc
from dash import callback
from dash.dependencies import Input, Output
import pandas as pd

from pages.utils.graph_utils import color_seq
import plotly.express as px

PAGE = "powertrain"
VIZ_ID = "rpm-map-lambda"

gc_rpm_map_lambda = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H3(
                    "RPM vs MAP vs Lambda/AFR LTF (%)",
                    className="card-title",
                    style={"textAlign": "center", "marginTop": "1%"},
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
def rpm_lambda_graph(_time_range):
    df = pd.read_csv('./ecu_data.csv', header="infer")

    fig = px.line_3d(df, x='RPM', y='MAP (psi)', z='Lambda/AFR LTF (%)')
    return fig
