# -*- coding: utf-8 -*-
"""
Created on Wed Jan 26 10:50:01 2022

@author: annas
This script finds the correlations used to calculate the C, S and D scores
in the CSD network. This is used to make sure that the correlations may be 
considered to be significant.
"""

import sys

#Make list of gene pairs and their interaction type (C,S or D) 
def identify_gene_pair(infile):
    gene_pairs = []
    edge_types = []
    for line in infile:
        split_line = line.rstrip().split('\t')
        gene_pairs.append((split_line[0], split_line[1]))
        edge_types.append(split_line[3]) #note that the edge type corresponding to a spesific gene pair will have the same index as the gene pair
    return gene_pairs, edge_types

#Identify correlations underlying each gene pair
def identify_cor(gene_pairs, edge_types, infile, outfile):
    interesting_cor = str(0)
    i = 0 #counter
    
    for line in infile: #go through all gene pairs
        split_line = line.rstrip().split('\t') #split the line
        
        if (split_line[0], split_line[1]) in gene_pairs: #check if gene pair is included in CSD
            i += 1
            sys.stdout.write("Gene pair nr." + str(i) + ": " + split_line[0] + ', ' + split_line[1] + '\n') #Follow loop
            
            #find index of gene pair in gene pair list --> match index in edge list
            index = gene_pairs.index((split_line[0], split_line[1]))  
            edge_type = edge_types[index]
            
            #Find lowest |correlation| if edge type is C or D. Find highest |correlation| if edge type is S.
            if edge_type == "C" or edge_type == "D":
                interesting_cor = str(min([float(split_line[2]), float(split_line[4])], key=abs))
            
            elif edge_type == "S":
                interesting_cor = str(max([float(split_line[2]), float(split_line[4])], key=abs))
            
            #write to file
            outfile.write(split_line[0] + '\t' + split_line[1] + '\t' + split_line[2] + '\t' + split_line[4] + '\t' + edge_type + '\t' + interesting_cor + '\n')
            
        


if __name__ == '__main__':
    #Open files
    infile1 = open("arithmetic_AllValues.txt")
    next(infile1) #skip header
    infile2 = open("arithmetic_CSDSelection_10000.txt")
    outfile = open("arithmetic_underlying_cor_CSD.txt", 'w')
    
    #Make list of gene pairs and their interaction type
    gene_pairs, edge_types = identify_gene_pair(infile2)
    
    #Write header of outfile
    outfile.write("Gene1" + '\t' + "Gene2" + '\t' + "rho_1" + '\t' + "rho_2" + '\t' + "Edge type" + '\t' + "rho of interest" + '\n')
    
    #Identify correlations underlying each gene pair
    identify_cor(gene_pairs, edge_types, infile1, outfile)
    
    #Close files
    infile1.close()
    infile2.close()
    outfile.close()
    
