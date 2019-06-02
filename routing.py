# -*- coding: utf-8 -*-
def dijkstra_generalized(graph, source, weight='weight', infinity=None, plus=None, less=None, min=min):
    """
    Adapted from Lab 5: Least-cost or widest paths via Dijkstra's algorithm.
    Returns (distances, predecessors) in that order.
    """
    import math

    def c(x, y):
        return graph[x][y][weight]
    
    u = source
    N = frozenset(graph.nodes())
    NPrime = {u} # i.e. "set([u])"
    dist = dict.fromkeys(N, math.inf)
    pred = dict.fromkeys(N, [])
    
    # Initialization
    for v in N:
        if graph.has_edge(u, v):
                dist[v] = c(u, v)
                pred[v] = [u]
                
    dist[u] = 0
    # Loop and find shortest distances
    while NPrime != N:
        candidates = {w: dist[w] for w in N if w not in NPrime}
        w, Dw = min(candidates.items(), key=lambda item: item[1]) # Get candidate with smallest distance
        NPrime.add(w)
        for v in graph[w]:
            if v not in NPrime:
                DvNew = dist[w] + c(w, v)
                if DvNew < dist[v]:
                    dist[v] = DvNew
                    pred[v] = [w]
    
    return (dist, pred)



def task1_visualize_tree():
    """
    Visualize the least-cost path tree for the given graph in task 1.1
    """
    import os
    import json
    import networkx as nx
    
    filename = os.path.join('.', 'task1.1.json')
    netjson = json.load(open(filename))
    
    graph = nx.Graph()
    
    graph.add_nodes_from((
        (node['id'], node['properties'])  # node-attributes
        for node in netjson['nodes']))
    
    graph.add_edges_from((
        # source-target-attributes
        (link['source'], link['target'], {'weight': link['cost']})
        for link in netjson['links']))
    
    dist, pred = dijkstra_generalized(graph, 'u')

    tree = nx.Graph()

    tree.add_nodes_from((
        (node['id'], node['properties'])  # node-attributes
        for node in netjson['nodes']))
    
    tree.add_edges_from((
        (k, v[0], {'weight': dist[k]-dist[v[0]]})
        for k, v in pred.items() if v))

    node_positions = nx.get_node_attributes(tree, name='pos')
    
    edge_label_positions = nx.draw_networkx_edge_labels(tree, pos=node_positions, 
        node_labels=nx.get_node_attributes(tree, name='name'), 
        edge_labels=nx.get_edge_attributes(tree, name='weight'))
    
    nx.draw_networkx(tree, pos=node_positions)



def forwarding(predecessor, source):
    """ 
    Compute a forwarding table from a predecessor list. 
    """
    table = {}
    for node, pre in predecessor.items():
        
    


'''
main
'''
task1_visualize_tree()