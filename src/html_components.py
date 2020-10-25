# -*- coding: utf-8 -*-
"""
Created on Sat Sep 19 15:30:16 2020

@author: Krishna Kinger
"""
import base64
import dash
import dash_html_components as html
import dash_core_components as dcc
from utils import listDirectories
from neo4j_graph import neograph

image_filename = '../static/logo.png' # replace with your own image
encoded_logo = base64.b64encode(open(image_filename, 'rb').read())
encoded_tukl = base64.b64encode(open('../static/tukl.png', 'rb').read())
encoded_via = base64.b64encode(open('../static/via.jpeg', 'rb').read())

def main_banner():
    return html.Div([
                 html.Img(src='data:image/png;base64,{}'.format(encoded_logo.decode()), style={'margin': -20}),
                 html.Img(src='data:image/png;base64,{}'.format(encoded_via.decode()), width=150, height=70, style={'margin': -20, 'float': 'right', 'padding':50}),
                 html.Img(src='data:image/png;base64,{}'.format(encoded_tukl.decode()), width=335, height=70, style={'margin': -20, 'float': 'right', 'padding':50})
            ], style={'backgroundColor': 'rgb(1, 91, 176)', 'height': '60px', 'margin': -10})

def dropdown_menu():
    dirs = listDirectories('../data')
    options = [{'label':key, 'value':value} for key, value in dirs.items()]
    return dcc.Dropdown(
                    id='graphs',
                    options=options,
                    value=list(dirs.values())[0],
                    style={'width':300, 'display':'inline-block', 'height':'30px'}
                    )
    
def dropdown_banner():
    return html.Div([
            html.Div([
                    html.H2('Select Network', 
                         style={'padding-left':50, 'padding-top':5, 'padding-right':30, 'padding-bottom':30, 
                                'color':'rgb(255, 255, 255)', 'display':'inline-block',
                                'font-family':'Anonymice Powerline', 'letter-spacing': '.1rem'}),
                    dropdown_menu()
                    ], style={'display':'inline-block'})
            ], style={'backgroundColor': 'rgb(1, 91, 176)', 'height':'60px', 'margin': -10, 'padding':10})


def graph_area():
    return html.Div([
            dcc.Graph(id='transaction_plot', style={'padding-top':10})
            ])
    
def dropdown_filter(values):
    return dcc.Dropdown(
                id='usr_filter',
                options=[{'label':value, 'value':value} for value in values],
                value=values,
                multi=True,
                clearable=False
            )

def dropdown_channels():
    return dcc.Dropdown(
                id='ddn_channels',
                options=[
                        {'label': 'CALLS', 'value': 'CALLS'},
                        {'label': 'EMAILS', 'value': 'EMAILS'}
                        ],
                value='EMAILS',
                #style={'width':'70%', 'display':'inline-block', 'height':'30px'}
                )

def dropdown_centrality():
    return dcc.Dropdown(
                id='ddn_centrality',
                options=[
                        {'label': 'Page Rank', 'value': 'Rank'},
                        {'label': 'Betweenness Centrality', 'value': 'BCRank'},
                        {'label': 'Article Rank', 'value': 'ArticleRank'},
                        {'label': 'Closeness Centrality', 'value': 'ClosenessRank'},
                        {'label': 'Harmonic Centrality', 'value': 'HarmonicRank'},
                        {'label': 'In Degree Centrality', 'value': 'InDegreeCentrality'},
                        {'label': 'Out Degree Centrality', 'value': 'OutDegreeCentrality'},
                        {'label': 'Eigen Centrality', 'value': 'EigenCentrality'},
                        ],
                value='Rank',
                #style={'width':'70%', 'display':'inline-block', 'height':'30px'}
                )

def dropdown_community():
    return dcc.Dropdown(
                id='ddn_community',
                options=[
                        {'label': 'Label Propagation', 'value': 'Community'},
                        {'label': 'Louvian Community', 'value': 'LouvianCommunity'},
                        {'label': 'Weakly Connected Components', 'value': 'WCCCommunity'},
                        {'label': 'Triangle Count', 'value': 'triangleCommunity'},
                        ],
                value='Community',
                #style={'width':'70%', 'display':'inline-block', 'height':'30px'}
                )

def neograph_area():
    return html.Iframe(id = 'nodelink_plot', style={'border': 'none', 'height': 900, 'width':1400})

    
def analytics_filter():
    return html.Div([
            html.Div([
                    html.H6('Select Channel'),
                    dropdown_channels(),
                    html.H6('Centrality Measure'),
                    dropdown_centrality(),
                    html.H6('Community Detection Measure'),
                    dropdown_community()
                    ], style={'padding':10, 'padding-top':30})
            
            ])

def analytics_area():
    return html.Div([
            html.Div([
                    analytics_filter(),
                    ], style={'width': '30%', 'backgroundColor': 'rgba(1, 91, 176, 0.6)', 'height': 900,
                            'display':'inline-block', 'vertical-align': 'top'}),
            html.Div([
                    neograph_area()
                    ], style={'width': '70%', 'display':'inline-block'})
            ], style={'display': 'inline-block'})

def main_layout():
    return html.Div([main_banner(),
                     dropdown_banner(),
                     analytics_area(),
                     graph_area(),
                     html.Pre(id='selected-data')]) 

if __name__ == "__main__":
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    app.layout = main_layout()
    app.run_server(debug=True)