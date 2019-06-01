# -*- coding: utf-8 -*-
import os
import json
import networkx as nx


""" 
Compute a forwarding table from a predecessor list. 
"""
def forwarding(predecessor, source):

    pass  # TODO
	



"""
Least-cost or widest paths via Dijkstra's algorithm.
"""	
def dijkstra_generalized(graph, source, weight='weight', infinity=None, plus=None, less=None, min=None):
    p, d = nx.dijkstra_predecessor_and_distance(graph, source)
    return (p, d)




"""
Visualize the least-cost path tree for the given graph in task 1.1
"""
def task1_visualize():
    filename = os.path.join('.', 'task1.1.json')  # modify as required
    netjson = json.load(open(filename))
    
    graph = nx.Graph()
    
    graph.add_nodes_from((
        (node['id'], node['properties'])  # node-attributes
        for node in netjson['nodes']))
    
    graph.add_edges_from((
        # source-target-attributes
        (link['source'], link['target'], {'weight': link['cost']})
        for link in netjson[    'links']))
    
    p, d = dijkstra_generalized(graph, 'u')

    node_positions = nx.get_node_attributes(graph, name='pos')
    
    edge_label_positions = nx.draw_networkx_edge_labels(graph, pos=node_positions, 
        node_labels=nx.get_node_attributes(graph, name='name'), 
        edge_labels=nx.get_edge_attributes(graph, name='weight'))
    
    nx.draw_networkx(graph, pos=node_positions)




task1_visualize()