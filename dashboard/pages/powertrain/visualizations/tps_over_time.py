from io import StringIO

import dash
import dash_mantine_components as dmc
import pandas as pd
import plotly.express as px
from dash import callback, dcc, html
from dash.dependencies import Input, Output
from dash_iconify import DashIconify

PAGE = "powertrain"
VIZ_ID = "tps-over-time"

gc_tps_over_time = dmc.Card(
    id="rpm-over-time",
    children=[
        dmc.CardSection(
            [
                dmc.Group(
                    children=[
                        dmc.Text("Linpots vs Time", weight=500),
                        dmc.ActionIcon(
                            DashIconify(icon="carbon:overflow-menu-horizontal"),
                            color="gray",
                            variant="transparent",
                        ),
                    ],
                    position="apart",
                ),
                dmc.Text(
                    children=[
                        "Data from the latest testing session"
                    ],
                    mt="sm",
                    color="dimmed",
                    size="sm",
                ),
            ],
            inheritPadding=True,
            py="xs",
            withBorder=True,
        ),
        dmc.CardSection(
            dcc.Loading(
                dcc.Graph(id=f"{PAGE}-{VIZ_ID}"),
            ),
        ),
    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    p="xs",
    m="xs",
    bg="black",
    style={"width": "100%"},
)


# callback for commits over time graph
@callback(
    Output(f"{PAGE}-{VIZ_ID}", "figure"),
    Input("linpot-data", "data")
)
def tps_over_time_graph(data):
    df = pd.read_json(data, orient='split')
    print("read df: ", df)
    if df.empty:
        return px.line(title="No Data", labels={"value": "TPS", "timestamp": "Time"})
    fig = px.line(
        df,
        x="timestamp",
        y=["Front Left", "Front Right", "Rear Left", "Rear Right"],
    )
    return fig
