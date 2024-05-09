import dash
from dash import html, dcc, callback, Output, Input, State
from dash.exceptions import PreventUpdate
import plotly.express as px
import pandas as pd

import tasks

dash.register_page(__name__)

layout = html.Div(children=[
    dcc.Dropdown(['president'], 'president', id='office'),
    dcc.Dropdown(['2024', '2020', '2016'], '2024', id='cycle'),
    html.Button(n_clicks=0, children='Update', id='update'),

    dcc.Loading(
        id='loading-graph', 
        children=[
            dcc.Graph(
                id='graph',
                style={'display': 'none'},
            )
        ],
        type='default',
    )
])

@callback(
    Output('graph', 'figure'),
    Output('graph', 'style'),
    Input('update', 'n_clicks'),
    State('office', 'value'),
    State('cycle', 'value'),
)
def update_graph(n_clicks, office, cycle):
    if n_clicks == 0: raise PreventUpdate
    fec_api_query = {
        'sort': '-total_disbursements',
        'office': office,
        'election_full': 'true',
        'cycle': cycle,
    }

    # query_response = tasks.fec_request('elections/', fec_api_query, per_page=10)

    # TODO: error handling

    df = pd.DataFrame({
        "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
        "Amount": [4, 1, 2, 2, 4, 5],
        "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"],
    })

    fig = px.bar(df, x="Amount", y="Fruit", color="City", barmode="group")

    return fig, {}