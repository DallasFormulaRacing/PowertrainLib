import dash
import dash_mantine_components as dmc

dash.register_page(__name__, path="/", name="Home", exact=True)

layout = dmc.Container([
    dmc.Header("DFR Dashboard", height=0, className="text-4xl text-center")
])
