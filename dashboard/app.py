"""
    README -- Organization of Callback Functions

    In an effort to compartmentalize our development where possible, all callbacks directly relating
    to pages in our application are in their own files.

    For instance, this file contains the layout logic for the index page of our app-
    this page serves all other paths by providing the searchbar, page routing faculties,
    and data storage objects that the other pages in our app use.

    Having laid out the HTML-like organization of this page, we write the callbacks for this page in
    the neighbor 'app_callbacks.py' file.
"""
import os
import sys
import logging
import dash
import plotly.io as plt_io
import dash_bootstrap_components as dbc
import dash_bootstrap_templates as dbt
logging.basicConfig(format="%(asctime)s %(levelname)-8s %(message)s", level=logging.INFO)


"""IMPORT AFTER GLOBAL VARIABLES SET"""
import pages.index.components as index_components

"""SET STYLING FOR APPLICATION"""
dbt.load_figure_template(["cyborg"])

# stylesheet with the .dbc class, this is a complement to the dash bootstrap templates, credit AnnMarieW
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

# making custom plotly template with custom colors on top of the slate design template
# plt_io.templates["custom_dark"] = plt_io.templates["cyborg"]

plt_io.templates.default = "plotly_dark"

"""CREATE APPLICATION"""
app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.CYBORG, dbc_css, dbc.icons.FONT_AWESOME],
    suppress_callback_exceptions=True,
    
    # Tailwind CSS CDN Loading
    external_scripts=[{"src": "https://cdn.tailwindcss.com"}]
)

"""DASH PAGES LAYOUT"""
# layout of the app stored in the app_layout file, must be imported after the app is initiated
from pages.index.layout import layout

app.layout = layout

"""DASH STARTUP PARAMETERS"""

if os.getenv("DASH_DEBUG", "False") == "True":
    app.enable_dev_tools(dev_tools_ui=True, dev_tools_hot_reload=False)

if __name__ == "__main__":
    app.run_server(debug=True)
    