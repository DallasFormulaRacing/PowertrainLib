from io import StringIO
from dash import html, dcc
import dash
import dash_mantine_components as dmc
from dash import callback
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
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
                        dmc.Text("TPS vs Time", weight=500),
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
                        "This graph shows the TPS of the engine over time. "
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
    Input("ljm-data", "data")
)
def tps_over_time_graph(data):
    df = pd.read_json(data, orient='split', encoding='unicode_escape')
    print("read df: ", df)
    if df.empty:
        return px.line(title="No Data", labels={"value": "TPS", "timestamp": "Time"})
    fig = px.line(
        df,
        x="timestamp",
        y=["Front Left", "Front Right", "Rear Left", "Rear Right"],
    )
    return fig
