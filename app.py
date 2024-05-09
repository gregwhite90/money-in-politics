import dash
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc

# TODO: re-style navbar
# TODO: change welcome message
# TODO: add about/methodology page
# TODO: add more data views

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.FLATLY])

server = app.server

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink(page['name'], href=page['relative_path']))
        for page in filter(lambda page: page['relative_path'] != '/', dash.page_registry.values())
    ],
    brand="Stay Bought",
    brand_href="/",
    class_name='mb-5',
    sticky='top',
)

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        navbar,
        dash.page_container,
    ]
)

if __name__ == '__main__':
    app.run(debug=True)