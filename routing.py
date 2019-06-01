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
    pred, dist = nx.dijkstra_predecessor_and_distance(graph, source)
    return (pred, dist)




"""
Visualize the least-cost path tree for the given graph in task 1.1
"""
def task1_visualize_tree():
    filename = os.path.join('.', 'task1.1.json')  # modify as required
    netjson = json.load(open(filename))
    
    graph = nx.Graph()
    
    graph.add_nodes_from((
        (node['id'], node['properties'])  # node-attributes
        for node in netjson['nodes']))
    
    graph.add_edges_from((
        # source-target-attributes
        (link['source'], link['target'], {'weight': link['cost']})
        for link in netjson['links']))
    
    pred, dist = dijkstra_generalized(graph, 'u')

    tree = nx.Graph()

    tree.add_nodes_from((
        (node['id'], node['properties'])  # node-attributes
        for node in netjson['nodes']))
    
    tree.add_edges_from((
        # source-target-attributes
        (k, v[0], {'weight': dist[k]-dist[v[0]]})
        for k, v in pred))

    node_positions = nx.get_node_attributes(tree, name='pos')
    
    edge_label_positions = nx.draw_networkx_edge_labels(tree, pos=node_positions, 
        node_labels=nx.get_node_attributes(tree, name='name'), 
        edge_labels=nx.get_edge_attributes(tree, name='weight'))
    
    nx.draw_networkx(p, pos=node_positions)




task1_visualize_tree()