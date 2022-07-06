# -*- coding: utf-8 -*-
"""
@author: thomleysens
"""

import sys
import os
import argparse
from tqdm.auto import tqdm


from pbf2graph.graph.transform import PBF2Graph

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="PBF file to graph-tool network .gt file"
        )
    parser.add_argument(
        "input",
        type=str,
        help="Path to .pbf file"
    )
    parser.add_argument(
        "output",
        type=str,
        help="Path to output .gt file"
    )
    args = parser.parse_args()
    bar = tqdm(
        total=3,
        desc="Make & Save Graph: Init"
    )
    transformation = PBF2Graph(
        args.input,
        # idx="dense_file_array,data/tmp.nodecache"
    )
    bar.desc = "Make & Save Graph: Graph"
    bar.update(1)
    transformation.get_graph()
    bar.desc = "Make & Save Graph: Save"
    bar.update(1)
    transformation.graph.save(
        args.output
    )
    bar.desc = "Make & Save Graph: DONE"
    bar.update(1)
    bar.close()