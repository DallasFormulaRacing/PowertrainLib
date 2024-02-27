from dash import html, dcc, callback
import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd

from pages.utils.graph_utils import color_seq
import plotly.express as px

PAGE = "powertrain"
VIZ_ID = "customizable_graph"

df = pd.read_csv('./ecu_data.csv', header="infer")

y_axis_options = [{'label': col, 'value': col} for col in df.columns if col != "Time (sec)"]

gc_customizable_graph = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H3(
                    id="graph-title",
                    className="card-title",
                    style={"textAlign": "center"},
                ),
                # dropdown
                dcc.Dropdown(
                    id="y-axis-dropdown",
                    options=y_axis_options,
                    value="RPM",
                    style={"width": "50%"}
                ),
                dcc.Loading(
                    dcc.Graph(id=f"{PAGE}-{VIZ_ID}"),
                ),
            ]
        ),
    ],
)

# callback to dynamically change y-axis
@callback(
    [Output("graph-title", "children"),
     Output(f"{PAGE}-{VIZ_ID}", "figure")],
    [Input("time-range", "data"),
     Input("y-axis-dropdown", "value")]
)
def customizable_graph(_time_range, y_axis_variable):
    graph_title = f"{y_axis_variable} vs Time (sec)"

    fig = px.line(
        df,
        x="Time (sec)",
        y=y_axis_variable,
        labels={"value": y_axis_variable, "timestamp": "Time"}
    )
    fig.update_layout(title=graph_title)
    return graph_title, fig