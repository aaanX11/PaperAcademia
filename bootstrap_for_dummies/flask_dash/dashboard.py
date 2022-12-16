from flask import Blueprint
from dash import Dash
from dash.dependencies import Input, State, Output
from dash import dcc
from dash import dash_table
from dash import html

from flask_dash.db import get_engine
from dash import html
import pandas as pd
import uuid
import os
import pickle
from . import queries
import urllib
import urllib.parse


def create_dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app = Dash(
        server=server,
        routes_pathname_prefix='/dashapp/',
        external_stylesheets=[
            '/static/dist/css/styles.css',
        ]
    )

    db = get_engine()
    df = pd.read_sql_table(
        "articles",
        con=db,
        columns=['title',
                 'year'],
    )
    #df1 = pd.DataFrame(df.groupby(['year'])['year'].count())
    dash_app.layout = html.Div(
        children=[
            dcc.Graph(
                id="histogram-graph",
                figure={
                    "data": [
                        {
                            "x": df.year,
                            "name": "testtest.",
                            "type": "histogram",
                        }
                    ],
                    "layout": {
                        "title": "TEST.",
                        "height": 500,
                        "padding": 150,
                        "xaxis": {"range": [1980, 2013]},
                    },
                },
            ),
            create_data_table(df),
        ],
        id="dash-container",
    )
    init_callbacks(dash_app)
    return dash_app.server


def create_data_table(df):
    """Create Dash datatable from Pandas DataFrame."""
    table = dash_table.DataTable(
        id="database-table",
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("records"),
        sort_action="native",
        sort_mode="native",
        page_size=300,
    )
    return table


def init_callbacks(dash_app):
    pass
    # @app.callback(
    # # Callback input/output
    # ....
    # )
    # def update_graph(rows):
    #     pass


def create_cytograph(server):
    """Create a Plotly Dash dashboard."""
    dash_app = Dash(
        server=server,
        routes_pathname_prefix='/cytoscape/',
        external_stylesheets=[
            '/static/dist/css/styles.css',
        ]
    )

    dash_app.layout = html.Div(
        children=[

        ],
        id="dash-container",
    )
    init_callbacks_cytograph(dash_app)
    return dash_app.server


def init_callbacks_cytograph(dash_app):
    @dash_app.callback(
        [Output('page-content', 'children')],
        [Input('url', 'search')]
    )
    def update_cytograph(params):
        pass

        return