import dash
import dash_mantine_components as dbc

dash.register_page(__name__, path="/suspension", name="Suspension", exact=True)

layout = dbc.Container([
    dbc.Header("Suspension", height=0, className="text-4xl text-center")
])
