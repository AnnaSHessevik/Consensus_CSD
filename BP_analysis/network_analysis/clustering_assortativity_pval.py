# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 17:24:03 2022

@author: annas
This script generates new networks from a given degree sequence
using a configuration model. For each network, the assortativity and clustering 
is calculated. This is used to estimate a p-value for the assortativity and 
clustering coefficients of the CSD network and its subnetworks."""

import networkx as nx


#Estimate p-value
def estimate_pval(random, actual, num_sim):    
    #Extreme case
    if (actual < random[0] or actual > random[num_sim-1]):
        print("Extreme case")
        return 1/num_sim
    
    for i in range(num_sim):        
        #Find position of actual value in the list of random values
        if random[i] > actual:
            print(i) #just to help with debugging
            #Estimate p-value
            if i < num_sim/2: 
                return (i/num_sim)*2 #multiply by 2 as we perform a two-sided test
            else:
                return (1-(i/num_sim))*2 #multiply by 2 as we perform a two-sided test
   
            
if __name__ == '__main__':    
    #Open files
    CSD = open("filtered_arithmetic_CSDSelection_10000.txt", 'rb')
    #C = open("filtered_arithmetic_CNetwork_10000.txt", 'rb')
    #S = open("filtered_arithmetic_SNetwork_10000.txt", 'rb')
    #D = open("filtered_arithmetic_DNetwork_10000.txt", 'rb')
    
    #Create CSD network
    G = nx.read_edgelist(CSD, data=[('weight',float), ('edge type', str)])
    #G = nx.read_edgelist(C, data=[('weight',float), ('edge type', str)])
    #G = nx.read_edgelist(S, data=[('weight',float), ('edge type', str)])
    #G = nx.read_edgelist(D, data=[('weight',float), ('edge type', str)])
    
    #Close files
    CSD.close()
    #C.close()
    #S.close()
    #D.close()
    
    #Find degree sequence
    actual_degrees = [d for v, d in G.degree()]
    
    #Calculate actual assortativity and clustering coefficients
    actual_r = nx.degree_assortativity_coefficient(G, weight = None)
    actual_c = nx.average_clustering(G, weight = None)
    
    #Create random graph with the given degree sequence and calculate 
    #assortativity and clustering
    assortativity = []
    clustering = []
    num_sim = 1000
    for i in range(num_sim):
        #Generate random graph
        G_rand = nx.configuration_model(actual_degrees, create_using = nx.classes.graph.Graph)
        
        #Calculate assortativity and clustering
        r = nx.degree_assortativity_coefficient(G_rand, weight = None)
        c = nx.average_clustering(G_rand, weight = None)
        
        #Add assorativity and clustering to list 
        assortativity.append(r)
        clustering.append(c)
    
    #Find position of actual assortativity and clustering coefficients in the
    #list of random assortativity and clustering coefficients
    assortativity.sort()
    clustering.sort()
    
    p_r = estimate_pval(assortativity, actual_r, num_sim)
    p_r_adj = 4*p_r #Note: may become higher than 1 due to correction
    
    print("Adjusted p-value for assortativity:", p_r_adj)
    
    p_c = estimate_pval(clustering, actual_c, num_sim)
    p_c_adj = 4*p_c #Note: may become higher than 1 due to correction
    
    print("Adjusted p-value for clustering:", p_c_adj)
 

            
        
        
        
        
    
    
    