import powertrain_dash_boilerplate
from dash import Dash, callback, html, Input, Output, dcc
import pandas as pd

app = Dash(__name__)
data = pd.read_csv("ecu_data.csv")

# Boilerplate default layout
# app.layout = html.Div([
#     powertrain_dash_boilerplate.Powertrain(
#         id='input',
#         value='my-value',
#         label='my-label'
#     ),
#     html.Div(id='output')
# ])

app.layout = html.Div(
    children=[
        html.Div([
            dcc.Graph(
                id=f"graph-{col}",
                figure={
                    "data": [
                        {
                            "x": data.index,
                            "y": data[col],
                            "type": "lines",
                        },
                    ],
                    "layout": {"title": col}
                },
            ),
            html.Hr()
        ]) for i, col in enumerate(data.columns) if i > 0
    ]
)

@callback(Output('output', 'children'), Input('input', 'value'))
def display_output(value):
    return 'You have entered {}'.format(value)


if __name__ == '__main__':
    app.run_server(debug=True)
