# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 12:22:56 2022

@author: annas
This script identifies and writes disease genes to a file. 
The node homogeneity is also calculated for each gene.
Modified version of identification_hubs.py
"""
import networkx as nx

if __name__ == '__main__':    
    #Open files
    arithmetic_file = open("filtered_arithmetic_CSDSelection_10000.txt", 'rb')
    disease_genes = open("disease_genes.txt")   
    
    #Create network
    G = nx.read_edgelist(arithmetic_file, data=[('weight',float), ('edge type', str)])
    
    
    #Read disease genes
    gene_list = []
    for line in disease_genes:
        line_split = line.rstrip().split('\t')
        gene_list.append(line_split[0])

    #Close files
    arithmetic_file.close()
    disease_genes.close()    

    #Open outfile
    outfile = open("disease_genes_characteristics.txt", "w")
    outfile.write("Node\tk\tk_C\tk_S\tk_D\tH\n")
    
    #Identify disease genes
    for node in G.nodes:
        if node in gene_list:
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
