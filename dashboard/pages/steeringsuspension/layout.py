import dash
from dash import html, dcc
import dash_mantine_components as dmc
from ..utils.analytics_page import make_components
from .visualizations.wheel_load import wheel_load_over_time
#from .visualizations.accel import accel_over_time

dash.register_page(__name__, path="/suspensionsteering", name="SuspensionSteering")

graphs = {
    "SuspensionSteering": {
        "Wheel Load over Time": wheel_load_over_time
        #"Acceleration vs Time": accel_over_time
    }
}

layout = make_components(graphs)
