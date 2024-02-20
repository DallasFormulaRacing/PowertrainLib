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

# Callback to load data for run ID
@app.callback(
    Output('testing-data', 'data'),
    Input('testing-day', 'value')
)
def load_data(run_id):
    # Query MongoDB for data with the given run ID
    mongo_data = list(collection.find({'run_id': run_id}))
    
    # Convert MongoDB data to DataFrame
    df = pd.DataFrame(mongo_data)
    
    # Convert DataFrame to JSON and return
    return df.to_json(date_format='iso', orient='split')

# Define callback to update graph using loaded data
@app.callback(
    Output('t', 'figure'),
    Input('testing-data', 'data')
)
def update_graph_1(jsonified_cleaned_data):
    # Convert JSON data to DataFrame
    df = pd.read_json(jsonified_cleaned_data, orient='split')
    
    # Perform data processing/ visualization 
    fig = px.scatter(df, x='time', y='rpm', title='RPM vs. Time for Track Run',
                 labels={'time': 'Time (s)', 'rpm': 'RPM'})
    
    return fig

# Layout
app.layout = html.Div([
    dcc.Input(id='testing-day', type='text', placeholder='Enter run ID'),
    dcc.Store(id='testing-data', data=None),
    dcc.Graph(id='t')
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
