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

class NX_Graph:

    def __init__(self, roads_file='../data/compiled_roads_bridges.csv', trunc=True):
        # OPEN ROAD ELEMENT FILES,
        self.raw = pd.read_csv(roads_file)
        self.raw['model_type'] = self.raw.model_type.str.strip()  # ensures only chars remain and no hidden whitespace
        # assumption (safe): above line assumes that the csv file only contains exactly the chars needed to match

        if trunc:   # truncated mode is for verification purposes
            self.raw = self.raw[self.raw.road == 'N1']

        # Separate into dataframe for 'links', clean and prepare for assignment as NX edges
        self.links = self.raw[self.raw.model_type == 'link']  # extract only 'links'
        self.links.drop(columns=['model_type', 'condition', 'name'], inplace=True)  # drop irrelevant columns for NX edge
        id_col = self.raw.columns.get_loc('id')
        self.links['source'] = self.raw.iloc[self.links.index - 1, id_col].array  # set NX source, see assumption below
        self.links['target'] = self.raw.iloc[self.links.index + 1, id_col].array  # ditto for NX target
        self.links['idx_ori'] = self.links.index  # save original index as column
        self.links.rename(columns={'length': 'weight'}, inplace=True)  # rename length to weight for NX use
        self.links.set_index(keys='id', drop=False, inplace=True)  # set index to id codes
        # assumption (untested): source and target assumes that links are sequential,
        #   that it's in a node-link-node format in csv.

        # extract nodes (anything other than links), and ensure intersections are represented once (for technical reasons)
        self.nodes = self.raw[self.raw.model_type != 'link']
        self.nodes.set_index(keys='id', drop=False, inplace=True)    # NX takes node IDs from index
        self.nodes = self.nodes[~self.nodes.duplicated(subset='id', keep='first')]  # eliminate duplicate intersections
        self.nodes.rename(columns={'length': 'weight', 'index': 'idx_ori'}, inplace=True)   # rename length to NX's weights
        self.nwdict_nodes = self.nodes[['road', 'id', 'model_type', 'lat', 'lon', 'weight']].to_dict(orient='index')
        # (may be depreciated)
        # NOTE: ~ returns inverse of boolean mask
        # assumption (untested): intersections are duplicated per road in csv. however, the current method assumes that
        #   duplicate intersection sections have the same location/name. NX doesn't care about location much, so this is
        #   reasonable.

        # extract sourcesink points, maybe return a randomised end point for one/multiple:
        self.sourcesinks = self.raw[self.raw.model_type == 'sourcesink']
        self.sourcesinks.drop(columns=['model_type', 'condition', 'length'], inplace=True)
        self.sourcesinks.set_index(keys='id', drop=False, inplace=True)

        self.intersections = self.raw[self.raw.model_type == 'intersection']

        # Cold storage: sanity check whether intersections have same coordinates/lengths
        # nwdf_inters = self.nwdf_nodes[self.nwdf_nodes.duplicated(subset='id', keep=False)]
        # for infra_id in nwdf_inters.id.unique():
        #     # check for differences in
        #     print(infra_id)

        # Create NetworkX Graph object, using links as NX edges
        self.nx_roads = nx.convert_matrix.from_pandas_edgelist(self.links, edge_attr=['road', 'id', 'lat', 'lon', 'weight'])
        self.nx_roads = self.nx_roads.to_undirected(as_view=True) # converts above line from directed to undirected, see below
        nx.set_node_attributes(self.nx_roads, self.nwdict_nodes)  # appends node attributes (such as labels and weights)
        # ADDENDUM: NX's conversion from Pandas to Graph creates a directed node (single way). Setting to undirected would
        #   mean two-way traffic is possible (in theory)

    def find_shortest_path(self, v_source, v_target):
        """
        Returns the shortest path, given that the NX network object is available.
        Will add more functionality to return the length of shortest path
        """
        test_path = nx.algorithms.shortest_paths.generic.shortest_path(self.nx_roads, source=v_source, target=v_target,
                                                                       weight='weight')
        # test_length = sum([self.nx_roads[test_path[i]][test_path[i+1]]['weight'] for i in range(len(test_path)-1)])
        # test_length = nx.algorithms.shortest_paths.generic.shortest_path_length(self.nx_roads, source=v_source, target=v_target,
        #                                                                     weight='weight')
        return test_path #, test_length

    def check_broken_points(self):
        broken_points = []
        # iterate from start to end, finding points where

        pass
