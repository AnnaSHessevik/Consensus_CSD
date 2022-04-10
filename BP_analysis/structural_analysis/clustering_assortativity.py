# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 13:00:04 2022

@author: annas
This script calculates assortativity and clustering of a input CSD 
network (and the individual C, S and D networks)
"""


import networkx as nx

if __name__ == '__main__':  
    #Open files
    C = open("filtered_fisher_CNetwork_10000.txt", 'rb')
    S = open("filtered_fisher_SNetwork_10000.txt", 'rb')
    D = open("filtered_fisher_DNetwork_10000.txt", 'rb')
    CSD = open("filtered_fisher_CSDSelection_10000.txt", 'rb')
    
    #Create networks
    networks = []
    networks.append((nx.read_edgelist(CSD, data=[('weight',float), ('edge type', str)]), "CSD"))
    networks.append((nx.read_edgelist(C, data=[('weight',float), ('edge type', str)]),"C"))
    networks.append((nx.read_edgelist(S, data=[('weight',float), ('edge type', str)]),"S"))
    networks.append((nx.read_edgelist(D, data=[('weight',float), ('edge type', str)]), "D"))
    
    #Close files
    C.close()
    S.close()
    D.close()
    CSD.close()
    
    #Open outfile 
    characteristics = open("fisher_characteristics.txt", "w")
    characteristics.write("Network type\tDegree assortativity coefficient\tAverage clustering coefficient\n")
    
    #Calculate assortativity and clustering coefficient
    for network in networks:
        r = nx.degree_assortativity_coefficient(network[0], weight = None)
        c = nx.average_clustering(network[0], weight = None)
        characteristics.write(network[1] + '\t' + str(r) + '\t' + str(c) + '\n')
    
    #Close outfile
    characteristics.close()
    