# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 20:06:49 2020

@author: Krishna Kinger
"""
graph_dict = {'../data/DEMO': 'demo',
              '../data/VAST_G1': 'vastg1',
              '../data/VAST_G2': 'vastg2',
              '../data/VAST_G3': 'vastg3',
              '../data/VAST_G4': 'vastg4',
              '../data/VAST_G5': 'vastg5',
              '../data/VAST_TEMPLATE': 'vasttemplate',
        }
def neograph(graphname, channel, centrality, community):
    graphname = graph_dict[graphname]
    centrality = channel[:-1].lower() + centrality
    community = channel[:-1].lower() + community
    index_string = '''
<!DOCTYPE html>
<html>
    <head>
        <title>DataViz</title>
        <style type="text/css">
            #viz{
                width: 1200px;
                height: 800px
            }
        </style>
        <script src="https://cdn.neo4jlabs.com/neovis.js/v1.5.0/neovis.js"></script>
    </head>
    <script>
        function draw() {
            var config = {
                container_id:"viz",
                server_url: "bolt://localhost:7687",
                server_user: "neo4j",
                server_password: "mynewpass",
                labels: {
                    "Person": {
                        caption: "pid",
                        size: "%s",
                        community: "%s"
                    }
                },
                relationships: {
                    "%s": {
                        caption: false,
                        thickness: "count"
                    }

                },
                initial_cypher: "MATCH p=(:%s)-[:%s]->(:%s) RETURN p"

            }
            var viz = new NeoVis.default(config);
            viz.render()
        }
    </script>
    <body onload='draw()'>
        <div id="viz"></div>
    </body>
</html>
''' % (centrality, community, channel, graphname, channel, graphname)
    return index_string

def neograph2():
    index_string = '''
<!DOCTYPE html>
<html>
    <head>
        <title>DataViz</title>
        <style type="text/css">
            #viz{
                width: 1700px;
                height: 900px
            }
        </style>
        <script type='text/javascript' src="https://cdn.neo4jlabs.com/neovis.js/v1.5.0/neovis.js"></script>
    </head>
    <script>
        function draw() {
            var config = {
                container_id:"viz",
                server_url: "bolt://localhost:7687",
                server_user: "neo4j",
                server_password: "mynewpass",
                labels: {
                    "Person": {
                        caption: "pid",
                        size: "callRank",
                        community: "callCommunity"
                    }
                },
                relationships: {
                    "CALLS": {
                        caption: false,
                        thickness: "count"
                    }

                },
                initial_cypher: "MATCH p=(:template)-[:CALLS]->(:template) RETURN p"

            }
            var viz = new NeoVis.default(config);
            viz.render()
        }
    </script>
    <body onload='draw()'>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
        <div id="viz"></div>
    </body>
</html>
'''
    return index_string

if __name__ == "__main__":
    pass
