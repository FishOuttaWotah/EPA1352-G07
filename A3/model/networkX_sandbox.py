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
    * some dataframe objects can be retrieved from calling <RnN obj>.something:
        .raw = full Rory's dataset in Pandas
        .intersections = subset of intersection points
        .sourcesinks = sourcesink objects
        .nodes = node points
        .nx_roads = the actual NX Graph object (which is used for NX functions)
        
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


class Road_n_Network:

    def __init__(self, roads_file='../data/compiled_roads_bridges.csv', trunc=False):
        # OPEN ROAD ELEMENT FILES,
        self.raw = pd.read_csv(roads_file)
        self.raw['model_type'] = self.raw.model_type.str.strip()  # ensures only chars remain and no hidden whitespace
        # assumption (safe): above line assumes that the csv file only contains exactly the chars needed to match

        if trunc:  # truncated mode is for verification purposes
            valid_list = ['N1','Z1402','Z1044','Z1042','Z1065','Z1048','Z1124','Z1031','R151','R170','Z1005'] # For the ones that work
            # valid_list = ['N2','R310','R360','R220','R241','Z2013']
            self.raw = self.raw.loc[self.raw.road.isin(valid_list)]

        # extract sourcesink points, maybe return a randomised end point for one/multiple:
        self.sourcesinks = self.raw[self.raw.model_type == 'sourcesink']
        self.sourcesinks.drop(columns=['model_type', 'condition', 'length'], inplace=True)
        self.sourcesinks.set_index(keys='id', drop=False, inplace=True)

        self.intersections = self.raw[self.raw.model_type == 'intersection']
        self.intersections.set_index('id', inplace=True)
        self.intersections.sort_index(inplace=True)

        # Separate into dataframe for 'links', clean and prepare for assignment as NX edges
        self.links = self.raw[self.raw.model_type == 'link']  # extract only 'links'
        self.links.drop(columns=['model_type', 'condition', 'name'],
                        inplace=True)  # drop irrelevant columns for NX edge
        id_col = self.raw.columns.get_loc('id')
        self.links['source'] = self.raw.iloc[self.links.index - 1, id_col].array  # set NX source, see assumption below
        self.links['target'] = self.raw.iloc[self.links.index + 1, id_col].array  # ditto for NX target
        self.links['idx_ori'] = self.links.index  # save original index as column
        self.links.rename(columns={'length': 'weight'}, inplace=True)  # rename length to weight for NX use
        self.links.set_index(keys='id', drop=False, inplace=True)  # set index to id codes
        # assumption (untested): source and target assumes that links are sequential,
        #   that it's in a node-link-node format in csv.

        # extract nodes (anything other than links), and ensure intersections are represented once (for technical reasons)
        self.nodes = self.raw[self.raw.model_type != 'link'].copy()
        self.nodes.set_index(keys='id', drop=False, inplace=True)  # NX takes node IDs from index
        self.nodes = self.nodes[~self.nodes.duplicated(subset='id', keep='first')]  # eliminate duplicate intersections
        self.nodes.rename(columns={'length': 'weight', 'index': 'idx_ori'},
                          inplace=True)  # rename length to NX's weights
        self.nwdict_nodes = self.nodes[['road', 'id', 'model_type', 'lat', 'lon', 'weight']].to_dict(orient='index')
        # (may be depreciated)
        # NOTE: ~ returns inverse of boolean mask
        # assumption (untested): intersections are duplicated per road in csv. however, the current method assumes that
        #   duplicate intersection sections have the same location/name. NX doesn't care about location much, so this is
        #   reasonable.


        # self.links2 = self.raw

        # Cold storage: sanity check whether intersections have same coordinates/lengths
        # nwdf_inters = self.nwdf_nodes[self.nwdf_nodes.duplicated(subset='id', keep=False)]
        # for infra_id in nwdf_inters.id.unique():
        #     # check for differences in
        #     print(infra_id)

        # Create NetworkX Graph object, using links as NX edges
        self.nx_roads = nx.convert_matrix.from_pandas_edgelist(self.links,
                                                               edge_attr=['road', 'id', 'lat', 'lon', 'weight'])
        self.nx_roads = self.nx_roads.to_undirected(
            as_view=True)  # converts above line from directed to undirected, see below
        nx.set_node_attributes(self.nx_roads, self.nwdict_nodes)  # appends node attributes (such as labels and weights)
        # ADDENDUM: NX's conversion from Pandas to Graph creates a directed node (single way). Setting to undirected would
        #   mean two-way traffic is possible (in theory)

    def find_shortest_path(self, v_source=None, v_target=None):
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

        print(f'{v_source} to {v_target}')
        test_path = nx.algorithms.shortest_paths.generic.shortest_path(self.nx_roads, source=v_source, target=v_target,
                                                                       weight='weight')
        # test_length = sum([self.nx_roads[test_path[i]][test_path[i+1]]['weight'] for i in range(len(test_path)-1)])
        # test_length = nx.algorithms.shortest_paths.generic.shortest_path_length(self.nx_roads, source=v_source, target=v_target,
        #                                                                     weight='weight')
        return test_path  # , test_length

    def test_all_paths(self,target):
        # test all paths to N1 end, including N1 start
        successes = []
        fails = []
        for startpoint in self.sourcesinks.index:
            if nx.algorithms.shortest_paths.generic.has_path(self.nx_roads,startpoint,target):
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
                        broken_roads.append((node,road))
                        break
        return broken_roads

    def fix_intersection_links(self):
        """
        Adds links for cases where intersection-bridge occurs
        """
        for inter_idx in self.intersections.index.unique():
            # draw from raw (for adjacency)
            raw_idx = self.raw[self.raw.id == inter_idx].index
            raw_above = self.raw.loc[raw_idx-1]
            raw_below = self.raw.loc[raw_idx+1]
            # for adjacent in [raw_above,raw_below]:
            #     if
            pass




if __name__ == '__main__':  # ensures that this script won't run fully when imported
    graph = Road_n_Network()
    pass
