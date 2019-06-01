# -*- coding: utf-8 -*-
import os
import json
import networkx as nx
from routing import dijkstra_generalized


filename = os.path.join('.', 'KuroseRoss5-15.json')  # modify as required
netjson = json.load(open(filename))

# graph = nx.DiGraph()
graph = nx.Graph()

graph.add_nodes_from((
    (node['id'], node['properties'])  # node-attributes
    for node in netjson['nodes']))

graph.add_edges_from((
    # source-target-attributes
    (link['source'], link['target'], {'weight': link['cost']})
    for link in netjson['links']))

# =============================================================================
#  TEST task 1.1
# =============================================================================
p, d = dijkstra_generalized(graph, 'u')
print(p)
print(d)

node_positions = nx.get_node_attributes(graph, name='pos')

edge_label_positions = nx.draw_networkx_edge_labels(graph, pos=node_positions, 
    node_labels=nx.get_node_attributes(graph, name='name'), 
    edge_labels=nx.get_edge_attributes(graph, name='weight'))

nx.draw_networkx(graph, pos=node_positions)