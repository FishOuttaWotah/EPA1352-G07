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

        # extract sourcesink points, maybe return a randomised end point for one/multiple:
        self.sourcesinks = self.raw[self.raw.model_type == 'sourcesink'].copy(deep=False)
        self.sourcesinks.drop(columns=['model_type', 'condition', 'length'], inplace=True)
        self.sourcesinks.set_index(keys='id', drop=False, inplace=True)

        self.intersections = self.raw[self.raw.model_type == 'intersection'].copy(deep=False)
        self.intersections.set_index('id', inplace=True)
        self.intersections.sort_index(inplace=True)

        # clean per road for edge creation in NX
        self.links2 = pd.DataFrame()
        self.nodes2 = pd.DataFrame()
        for road in self.raw.road.unique():
            self.road_geometry = self.raw[self.raw.road == road].copy(deep=False)
            # self.road_links = self.road_geometry[self.road_geometry.model_type != 'sourcesink']
            self.road_geometry.reset_index(drop=True,inplace=True)
            self.road_links = self.road_geometry.iloc[1:].copy(deep=True)
            road_col_id = self.road_geometry.columns.get_loc('id')
            self.road_links['length'] = 0   # sets edges to zero, only nodes have weights to travel
            self.road_links['source'] = self.road_geometry.iloc[self.road_links.index - 1, road_col_id].array
            self.road_links['target'] = self.road_geometry.iloc[self.road_links.index, road_col_id].array
            self.road_links.set_index('id', drop=False, inplace=True)  # used in edges and nodes!
            self.road_geometry.rename(columns={'length': 'weight'}, inplace=True)
            self.links2 = self.links2.append(self.road_links)
            self.nodes2 = self.nodes2.append(self.road_geometry)

        # Create NetworkX Graph object, using links as NX edges
        self.nx_roads = nx.convert_matrix.from_pandas_edgelist(self.links2,
                                                               edge_attr=['road', 'lat', 'lon'])
        self.nodes2.drop_duplicates(subset='id',keep='first',inplace=True) # eliminate duplicate intersections
        self.nodes2.set_index(keys='id', drop=False, inplace=True)  # NX takes node IDs from index
        self.road_nodes_dict = self.nodes2[['road', 'id', 'model_type', 'lat', 'lon', 'weight']].to_dict(
            orient='index')
        nx.set_node_attributes(self.nx_roads,
                               self.road_nodes_dict)  # appends node attributes (such as labels and weights)
        #                                                        edge_attr=['road', 'id', 'lat', 'lon', 'weight'])
        self.nx_roads = self.nx_roads.to_undirected(
            as_view=True)  # converts above line from directed to undirected, see below
        # ADDENDUM: NX's conversion from Pandas to Graph creates a directed node (single way). Setting to undirected would
        #   mean two-way traffic is possible (in theory)

    def find_shortest_path(self, v_source=None, v_target=None, verbose=False):
        """
        Returns the shortest path, given that the NX network object is available.
        Will add more functionality to return the length of shortest path
        """
        choices = self.sourcesinks.index.tolist()
        if v_source is None and v_target is None:
            v_source, v_target = random.choices(choices, k=2)
        elif v_source is None:
            choices = choices.remove(v_target)
            v_source = random.choice(choices)
        elif v_target is None:
            choices = choices.remove(v_source)
            v_target = random.choice(choices)


        test_path = nx.algorithms.shortest_paths.generic.shortest_path(self.nx_roads, source=v_source, target=v_target,
                                                                       weight='length')
        # test_length = sum([self.nx_roads[test_path[i]][test_path[i + 1]]['weight'] for i in range(len(test_path) - 1)])
        test_length = sum([self.nx_roads.nodes[node]['weight'] for node in test_path])
        if verbose:
            print(f'{v_source} to {v_target}')
            print(test_length)
        return test_path, test_length

    def test_all_paths(self, target):
        # test all paths to N1 end, including N1 start
        successes = []
        fails = []
        for startpoint in self.sourcesinks.index:
            if nx.algorithms.shortest_paths.generic.has_path(self.nx_roads, startpoint, target):
                # means path exists, intersections work
                successes.append(startpoint)
            else:
                fails.append(startpoint)
        return successes, fails

    def check_broken_points(self):
        broken_roads = []
        for road in graph.nodes.road.unique():
            road_nodes = graph.nodes[graph.nodes.road == road]['id'].array
            if nx.algorithms.shortest_paths.generic.has_path(graph.nx_roads, road_nodes[0],
                                                             road_nodes[-1]):
                # print(f'{road} is fine')
                continue
            else:
                for node in road_nodes:
                    if nx.algorithms.shortest_paths.generic.has_path(graph.nx_roads, node,
                                                                     road_nodes[-1]):
                        # print(f'\tconnection starts at {node} for {road}')
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
