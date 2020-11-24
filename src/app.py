# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 11:09:03 2020

@author: Krishna Kinger
"""
import dash
import pandas as pd
from html_components import main_layout
from utils import generate_plot
from neo4j_graph import neograph, neograph_filtered
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
     dash.dependencies.Input("ddn_community", "value"),
     dash.dependencies.Input('transaction_plot', 'selectedData')]
)
def update_graph(selected_graph, selected_channel, selected_centrality, selectedCommunity, selectedData):
    ctx = dash.callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    print(button_id)
    graph_label = selected_graph.rsplit('/', 1)[-1]
    if button_id == 'graphs':
        global df_neo4j
        query = "match (nodes:{}) RETURN nodes".format(graph_label.lower())
        graph = py2neo.Graph(bolt=True, host='localhost', user='neo4j', password='mynewpass')
        df_neo4j = graph.run(query).to_data_frame()
    persons = []
    tempo_fig = generate_plot(selected_graph)
    #if not ctx.triggered or button_id in ['graphs', 'ddn_channels']:
    nodelink_fig = neograph(selected_graph, selected_channel, selected_centrality, selectedCommunity)
    if button_id == 'transaction_plot':
        print('Filter operation')
        start_date = selectedData['range']['x'][0]
        end_date = selectedData['range']['x'][1]
        nodelink_fig = neograph_filtered(selected_graph, selected_channel, selected_centrality, 
                                         selectedCommunity, start_date, end_date)
        return dash.dash.no_update, nodelink_fig
        
    centrality = selected_channel[:-1].lower() + selected_centrality
    community = selected_channel[:-1].lower() + selectedCommunity
    if selected_centrality != 'None':
        persons = df_neo4j.nodes.apply(pd.Series).sort_values([centrality]).pid
    if selectedCommunity != 'None':
        persons = df_neo4j.nodes.apply(pd.Series).sort_values([community]).pid
    if selected_centrality != 'None' and selectedCommunity != 'None':
        persons = df_neo4j.nodes.apply(pd.Series).sort_values([community,centrality]).pid
    #if button_id in ['ddn_centrality', 'ddn_community']:
    tempo_fig.update_layout(yaxis= dict(categoryarray= persons))
        #return tempo_fig, dash.dash.no_update
    return tempo_fig, nodelink_fig
'''
@app.callback(
    dash.dependencies.Output('selected-data', 'children'),
    [dash.dependencies.Input('transaction_plot', 'selectedData')])
def display_selected_data(selectedData):
    start_date = selectedData['range']['x'][0]
    end_date = selectedData['range']['x'][1]
    
    #print(selectedData['range']['y'][0])
    #print(selectedData['range']['y'][1])
    print(start_date)
    print(end_date)
    #person_list = []
    #print(len(selectedData['points']))
    #for ite in selectedData['points']:
    #    person_list.append(ite['y'])
    #print(selectedData['points'][0]['y'])
    #print(selectedData['points'][-1]['y'])
    #print(person_list)
    return json.dumps(selectedData, indent=2)
'''
if __name__ == "__main__":
    app.run_server(debug=True)
