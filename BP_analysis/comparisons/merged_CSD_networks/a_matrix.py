# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 14:31:38 2022

@author: annas

This script visualizes the adjacency matrix of the merged CSD network
"""
import networkx as nx
#import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from matplotlib import patches
from collections import defaultdict
from networkx.algorithms import community
from collections import OrderedDict



def def_scores(G): #Define a new edge attribute called score     
    score = 0
    nx.set_edge_attributes(G, score, "score")
    
    #Determine score for each link
    for edge in G.edges:
        edge_type = G[edge[0]][edge[1]].get("edge type") #find edge type (C,S or D)
        origin = G[edge[0]][edge[1]].get("network origin") #find network origin (common, arithmetic, fisher)
        
        #Calculate score
        score = 0
        if edge_type == "C":
            score +=1
        elif edge_type == "S":
            score += 2
        elif edge_type == "D":
            score += 3
        
        #only alter score if the link is spesific for arithmetic or fisher network
        if origin == "arithmetic":
            score += 3
        elif origin == "fisher":
            score += 6
            
        G[edge[0]][edge[1]]["score"] = score           

#Generate a network list, and add information about network origin of nodes
def add_n_att(G, network_file):
    total_nodes = []
    common_nodes = []
    arithmetic_nodes = []
    fisher_nodes  = []
    nx.set_node_attributes(G, "none", "network origin")
    
    for line in network_file:
        split_line = line.rstrip().split('\t')
        #Add information about network origin
        G.nodes[split_line[0]]["network origin"] = split_line[1]
        
        #Add node and network origin to list
        total_nodes.append([split_line[0], split_line[1]])
        
        #Add node to list according to network origin
        if split_line[1] == "common":
            common_nodes.append(split_line[0])
            
        elif split_line[1] == "arithmetic":
            arithmetic_nodes.append(split_line[0])
            
        elif split_line[1] == "fisher":
            fisher_nodes.append(split_line[0])

    return total_nodes, common_nodes, arithmetic_nodes, fisher_nodes 


#Assign attributes, from http://sociograph.blogspot.com/2012/11/visualizing-adjacency-matrices-in-python.html
def assign_nodes(assignment_list):
    by_attribute_value = defaultdict(list)
    for el in assignment_list:
        by_attribute_value[el[1]].append(el[0])
    return by_attribute_value.values()

#Plot adjacency matrix, from http://sociograph.blogspot.com/2012/11/visualizing-adjacency-matrices-in-python.html
def draw_adjacency_matrix(G, node_order=None, partitions=[], colors=[]):
    """
    - G is a netorkx graph
    - node_order (optional) is a list of nodes, where each node in G
          appears exactly once
    - partitions is a list of node lists, where each node in G appears
          in exactly one node list
    - colors is a list of strings indicating what color each
          partition should be
    If partitions is specified, the same number of colors needs to be
    specified.
    """
    A = nx.to_numpy_matrix(G, nodelist=node_order, weight="score")

    #Plot adjacency matrix 
    ax = plt.subplot()
    ax.tick_params(length=0, width=0) #remove ticks
    plt.spy(A, precision=0, markersize=0.2, c = "mediumblue", label = "C, common", marker = "o")
    plt.spy(A, precision = 1, markersize=0.2, c = "forestgreen", label = "S, common", marker = "o")
    plt.spy(A, precision = 2, markersize=0.2, c = "firebrick", label = "D, common", marker = "o")
    plt.spy(A, precision = 3, markersize=0.2, c = "cyan", label = "C, unique", marker = "o")
    plt.spy(A, precision = 4, markersize=0.2, c = "lime", label = "S, unique", marker = "o")
    plt.spy(A, precision = 5, markersize=0.2, c = "deeppink", label = "D, unique", marker = "o")
    plt.spy(A, precision = 6, markersize=0.2, c = "cyan", marker = "o") #label = "C, transformed")
    plt.spy(A, precision = 7, markersize=0.2, c = "lime", marker = "o") #label = "S, transformed")
    plt.spy(A, precision = 8, markersize=0.2, c = "deeppink", marker = "o") # label = "D, transformed")
   
    
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.23), ncol=2, fontsize = "small", edgecolor = "gray", markerscale = 20)  
    
    
    # Highlight module boundaries
    assert len(partitions) == len(colors)
    ax = plt.gca()
    for partition, color in zip(partitions, colors):
        current_idx = 0
        for module in partition:
            ax.add_patch(patches.Rectangle((current_idx, current_idx),
                                          len(module), # Width
                                          len(module), # Height
                                          facecolor="none",
                                          edgecolor=color,
                                          linewidth="1", linestyle="--"))
            current_idx += len(module)

    ax.set_xticklabels([])
    ax.set_yticklabels([])
    plt.savefig("A_matrix_merged.png", dpi=500, bbox_inches='tight')




def find_communities(Gs):
    partitions = defaultdict(list)
    community_id = 1
    
    for G in Gs:
        #Identify communitites
        coms = community.louvain_communities(G, weight=None) #treat network as unweighted
        par = defaultdict(list)
        
        #Convert to suitable format
        for com in coms:
            #Add community to partitions
            #partitions[community_id] = list(com)
            par[community_id] = list(com)
            community_id += 1
            
        #Sort partitions for each network type by length
        par_ordered = OrderedDict(sorted(par.items(), key=lambda item: len(item[1]), reverse=True))   
        
        #Add sorted partitions to combined partitions
        partitions.update(par_ordered)
      
    return partitions.values()


if __name__ == '__main__':
    #Open file
    network_file = open("merged_arithmetic_fisher.txt", 'rb')
    
    #Create network
    G = nx.read_edgelist(network_file, data=[('edge type',str), ('network origin', str)])
    
    #Close file
    network_file.close()
    
    #Create a scoring system that give edges a score based on edge type and network origin
    def_scores(G)
    
    #Add node list according to network origin
    network_file2 = open("merged_network_attributes.txt")
    total_nodes, common_nodes, arithmetic_nodes, fisher_nodes  = add_n_att(G, network_file2)
    network_file2.close()
    
    #Get and plot adjacency matrix (sorted according to network origin)
    #A = nx.to_numpy_array(G) #, weight="score")

    #Assign nodes to network origin
    origin_list = assign_nodes(total_nodes)
    
    #Create a list of nodes, sorted by network origin
    nodes_origin_ordered = [node for origin in origin_list for node in origin]
    
    #Make subgraphs
    G_common = nx.Graph.subgraph(G, common_nodes)
    G_arithmetic = nx.Graph.subgraph(G,arithmetic_nodes)
    G_fisher = nx.Graph.subgraph(G,fisher_nodes)
    
    #Find community structure
    partitions = find_communities([G_common, G_arithmetic, G_fisher])
    
    #Create a list of nodes, sorted by communities
    nodes_community_ordered = [node for com in partitions for node in com]

    
    #Plot adjacency matrix    
    draw_adjacency_matrix(G, nodes_community_ordered, [origin_list, partitions], ["black", "none"])


    

    
    

