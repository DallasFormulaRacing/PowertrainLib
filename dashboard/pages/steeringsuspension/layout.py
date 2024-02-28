import dash
import dash_mantine_components as dmc

dash.register_page(__name__, path="/suspension", name="Suspension", exact=True)

layout = dmc.Container([
    dmc.Header("Suspension", height=0, className="text-4xl text-center")
])
