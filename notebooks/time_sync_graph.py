import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.express as px

# SAMPLE TIME SYNC GRAPH

df = pd.read_csv('ecu_data.csv')  # file path to data

app = dash.Dash(__name__)

# layout
app.layout = html.Div([
    html.H1("ECU Data"),
    html.Div([
        html.Label("Graph 1 Y-axis:"),
        dcc.Dropdown(
            id='graph1-y-axis',
            options=[{'label': col, 'value': col} for col in df.columns if col != 'Time (sec)'],
            value=df.columns[1],
            style={'width': '200px'}
        ),
        dcc.Graph(id='graph1', config={'displayModeBar': True}, style={'height': '400px'})
    ]),
    html.Div([
        html.Label("Graph 2 Y-axis:"),
        dcc.Dropdown(
            id='graph2-y-axis',
            options=[{'label': col, 'value': col} for col in df.columns if col != 'Time (sec)'],
            value=df.columns[2],
            style={'width': '200px'}
        ),
        dcc.Graph(id='graph2', config={'displayModeBar': True}, style={'height': '400px'})
    ]),
    dcc.Store(id='x-axis-range')
])

# callback to update x-axis range
@app.callback(
    Output('x-axis-range', 'data'),
    [Input('graph1', 'relayoutData'),
     Input('graph2', 'relayoutData')]
)
def update_x_axis_range(relayoutData1, relayoutData2):
    if relayoutData1 and 'xaxis.range[0]' in relayoutData1:
        return {'x_range': [relayoutData1['xaxis.range[0]'], relayoutData1['xaxis.range[1]']]}
    elif relayoutData2 and 'xaxis.range[0]' in relayoutData2:
        return {'x_range': [relayoutData2['xaxis.range[0]'], relayoutData2['xaxis.range[1]']]}
    else:
        return {'x_range': None}

# callback to update graph 1
@app.callback(
    Output('graph1', 'figure'),
    [Input('graph1-y-axis', 'value'),
     Input('x-axis-range', 'data')]
)
def update_graph1(selected_y_axis, x_range):
    title = f"{selected_y_axis} x Time (sec)"
    fig = px.line(df, x='Time (sec)', y=selected_y_axis)
    fig.update_layout(title=title, xaxis_title="Time (sec)", yaxis_title=selected_y_axis, xaxis=dict(range=x_range['x_range']))
    return fig

# callback to update graph 2
@app.callback(
    Output('graph2', 'figure'),
    [Input('graph2-y-axis', 'value'),
     Input('x-axis-range', 'data')]
)
def update_graph2(selected_y_axis, x_range):
    title = f"{selected_y_axis} x Time (sec)"
    fig = px.line(df, x='Time (sec)', y=selected_y_axis)
    fig.update_layout(title=title, xaxis_title="Time (sec)", yaxis_title=selected_y_axis, xaxis=dict(range=x_range['x_range']))
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
