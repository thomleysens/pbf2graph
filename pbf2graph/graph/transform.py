# -*- coding: utf-8 -*-
"""
@author: thomleysens
"""

import pandas as pd
import re
import numpy as np
from tqdm.auto import tqdm
from graph_tool import *
from geopy.distance import distance

from graph.handler import GraphHandler
from utils.utils import WAYS_TAGS

pd.options.mode.chained_assignment = None


class PBF2Graph:
    """
    Transform OSM PBF file to routable Graph-Tool Graph
    """
    
    def __init__(self, pbf, idx="flex_mem"):
        """
        Init 
        
        Note: to download PBF files, you can visit Geofabrik
              (https://download.geofabrik.de/)
        
        Parameters
        ----------
        pbf (str): Path to OpenStreetMap (OSM) 
                   Protocolbuffer Binary Format (PBF) file
        idx (str): Memory Management setting, for more details,
                   see: 
                   - https://osmcode.org/osmium-concepts/#indexes
                   - https://docs.osmcode.org/pyosmium/latest/intro.html#handling-geometries
                   Default: "flex_mem"
        """
        self.pbar = tqdm(
            total=5,
            desc="Init: Handler",
            leave=False
        )
        #Regex to remove non digit char for some columns
        self.non_decimal = re.compile(
            r"[^\d.]+"
        )
        gh = GraphHandler()
        gh.apply_file(
            pbf,
            locations=True,
            idx=idx
        )
        
        self.pbar.desc="Init: Properties"
        self.pbar.update(1)
        
        cols = []
        self.df = pd.DataFrame(gh.ways)
        for k in WAYS_TAGS.keys():
            if k in self.df.columns:
                cols.append(k)
        cols.append("nodes")
        self.df = self.df[cols]
        self.df = self.df.explode(
            "nodes"
        ).reset_index(
            drop=True
        )
        for col, type_ in WAYS_TAGS.items():
            if col in self.df.columns:
                if type_ == "string":
                    self.df[col].fillna(
                        "",
                        inplace=True
                    )
                else:
                    self.df[col] = self.df[col].map(
                        self._digit_filter
                    )
                    self.df[col].fillna(
                        0,
                        inplace=True
                    )
        
        self.graph = Graph()
        self.node_id = self.graph.new_vertex_property(
            "long"
        )
        self.graph.vertex_properties["id"] = self.node_id
        self.position = self.graph.new_vertex_property(
            "vector<double>"
        )
        self.graph.vertex_properties["position"] = self.position
        self.x = self.graph.new_vertex_property(
            "double"
        )
        self.graph.vertex_properties["x"] = self.x
        self.y = self.graph.new_vertex_property(
            "double"
        )
        self.graph.vertex_properties["y"] = self.y
        
        self.pbar.desc="Init: DataFrames"
        self.pbar.update(1)
        
        self.nodes = self.df[
            ["nodes"]
        ]
        self.nodes["nodes"] = self.nodes["nodes"].map(
            self._get_node
        )
        new_col_list = ["node_index","lon","lat"]
        for n, col in enumerate(new_col_list):
            self.nodes[col] = self.nodes["nodes"].apply(
                lambda x: x[n]
            )
        self.nodes = self.nodes.drop(
            "nodes", 
            axis=1
        ).drop_duplicates()
        self.nodes["node_index"] = pd.to_numeric(
            self.nodes["node_index"]
        )
        self.nodes.set_index(
            "node_index",
            drop=True,
            inplace=True
        )
        self.nodes["id"] = [
            i for i in range(
                len(
                    self.nodes
                )
            )
        ]
        self.df["next_nodes"] = self.df["nodes"].shift(-1)
        self.df["next_id"] = self.df["id"].shift(-1)
        self.df = self.df[:-1]
        
        self.pbar.desc="Init: Get length"
        self.pbar.update(1)
        
        self._distance()
        
        self.pbar.desc="Init: Clean & Format"
        self.pbar.update(1)
        
        self.df["nodes"] = self.df["nodes"].map(
            lambda x: int(
                x.split("@")[0]
            )
        )
        self.df["next_nodes"] = self.df["next_nodes"].map(
            lambda x: int(
                x.split("@")[0]
            )
        )
        self.df["nodes"] = pd.to_numeric(
            self.df["nodes"]
        )
        self.df["next_nodes"] = pd.to_numeric(
            self.df["next_nodes"]
        )
        self._add_ep()
        self.pbar.desc = "Init: DONE"
        self.pbar.update(1)
        self.pbar.close()

    
    def _digit_filter(self, x):
        """
        Filter non digit character
        
        Parameters
        ----------
        x (object): element to filter
        
        Return 
        ------
        number (int or float)
        """
        number = self.non_decimal.sub("", str(x))
        if "." in number:
            number = float(number)
        elif number == "":
            number = np.nan
        else:
            number = int(number)
            
        return number
                        
    def _distance(self):
        """
        Measure the distance/length of edges
        """
        def _coords(x):
            x = x.split("@")[1].split("/")
            # latitude, longitude for geopy needs
            return (
                float(x[1]),
                float(x[0])
            )
        def _measure(x):
            return distance(
                x[0],
                x[1]
            ).meters
        tqdm.pandas(
            desc="Measuring Length",
            leave=False
        )
        self.df["ori"] = self.df["nodes"].map(
            _coords
        )
        self.df["dest"] = self.df["next_nodes"].map(
            _coords
        )
        self.df["length"] = list(
            zip(
                self.df.ori, 
                self.df.dest
            )
        )
        self.df["length"] = self.df["length"].progress_map(
            _measure
        )
        self.df.drop(
            columns=["dest", "ori"],
            inplace=True
        )
    
    def get_graph(self, chunk=100000):
        """
        Build Graph-Tool graph
        
        Parameters
        ----------
        chunk (int): Edges chunk size to be added to 
                     the graph
                     Default: 100000
        """
        
        def _add_edge(reverse=False):
            """
            Adding edge to the graph if same id way
            """
            node_index = self.nodes.at[
                row[node_id_col_nb],
                "id"
            ]
            next_node_index = self.nodes.at[
                row[next_node_id_col_nb],
                "id"
            ]
            if reverse is True:
                tuples = [next_node_index, node_index]
            else:
                tuples = [node_index,next_node_index]
            tuples.extend(
                [
                    row[col] for col in self.col_nbs
                ]
            )
            if row[way_id] == row[next_way_id]:
                self.edges_list.append(tuple(tuples))
            
        self.edges_list = []
        node_id_col_nb = self.df.columns.get_loc(
            "nodes"
        ) + 1
        next_node_id_col_nb = self.df.columns.get_loc(
            "next_nodes"
        ) + 1
        way_id = self.df.columns.get_loc(
            "id"
        ) + 1
        next_way_id = self.df.columns.get_loc(
            "next_id"
        ) + 1
        
        for row in tqdm(
            self.df.itertuples(),
            total=len(self.df),
            desc="Add edges",
            leave=False
        ):
            if row[self.oneway_nb] == "yes":
                _add_edge()
            else:
                _add_edge()
                _add_edge(reverse=True)

            if len(self.edges_list) == chunk:
                self.graph.add_edge_list(
                    self.edges_list, 
                    eprops=self.eprops
                )
                self.edges_list=[]

        if len(self.edges_list) < chunk:
            self.graph.add_edge_list(
                self.edges_list, 
                eprops=self.eprops
            )
            self.edges_list=[]
        
        self._add_nodes()
                
    def _add_nodes(self):
        """
        Adding nodes properties to the graph
        """
        for node in tqdm(
            self.nodes.itertuples(),
            total=len(self.nodes),
            desc="Add vertices' properties",
            leave=False
        ):
            pos = (node[1], node[2])
            self.position[
                self.graph.vertex(node[3])
            ] = pos
            self.node_id[
                self.graph.vertex(node[3])
            ] = node[0]
            x = node[1]
            y = node[2]
            self.x[
                self.graph.vertex(node[3])
            ] = x
            self.y[
                self.graph.vertex(node[3])
            ] = y
            
    def _get_node(self, node):
        """
        Format node
        
        Parameters
        ----------
        node (str): Node element
        
        Return
        ------
        node_id (str), lon (str), lat (str)
        """
        node = node.split("@")
        coords = node[1].split("/")
        lon = coords[0]
        lat = coords[1]
        node_id = node[0]
        
        return node_id, lon, lat
    
    def _add_ep(self):
        """
        Add edge properties to the graph
        """
        self.eprops = []
        self.col_nbs = []
        for col in self.df.columns:
            if col in WAYS_TAGS:
                eprop = self.graph.new_edge_property(
                    WAYS_TAGS[col]
                )
                self.graph.edge_properties[col] = eprop
                self.eprops.append(eprop)
                self.col_nbs.append(
                    self.df.columns.get_loc(
                        col
                    ) + 1
                )
        self.oneway_nb = self.df.columns.get_loc(
            col
        ) + 1