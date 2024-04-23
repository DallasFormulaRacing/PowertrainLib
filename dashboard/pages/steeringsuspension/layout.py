import dash
from dash import html, dcc
import dash_mantine_components as dmc
from ..utils.analytics_page import make_components
from .visualizations.wheel_load import wheel_load_over_time
from .visualizations.pitch_roll import pitch_roll_over_time
from .visualizations.linpot import linpot_over_time

dash.register_page(__name__, path="/suspensionsteering", name="SuspensionSteering")

graphs = {
    "SuspensionSteering": {
        "Wheel Load over Time": wheel_load_over_time,
        "Linpot over Time": linpot_over_time,
        "Pitch and Roll over Time": pitch_roll_over_time
    }
}

layout = make_components(graphs)
