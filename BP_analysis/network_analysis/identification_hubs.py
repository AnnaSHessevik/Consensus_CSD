# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 15:35:24 2022

@author: annas
This script identifies and write hubs with k > n to a file. 
The node homogeneity is also calculated for each hub.
"""
import networkx as nx

if __name__ == '__main__':
    #Determine n
    n = 9
    
    #Open files
    arithmetic_file = open("filtered_arithmetic_CSDSelection_10000.txt", 'rb')
       
    #Create network
    G = nx.read_edgelist(arithmetic_file, data=[('weight',float), ('edge type', str)])
    
    #Close files
    arithmetic_file.close()

    #Open outfile
    outfile = open("hub_characteristics.txt", "w")
    outfile.write("Node\tk\tk_C\tk_S\tk_D\tH\n")
    
    #Identify hubs
    for node in G.nodes:
        if G.degree[node] > n:
            k_c = 0
            k_s = 0
            k_d = 0
            k = G.degree[node]
            #Identify edge specific degree
            for nbr, datadict in G[node].items():
                if datadict["edge type"] == "C":
                    k_c += 1
                elif datadict["edge type"] == "S":
                    k_s += 1
                elif datadict["edge type"] == "D":
                    k_d += 1
                    
            #calculate node homogeneity
            h = (k_c/k)**2 + (k_s/k)**2 + (k_d/k)**2
            outfile.write(node + "\t" + str(k) + "\t" + str(k_c) + "\t" + str(k_s) + "\t" + str(k_d) + "\t" + str(round(h,2)) + "\n")
            
    outfile.close()