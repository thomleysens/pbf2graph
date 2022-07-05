# -*- coding: utf-8 -*-
"""
@author: thomleysens
"""
import osmium



class GraphHandler(osmium.SimpleHandler):
    """
    Handle OSM Ways elements with "higway" tag 
    """
    def __init__(self):
        osmium.SimpleHandler.__init__(self)
        self.ways = []
            
    
    def way(self, w):
        if w.tags.get("highway") is not None:  
            self.ways.append(
                {
                    k:v for k,v in w.tags
                }
            )
            self.ways[-1].update(
                {
                    "id":w.id
                }
            )
            self.ways[-1].update(
                {
                    "nodes":[
                        str(node) for node in list(
                            w.nodes
                        )
                    ]
                }
            )