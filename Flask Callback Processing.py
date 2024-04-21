import dash
from dash import html, dcc, Input, Output
import pandas as pd
import pymongo

# Initialize Dash app
app = dash.Dash(__name__)

# Connect to MongoDB 
client = pymongo.MongoClient('database_url')
db = client['database_name']
collection = db['collection_name']

# Callback to load data for run ID and session ID
@app.callback(
    Output('testing-data', 'data'),
    Input('testing-day', 'value'),
    Input('session-id', 'value')
)
def load_data(run_id, session_id):
    # Query MongoDB for data with the given run ID and session ID
    mongo_data = list(collection.find({'run_id': run_id, 'session_id': session_id}))
    
    # Convert MongoDB data to DataFrame
    df = pd.DataFrame(mongo_data)
    
    # Convert DataFrame to JSON and return
    return df.to_json(date_format='iso', orient='split')

# Define callback to update graph using loaded data
@callback(Output("title", "children"), Input("url", "pathname"))
def update_title(pathname) -> str:
    """Updates the title of the page based on the current pathname.

    Args:
        pathname (str): The current pathname of the page.

    Returns:
        str: The title of the page.
    """
    if pathname == "/":
        return "Home"
    else:
        for page in dash.page_registry.values():
            if page["path"] == pathname:
                return page["name"]
    return "404 - Not Found"

# Layout
layout = dmc.MantineProvider(
    theme={
        "fontFamily": "'Inter', sans-serif",
        "colorScheme": "dark",
        "primaryColor": "red",
        "components": {
            "Button": {"styles": {"root": {"fontWeight": 400}}},
            "Alert": {"styles": {"title": {"fontWeight": 500}}},
            "AvatarGroup": {"styles": {"truncated": {"fontWeight": 500}}},
            # make backgrounds #111111
            "Navbar": {"styles": {"root": {"backgroundColor": "#111111"}}},
            "Grid": {"styles": {"root": {"backgroundColor": "#111111"}}},
        },
    },
    inherit=True,
    withGlobalStyles=True,
    withNormalizeCSS=True,
    children=[
        dcc.Input(id='testing-day', type='text', placeholder='Enter run ID'),
        dcc.Input(id='session-id', type='text', placeholder='Enter session ID'),  # New input for session ID
        dcc.Store(id='testing-data', data=None),
        dcc.Graph(id='t')
    ],
)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
