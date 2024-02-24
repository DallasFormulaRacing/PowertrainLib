import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from datetime import date

# Create a Dash application
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the navigation bar layout
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/", style={'color': '#FFFFFF'})),
        dbc.NavItem(dbc.NavLink("Powertrain", href="/powertrain", style={'color': '#06A0DC'})),
        dbc.NavItem(dbc.NavLink("Aero", href="/aero", style={'color': '#A04799'})),
        dbc.NavItem(dbc.NavLink("Steering", href="/steering", style={'color': '#FDC2CE'})),
    ],
    brand="Dallas Formula Racing",
    brand_href="/",
    color="dark",
    dark=True,
    style={'backgroundColor': '#000000'},
)

# Define the date picker range just below the navbar
date_picker_range = html.Div(
    dcc.DatePickerRange(
        id='date-picker-range',
        start_date=date(2023, 1, 20),
        end_date=date(2023, 2, 9),
        display_format='MMM D, YYYY',
        style={'color': '#000000'}
    ),
    style={'padding': '10px', 'backgroundColor': '#000000', 'textAlign': 'center'}
)

# Define the app layout with a black background color
app.layout = html.Div([
    navbar,
    date_picker_range,  # This will place the date range picker just below the navbar
    # The rest of your page content would go here
    html.Div([], style={'backgroundColor': '#000000', 'height': '100vh'})
], style={'backgroundColor': '#000000', 'margin': '0', 'padding': '0', 'height': '100vh'})

# Run the application
if __name__ == "__main__":
    app.run_server(debug=True)
