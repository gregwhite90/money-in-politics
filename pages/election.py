import dash
from dash import html, dcc, callback, Output, Input, State
from dash.exceptions import PreventUpdate
import plotly.express as px
import pandas as pd
import requests

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

# TODO: clean up the user interface
# TODO: get working for house and senate races too
# TODO: expand the dates possible
# TODO: change to adjusted disbursements for candidate committees
# TODO: add independent expenditures
# TODO: add party-coordinated expenditures
# TODO: figure out how to sort
# TODO: figure out how to be efficient with API calls. only 16-100 calls per hour
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

    query_response = tasks.fec_request('elections/', fec_api_query, per_page=10)

    # TODO: better error handling
    # TODO: should some error handling happen at the Celery task level?
    if query_response.status_code != requests.codes.ok: raise PreventUpdate
    try:
        data = query_response.json()
        df = pd.json_normalize(
            data,
            record_path='results',
        )
    except:
        raise PreventUpdate
    
    fig = px.bar(df, x="total_disbursements", y="candidate_name", color="party_full", barmode="relative")
    fig.update_layout(yaxis={'categoryorder':'total ascending'})

    return fig, {}