# -*- coding: utf-8 -*-
import os
import json
import networkx as nx
from routing import dijkstra_generalized, forwarding
from pprint import pprint


filename = os.path.join('.', 'task1.1.json')  # modify as required
netjson = json.load(open(filename))

# graph = nx.DiGraph()
graph = nx.Graph()

graph.add_nodes_from((
    (node['id'], node['properties'])  # node-attributes
    for node in netjson['nodes']))

graph.add_edges_from((
    # source-target-attributes
    (link['source'], link['target'], {'weight': link['weight']})
    for link in netjson['links']))

# =============================================================================
#  TEST task 1.1
# =============================================================================
d, p = dijkstra_generalized(graph, 'u')
print(d)
print(p)

table = forwarding(p, 'u')
print("\n\n")
pprint(table)

#node_positions = nx.get_node_attributes(graph, name='pos')
#
#edge_label_positions = nx.draw_networkx_edge_labels(graph, pos=node_positions, 
#    node_labels=nx.get_node_attributes(graph, name='name'), 
#    edge_labels=nx.get_edge_attributes(graph, name='weight'))
#
#nx.draw_networkx(graph, pos=node_positions)


























#import gevent
#import time
#
#
#num_tasks = 5
#def now():
#    return time.perf_counter()
#
#
#def one_task(pid):
#    # "pid" is "process identifier", a number
#    expected = 1.0 # seconds
#    print('{}: "Working" for {:f} sec... '.format(pid, expected))
#    start_time = now()
#    gevent.sleep(seconds=expected) # "hard work" :)
#    actual = now() - start_time
#    print('{}: Finished after {:f} sec'.format(pid, actual))
#
#
#def run_timed(fun, *args, title="Running..."):
#    print(title)
#    start_time = now()
#    fun(*args)
#    print('Required: {:f} sec'.format(now() - start_time))
#
#
#def run_tasks_synchronously():
#    for pid in range(num_tasks):
#        one_task(pid)
#
#
#def run_tasks_asynchronously():
#    threads = [gevent.spawn(one_task, pid) for pid in range(num_tasks)]
#    gevent.joinall(threads)
#    
#    
#run_timed(run_tasks_synchronously, title="Synchronous...")
#print()
#run_timed(run_tasks_asynchronously, title="Asynchronous...")