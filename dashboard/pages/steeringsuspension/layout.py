import dash
from dash import html, dcc
import dash_mantine_components as dmc
from ..utils.analytics_page import make_components
from .visualizations.wheel_load import wheel_load_over_time

dash.register_page(__name__, path="/suspensionsteering", name="SuspensionSteering")

graphs = {
    "SuspensionSteering": {
        "Wheel Load over Time": wheel_load_over_time,
        #"title of graph" : name_of_card
    }
}

layout = make_components(graphs)
