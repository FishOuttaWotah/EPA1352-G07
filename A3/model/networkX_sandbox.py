import networkx as nx
import pandas as pd
import numpy as np

"""
from_pandas_dataframe()
distances between nodes are called weights? 

"""
# let's do the tutorial

G = nx.Graph()

# addition of nodes
G.add_nodes_from([
    (1, {'color': 'green'}),
    (2, {'color': 'red'}),
    (3, {'color': 'blue'})
])
H = nx.path_graph(10)
G.add_nodes_from(H) # extend nodes from G
# G.add_node(H) # append H to G as a composite node, ie. graph of graphs

# addition of edges
G.add_edges_from([(1,2),(1,3)]) # attr 'weight' can be added as 3rd arg (as dict) in tuple

# nodes can be labelled as numbers or str
# possible to use convert_node_labels_to_integers() to get purely int labels
