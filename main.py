#!/usr/bin/env python
# coding=utf-8
# Python version = 2.7.15

from src.phylogeny_travel import TravelPhylogeny
import os
import re
from time import sleep
import networkx as nx



TravelPhylogeny = TravelPhylogeny()
 ## Create a graph from ncbi sqldb
G = TravelPhylogeny.Graph_from_sqldb(sqlite_db = "data/taxa.sqlite")

## Process assembly file
assembly= TravelPhylogeny.assembly_file_process(assembly_file_name = "data/assembly_summary_refseq_1.txt")

## Add FTP full link in graph attribute genome
i = 0
for taxaid in assembly['taxid']:
    G.node[taxaid]['genome'].append(assembly.iloc[i][22])
    i = i + 1  

## Select the taxid for which we want to make a dna sensor of length k   
seed = 83332
seed_mer = TravelPhylogeny.create_seed_mer(seed=seed,G=G,k=100)
TravelPhylogeny.put_list_node_in_gzip(seed,seed_mer)

## If graph is directed, convert to undirected to travel relevant node
H = G.to_undirected()

## Write path to a file
path_of_search_space= list(nx.dfs_preorder_nodes(H,seed))

TravelPhylogeny.write_path("path",str(path_of_search_space))
print(path_of_search_space[1:20])

## search path and processing
TravelPhylogeny.create_and_save_kmer_from_path_of_search_space(G=G,seed_mer=seed_mer,
                                               k=100,path_of_search_space=path_of_search_space)
