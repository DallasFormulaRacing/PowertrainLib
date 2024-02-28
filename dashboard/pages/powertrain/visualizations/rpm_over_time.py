from dash import html, dcc
import dash
import dash_mantine_components as dmc
from dash import callback
from dash.dependencies import Input, Output
import pandas as pd
from dash_iconify import DashIconify

import plotly.express as px

PAGE = "powertrain"
VIZ_ID = "rpm-over-time"

gc_rpm_over_time = dmc.Card(
    id="rpm-over-time",
    children=[
        dmc.CardSection(
            [
                dmc.Group(
                    children=[
                        dmc.Text("RPM vs Time", weight=500),
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
                        "This graph shows the RPM of the engine over time. "
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
    Input("time-range", "data")
)
def rpm_over_time_graph(_time_range):
    df = pd.read_csv('./ecu_data.csv', header="infer")

    fig = px.line(
        df,
        x="Time (sec)",
        y="RPM",
        labels={"value": "RPM", "timestamp": "Time"}
    )
    return fig
