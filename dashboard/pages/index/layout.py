import dash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import dcc, html

# navbar for top of screen
navbar = dbc.Nav(
            [
                dbc.NavLink(
                    html.Div(page["name"], className="ms-2"),
                    href=page["path"],
                    active="exact",
                )
                for page in dash.page_registry.values()
            ],
            vertical=False,
            pills=False,
            className="bg-transparent bg-opacity-50 bg-blur-xl justify-content-center gap-4 w-full p-2 z-25",
        )

layout = dbc.Container(
    [
        # components to store data from queries
        dcc.Store(id="time-range", storage_type="session", data=[]),
        dcc.Store(id="user-group-loading-signal", data="", storage_type="memory"),
        dcc.Location(id="url"),
        navbar,
        dbc.Row(
            [
                dash.page_container,
            ],
            justify="start",
        )
    ],
    fluid=True,
    className="dbc",
)
