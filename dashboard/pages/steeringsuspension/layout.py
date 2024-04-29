import dash
from dash import html, dcc
import dash_mantine_components as dmc
from utils.analytics_page import make_components
from .visualizations.wheel_load import wheel_load_over_time
from .visualizations.pitch_roll import pitch_roll_over_time
from .visualizations.linpot import linpot_over_time
from .visualizations.damper_force import damper_force_over_time
from .visualizations.damper_velocity import damper_velocity_over_time
from .visualizations.accel_vs_time import acceleration_vs_time

dash.register_page(__name__, path="/suspensionsteering", name="SuspensionSteering")

graphs = {
    "SuspensionSteering": {
        "Wheel Load over Time": wheel_load_over_time,
        "Linpot over Time": linpot_over_time,
        #"Pitch and Roll over Time": pitch_roll_over_time,
        "Damper Force over Time": damper_force_over_time,
        "Damper Velocity over Time": damper_velocity_over_time,
        #"Acceleration vs Time": acceleration_vs_time
    }
}

layout = make_components(graphs)
