# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 22:45:50 2020

@author: Krishna Kinger
"""

import py2neo
import pandas as pd

def neo4j_query_process(channel, centrality, community):
    centrality = channel[:-1].lower() + centrality
    community = channel[:-1].lower() + community
    query = "match (nodes:demo) RETURN nodes"
    graph = py2neo.Graph(bolt=True, host='localhost', user='neo4j', password='mynewpass')
    df = graph.run(query).to_data_frame()
    nodes = df.nodes.apply(pd.Series).sort_values([community,centrality]).pid
    return nodes.tolist()


if __name__ == "__main__":
    channel = 'CALLS'
    centrality = 'BCRank'
    community = 'LouvianCommunity'
    nodes = neo4j_query_process(channel, centrality, community)