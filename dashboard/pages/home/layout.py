import dash
import dash_mantine_components as dbc

dash.register_page(__name__, path="/", name="Home", exact=True)

layout = dbc.Container([
    dbc.Header("DFR Dashboard", height=0, className="text-4xl text-center")
])
