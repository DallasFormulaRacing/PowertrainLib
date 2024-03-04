import dash
from dash import html, dcc
import dash_mantine_components as dmc
from ..utils.analytics_page import make_components
from .visualizations.rpm_over_time import gc_rpm_over_time
from .visualizations.rpm_map_lambda import gc_rpm_map_lambda
from .visualizations.tps_over_time import gc_tps_over_time
from .visualizations.customizable_ecu_data import gc_customizable_graph

dash.register_page(__name__, path="/powertrain", name="Powertrain")

graphs = {
    "Engine": {
        "RPM Over Time": gc_rpm_over_time,
        "RPM vs MAP vs Lambda/AFR LTF": gc_rpm_map_lambda,
        "Customizable ECU Data": gc_customizable_graph
    }
}

layout = make_components(graphs)
