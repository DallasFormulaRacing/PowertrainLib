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

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s", level=logging.INFO
)


"""IMPORT AFTER GLOBAL VARIABLES SET"""
import pages.index.components as index_components

plt_io.templates.default = "plotly_dark"
custom_template = plt_io.templates["plotly_dark"]

custom_template.layout.colorway = [
    "#e1382d",
    "#ff9e00",
    "#f0e100",
    "#00e1ff",
    "#00ff8e",
    "#ff00f7",
    "#ff0077",
    "#ff00d2",
    "#ff00a6",
    "#ff0055",
]
# background color
custom_template.layout.paper_bgcolor = "black"
custom_template.layout.plot_bgcolor = "black"
"""CREATE APPLICATION"""
app = dash.Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    assets_folder="assets"
    # Tailwind CSS CDN Loading
    # external_scripts=[{"src": "https://cdn.tailwindcss.com"}],
)

# Hack needed for gunicorn to detect server
server = app.server

"""DASH PAGES LAYOUT"""
# layout of the app stored in the app_layout file, must be imported after the app is initiated for setup
from pages.index.layout import layout # pylint: disable=wrong-import-position

app.layout = layout

"""DASH STARTUP PARAMETERS"""

if os.getenv("DASH_DEBUG", "False") == "True":
    app.enable_dev_tools(dev_tools_ui=True, dev_tools_hot_reload=False)

if __name__ == "__main__":
    app.run_server(debug=True)
