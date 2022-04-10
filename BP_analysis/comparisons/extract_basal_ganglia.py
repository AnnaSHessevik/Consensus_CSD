# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 14:35:18 2022

@author: annas
This script extract CSD links in the input data set which
matches the BP CSD network.
"""

import sys

if __name__ == '__main__':
    #Open file with BP CSD network
    infile1 = open("filtered_CSD_for_ganglia_comparison.txt")
    next(infile1) #skip first line
    
    #Make list with pairs of gene pairs in BP CSD
    gene_pairs = []
    for line in infile1:
        line_split = line.strip().split('\t')
        gene_pairs.append((line_split[0], line_split[1]))
        
    #Close infile1
    infile1.close()

    #Open file with basal ganglia information
    infile2 = open("CSD_basal_ganglia.txt")
    
    #Make new file which will contain the gene pairs from basal ganglia
    #that match the BP CSD network
    outfile = open("extracted_CSD_basal_ganglia.txt", "w")
    #write header to outfile
    outfile.write(infile2.readline())
    
    num_matches = 0
    
    #Extract the gene pairs from infile2 that are included in the BP CSD network
    for line in infile2:
        line_split = line.strip().split('\t')
        tested_genes = (line_split[0], line_split[1])
        if tested_genes in gene_pairs:
            outfile.write(line)
            num_matches += 1
            
    #Close files
    infile2.close()
    outfile.close()

    #Write total number of gene pairs in BP CSD network, and number of matches in basal ganglia    
    sys.stdout.write("Number of BP CSD links: " + str(len(gene_pairs)) + '\n')
    sys.stdout.write("Number of matches in basal ganglia: " + str(num_matches) + "\n")
