# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 11:09:03 2020

@author: Krishna Kinger
"""
import json
import dash
import pandas as pd
from html_components import main_layout
from utils import generate_plot
from neo4j_graph import neograph
import py2neo

query = "match (nodes:demo) RETURN nodes"
graph = py2neo.Graph(bolt=True, host='localhost', user='neo4j', password='mynewpass')
df_neo4j = graph.run(query).to_data_frame()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = main_layout


@app.callback(
    [dash.dependencies.Output('transaction_plot', 'figure'),
     dash.dependencies.Output('nodelink_plot', 'srcDoc')],
    [dash.dependencies.Input("graphs", "value"),
     dash.dependencies.Input("ddn_channels", "value"),
     dash.dependencies.Input("ddn_centrality", "value"),
     dash.dependencies.Input("ddn_community", "value"),]
)
def update_graph(selected_graph, selected_channel, selected_centrality, selectedCommunity):
    tempo_fig = generate_plot(selected_graph)
    nodelink_fig = neograph(selected_graph, selected_channel, selected_centrality, selectedCommunity)
    centrality = selected_channel[:-1].lower() + selected_centrality
    community = selected_channel[:-1].lower() + selectedCommunity
    persons = df_neo4j.nodes.apply(pd.Series).sort_values([community,centrality]).pid
    tempo_fig.update_layout(yaxis= dict(categoryarray= persons))
    return tempo_fig, nodelink_fig

@app.callback(
    dash.dependencies.Output('selected-data', 'children'),
    [dash.dependencies.Input('transaction_plot', 'selectedData')])
def display_selected_data(selectedData):
    start_date = selectedData['range']['x'][0]
    end_date = selectedData['range']['x'][1]
    print(start_date)
    print(end_date)
    return json.dumps(selectedData, indent=2)

if __name__ == "__main__":
    app.run_server(debug=True)
