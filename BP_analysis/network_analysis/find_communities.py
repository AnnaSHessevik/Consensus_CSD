# -*- coding: utf-8 -*-
"""
Created on Mon Feb 28 10:39:58 2022

@author: annas
This script identifies communities in the input network using the Louvain algorithm.
"""

import networkx as nx
#from community import community_louvain
from networkx.algorithms import community

if __name__ == '__main__':
    #Open file
    network_file = open("filtered_arithmetic_CSDSelection_10000.txt", 'rb')
    
    #Create network
    G = nx.read_edgelist(network_file, data=[('score',float), ('edge type', str)])
    
    #Close file
    network_file.close()
    
    
    #Find communitites
    partitions = community.louvain_communities(G, weight=None) #treat network as unweighted
    
    #Write community structure to file
    community_structure = open("community_structure.txt", "w")
    community_nr = 0
    
    
    for nodes_set in partitions:
        if len(nodes_set) > 5:
            community_nr += 1
            for node in nodes_set:
                community_structure.write(node + '\t' + str(community_nr) + '\n')
        
    community_structure.close()
        

    
