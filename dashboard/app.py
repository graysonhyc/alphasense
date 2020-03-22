# Import required libraries
import os
import pickle
import copy
import datetime as dt
import math

import requests
import pandas as pd
from flask import Flask
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

# Multi-dropdown options
from controls import COUNTIES, WELL_STATUSES, WELL_TYPES, WELL_COLORS

app = dash.Dash(__name__)
server = app.server

df_prediction = pd.read_csv('data/master_cleaned.csv')
df_prediction['date_posted'] = pd.to_datetime(df_prediction['date_posted'])
df_history = pd.read_csv('data/stock_history.csv')
df_history['dates'] = pd.to_datetime(df_history['dates'])
df_history = df_history.sort_values('dates')

# Create controls
company_options = [{'label': str(company), 'value': str(company)}
                  for company in df_prediction['company'].unique()]

issuer_options = [{'label': str(issuer), 'value': str(issuer)}
                  for issuer in df_prediction['issuer'].unique()]


layout = dict(
    autosize=True,
    margin=dict(
        l=30,
        r=30,
        b=20,
        t=40
    ),
    hovermode="closest",
    #plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    legend=dict(font=dict(size=10), orientation='h'),
)

# Create app layout
app.layout = html.Div(
    [
        dcc.Store(id='aggregate_data'),
        html.Div(
            [
                html.Div(
                    [
                        html.H2(
                            'AlphaSense',

                        ),
                        html.H4(
                            'Issuer Credibility Overview',
                        )
                    ],
                    className='eight columns'
                ),
            ],
            id="header",
            className='row',
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.P(
                            'Filter by stock:',
                            className="control_label"
                        ),
                        dcc.Dropdown(
                            id='company',
                            options=company_options,
                            multi=False,
                            value=None,
                            className="dcc_control"
                        ),
                        html.P(
                            'Filter by issuer:',
                            className="control_label"
                        ),
                        dcc.Dropdown(
                            id='issuer',
                            options=issuer_options,
                            multi=True,
                            value=None,
                            className="dcc_control"
                        ),
                    ],
                    className="pretty_container four columns"
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Graph(
                                    id='main_graph',
                                )
                            ],
                            id="countGraphContainer",
                            className="pretty_container"
                        )
                    ],
                    id="rightCol",
                    className="eight columns"
                )
            ],
            className="row"
        ),
    ],
    id="mainContainer",
    style={
        "display": "flex",
        "flex-direction": "column"
    }
)


# Helper functions
def filter_dataframe(df_prediction, df_history, company, issuer):
    dff_prediction = df_prediction[df_prediction['company'].isin([company])
             & df_prediction['issuer'].isin(issuer)
             #& (df['date_posted'] > dt.datetime(year_slider[0], 1, 1))
             #& (df['date_posted'] < dt.datetime(year_slider[1], 1, 1))
             ]
    dff_history = df_history[df_history['company'].isin([company])]
    
    return dff_prediction, dff_history


# Selectors -> graph
@app.callback(Output('main_graph', 'figure'),
             [Input('company', 'value'),
               Input('issuer', 'value')])
def main_graph(company, issuer):

    layout_main = copy.deepcopy(layout)
    layout_main['title'] = 'Overview'

    dff_prediction, dff_history = filter_dataframe(df_prediction, df_history, company, issuer)

    figure = px.scatter(dff_prediction,
                        x='date_posted',
                        y='predicted',
                        color='issuer')

    figure = go.Figure(layout=go.Layout(layout_main))
    figure.add_trace(go.Scatter(x=dff_history.dates,
                                y=dff_history.close,
                                mode='lines',
                                name=company))

    for i in issuer:
        dff_slice = dff_prediction[dff_prediction['issuer']==i]
        figure.add_trace(go.Scatter(x=dff_slice.date_posted,
                                y=dff_slice.predicted,
                                mode='markers',
                                name=i))

    return figure


# Main
if __name__ == '__main__':
    app.server.run(debug=True, threaded=True)