import dash
import dash_mantine_components as dmc
from dash import dcc

from .components import update_title # pylint: disable=unused-import
# navbar for top of screen
navbar = dmc.Group(
    [
        dmc.Anchor(page["name"], href=page["path"], className="nav-link")
        for page in dash.page_registry.values()
    ],
    className="nav"
)

layout = dmc.MantineProvider(
    theme={
        "fontFamily": "'Inter', sans-serif",
        "colorScheme": "dark",
        "primaryColor": "red",
        "components": {
            "Button": {"styles": {"root": {"fontWeight": 400}}},
            "Alert": {"styles": {"title": {"fontWeight": 500}}},
            "AvatarGroup": {"styles": {"truncated": {"fontWeight": 500}}},
            # make backgrounds #111111
            "Navbar": {"styles": {"root": {"backgroundColor": "#111111"}}},
            "Grid": {"styles": {"root": {"backgroundColor": "#111111"}}},
        },
    },
    inherit=True,
    withGlobalStyles=True,
    withNormalizeCSS=True,
    children=[
        # components to store data from queries
        dcc.Store(id="time-range", storage_type="session", data=[]),
        dcc.Store(id="user-group-loading-signal", data="", storage_type="memory"),
        dcc.Store(id='ecu-data', data=[]),
        dcc.Store(id="linpot-data", data=[]),
        dcc.Store(id="xl-data", data=[]),
        dcc.Location(id="url"),
        navbar,
        dmc.Text(
            "Home",
            id="title",
            className="page-title",
        ),
        # dcc.Input(id='testing-day', type='text', placeholder='Enter run ID'),
        dash.page_container
    ],
)
