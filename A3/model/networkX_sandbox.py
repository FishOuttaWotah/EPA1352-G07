import networkx as nx
import pandas as pd
import random

# import matplotlib.pyplot as plt
# import numpy as np
# import os.path

# from os import path
"""
NX expected outputs to MESA
    * import this into model.py
    * create a Road_n_Network object in model
    * current road geometry uses Rory's csv by default '../data/ (make sure it's updated)
    * TO FIND SHORTEST PATH, run <RnN obj>.find_shortest_path(<source>,<target>).
        You should get a list-like object that's like [sourceID, nodeID, ..., intersectionID, ..., targetID]
    * some dataframe objects can be retrieved from calling <RnN obj>.something:
        .raw = full Rory's dataset in Pandas (with some minor manual edits)
        .intersections = subset of intersection points
        .sourcesinks = sourcesink objects
        .nx_roads = the actual NX Graph object (which is used for NX functions)
        
Working operation:
> Road_n_Network class opens the road geometry csv file

"""


class Road_n_Network:

    def __init__(self, roads_file='../data/compiled_roads_bridges.csv'):
        # OPEN ROAD ELEMENT FILES,
        self.raw = pd.read_csv(roads_file)
        self.raw['model_type'] = self.raw.model_type.str.strip()  # ensures only chars remain and no hidden whitespace
        # assumption (safe): above line assumes that the csv file only contains exactly the chars needed to match

        # EXTRACT SOURCESINK POINTS AND INTERSECTION POINTS
        # specified 'shallow' copy to imply reference to original (if original is changed, this does too),
        #   but mostly to shut Pandas up with their warnings
        self.sourcesinks = self.raw[self.raw.model_type == 'sourcesink'].copy(deep=False)     #
        self.sourcesinks.drop(columns=['model_type', 'condition', 'length'], inplace=True)
        self.sourcesinks.set_index(keys='id', drop=False, inplace=True)

        self.intersections = self.raw[self.raw.model_type == 'intersection'].copy(deep=False)
        self.intersections.set_index('id', inplace=True)
        self.intersections.sort_index(inplace=True)

        # CLEAN PER ROAD FOR EDGE & NODE CREATION IN NX
        """
        Mechanism:
        * All geometry items are nodes, even the links in the csv 
        * Edges are items between nodes
        
        """
        self.edges = pd.DataFrame()    # dataframe to grow for edges, ditto next for nodes
        self.nodes = pd.DataFrame()
        for road in self.raw.road.unique():
            self.road_nodes = self.raw[self.raw.road == road].copy(deep=False)   # extract specific road code
            self.road_nodes.reset_index(drop=True, inplace=True)  # so that iloc works later
            self.road_edges = self.road_nodes.iloc[1:].copy(deep=True)   # take N-1 roads because that's number of edges
            road_col_id = self.road_nodes.columns.get_loc('id')      # just in case 'id' column moves elsewhere
            self.road_edges['length'] = 0   # creates lengths of zero, only nodes have lengths (for NX weights)
            self.road_edges['source'] = self.road_nodes.iloc[self.road_edges.index - 1, road_col_id].array
            self.road_edges['target'] = self.road_nodes.iloc[self.road_edges.index, road_col_id].array
            self.road_nodes.rename(columns={'length': 'weight'}, inplace=True)
            self.edges = self.edges.append(self.road_edges)
            self.nodes = self.nodes.append(self.road_nodes)

        # Create NetworkX Graph object, using links as NX edges
        self.nx_roads = nx.convert_matrix.from_pandas_edgelist(self.edges,edge_attr=['road', 'lat', 'lon'])
        # ^ creates directed NX Graph with edges per row, going from 'source' to 'target', and extra edge attributes
        self.nodes.drop_duplicates(subset='id', keep='first', inplace=True) # eliminate duplicate intersections for dict creation
        self.nodes.set_index(keys='id', drop=False, inplace=True)  # because NX takes node IDs from index
        self.road_nodes_dict = self.nodes[['road', 'id', 'model_type', 'lat', 'lon', 'weight']].to_dict(
            orient='index') # map DF to nested dict, with node IDs as index identifier
        nx.set_node_attributes(self.nx_roads,self.road_nodes_dict)  # appends node attributes (coords and weights)
        self.nx_roads = self.nx_roads.to_undirected(
            as_view=True)  # converts above line from directed to undirected, see below
        # ADDENDUM: NX's conversion from Pandas to Graph creates a directed node (single way). Setting to undirected would
        #   mean two-way traffic is possible

    def find_shortest_path(self, v_source=None, v_target=None, verbose=False):
        """
        Returns the shortest path and path length, given that the NX network object is available.
        """
        # basic randomisation routine for diagnostic
        choices = self.sourcesinks.index.tolist()
        if v_source is None and v_target is None:
            v_source, v_target = random.choices(choices, k=2)
        elif v_source is None:
            choices = choices.remove(v_target)
            v_source = random.choice(choices)
        elif v_target is None:
            choices = choices.remove(v_source)
            v_target = random.choice(choices)

        # input NetworkX Graph object, set source and target, gets list of nodes to travel in return
        test_path = nx.algorithms.shortest_paths.generic.shortest_path(self.nx_roads, source=v_source, target=v_target,
                                                                       weight='length')
        # sum weight of nodes for the path for the travel distance (and doesn't include edges)
        test_length = [self.nx_roads.nodes[node]['weight'] for node in test_path]
        if verbose:
            print(f'{v_source} to {v_target}')
            print(test_length)
        return test_path, test_length

    def test_all_paths(self, target):
        # test all sourcesink points to attempt navigation to a  given target,
        # returns two lists of successful links and unsuccessful points.
        successes = []
        fails = []
        for startpoint in self.sourcesinks.index:
            if nx.algorithms.shortest_paths.generic.has_path(self.nx_roads, startpoint, target):
                # means path exists, intersections work
                successes.append(startpoint)
            else:
                fails.append(startpoint)
        return successes, fails

    def test_broken_points(self, verbose=False):
        # DEPRECIATED due to altered implementation of NetworkX
        # simple method for finding specific points where links are broken, returns list of (node,road) for broken ones
        # ONLY USEFUL for checking whole roads, not connections between roads
        # iterations of this is required if several broken links are present for a road
        broken_roads = []
        for road in graph.nodes.road.unique():
            road_nodes = graph.nodes[graph.nodes.road == road]['id'].array
            # checks at the start whether the full road is connected
            if nx.algorithms.shortest_paths.generic.has_path(graph.nx_roads, road_nodes[0],
                                                             road_nodes[-1]):
                if verbose: print(f'{road} is fine')
                continue # move on to next road
            else:
                for node in road_nodes:
                    # move down the road points to find the furthest point where connection is possible
                    if nx.algorithms.shortest_paths.generic.has_path(graph.nx_roads, node,
                                                                     road_nodes[-1]): # if such a point is found
                        if verbose: print(f'\tconnection starts at {node} for {road}')
                        broken_roads.append((node, road))
                        break
        return broken_roads

    def fix_intersection_links(self):
        """
        Adds links for cases where intersection-bridge occurs
        """
        for inter_idx in self.intersections.index.unique():
            # draw from raw (for adjacency)
            raw_idx = self.raw[self.raw.id == inter_idx].index
            raw_above = self.raw.loc[raw_idx - 1]
            raw_below = self.raw.loc[raw_idx + 1]
            # for adjacent in [raw_above,raw_below]:
            #     if
            pass


if __name__ == '__main__':  # ensures that this script won't run fully when imported
    graph = Road_n_Network()
    pass
