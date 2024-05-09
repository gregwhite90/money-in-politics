import dash
from dash import html

dash.register_page(__name__, path='/')

layout = html.Div([
    html.H1('Welcome to Stay Bought'),
    html.P('Stay Bought is a tool to help you understand the campaign finances of candidates for US federal office.'),
])