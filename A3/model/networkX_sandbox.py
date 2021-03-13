import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
# import numpy as np
import os.path

# from os import path
"""
Overarching Assumptions:
A: always a link-bridge-link system
A: lengths equals weights (sufficient for Dijkstra's distance setting)

Notes:
* Nodes can have weights too (in which can be done for bridges)
* NX's edge growing means that as long as intersections have same identifiers, they will get appended links
* Network could be initialised in start of simulation, in Infra determination phase

Potential features:
F: assigned delays could be set as 'distance-normalised for delay' for bridge points 

"""
# set paths for opening/saving
# network_filename = 'demo-4.csv'
network_filename = 'compiled_roads_bridges.csv'
network_path = '../data/' + network_filename
graph_output_name = 'nx_out0'  # set save output name convention
if os.path.isfile(network_path + graph_output_name):  # instead of overwriting, create new file with updated ending
    graph_output_name = 'nx_out[:-1]' + str(int(graph_output_name[-1]) + 1)
    print(graph_output_name)

# OPEN ROAD ELEMENT FILES,
nwdf_0 = pd.read_csv(network_path)
nwdf_0['model_type'] = nwdf_0.model_type.str.strip()  # ensures only chars remain and no hidden whitespace
# assumption (safe): above line assumes that the csv file only contains exactly the chars needed to match

# Separate into dataframe for 'links', clean and prepare for assignment as NX edges
nwdf_links = nwdf_0[nwdf_0.model_type == 'link']  # extract only 'links'
nwdf_links.drop(columns=['model_type', 'condition', 'name'], inplace=True)  # drop irrelevant columns for NX edge
nwdf_links['source'] = nwdf_0.iloc[nwdf_links.index - 1]['id'].array  # set NX source, see assumption below
nwdf_links['target'] = nwdf_0.iloc[nwdf_links.index + 1]['id'].array  # ditto for NX target
nwdf_links['idx_ori'] = nwdf_links.index  # save original index as column
nwdf_links.rename(columns={'length': 'weight'}, inplace=True)  # rename length to weight for NX use
nwdf_links.set_index(keys='id', drop=False, inplace=True)  # set index to id codes
# assumption (untested): source and target assumes that links are sequential,
#   that it's in a node-link-node format in csv.

# extract nodes (anything other than links), and ensure intersections are represented once (for technical reasons)
nwdf_nodes = nwdf_0[nwdf_0.model_type != 'link']
nwdf_nodes.set_index(keys='id', drop=False, inplace=True)    # NX takes node IDs from index
nwdf_nodes = nwdf_nodes[~nwdf_nodes.duplicated(subset='id', keep='first')]  # eliminate duplicate intersections
nwdf_nodes.rename(columns={'length': 'weight', 'index': 'idx_ori'}, inplace=True)   # rename length to NX's weights
nwdict_nodes = nwdf_nodes[['road', 'id', 'model_type', 'lat', 'lon', 'weight']].to_dict(orient='index')
# (may be depreciated)
# NOTE: ~ returns inverse of boolean mask
# assumption (untested): intersections are duplicated per road in csv. however, the current method assumes that
#   duplicate intersection sections have the same location/name. NX doesn't care about location much, so this is
#   reasonable.

# Cold storage: sanity check whether intersections have same coordinates/lengths
# nwdf_inters = nwdf_nodes[nwdf_nodes.duplicated(subset='id', keep=False)]
# for infra_id in nwdf_inters.id.unique():
#     # check for differences in
#     print(infra_id)

# Create NetworkX Graph object, using links as NX edges
nx_roads = nx.convert_matrix.from_pandas_edgelist(nwdf_links, edge_attr=['road', 'id', 'lat', 'lon', 'weight'])
nx_roads = nx_roads.to_undirected(as_view=True) # converts above line from directed to undirected, see below
nx.set_node_attributes(nx_roads, nwdict_nodes)  # appends node attributes (such as labels and weights)
# ADDENDUM: NX's conversion from Pandas to Graph creates a directed node (single way). Setting to undirected would
#   mean two-way traffic is possible (in theory)

# save as Gephi-readable file
# nx.readwrite.write_gexf(nx_roads, network_filename+graph_output_name+'.gexf')

nx.draw_networkx(nx_roads)
plt.show()
# find shortest path
test_item = nwdf_links.weight.to_dict()
test_path = nx.algorithms.shortest_paths.generic.shortest_path(nx_roads, source=1000013, target=1000000,
                                                               weight='weight')
test_length = nx.algorithms.shortest_paths.generic.shortest_path_length(nx_roads, source=1000013, target=1000000,
                                                                        weight='weight')
# print(nx_roads.nodes)

print(nwdf_0)

# data wrangling, separate links and node objects
# prompting edge growing from


"""
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
"""
