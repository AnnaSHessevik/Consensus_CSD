# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 15:31:13 2021

@author: annas
This script finds common genes in the input datasets.
"""
from itertools import combinations

#Create a set with gene names from file
def set_of_genes(infile):
    #skip first line
    next(infile)
    
    #Read file line for line and add gene name to sest
    gene_set = set()
    for line in infile:
        line_split = line.rstrip().split('\t')
        gene_set.add(line_split[0])
    return gene_set

if __name__ == '__main__':
    #Open files
    infile_root = "bipolar_disorder_preprocessed_"
    accession_nr = ["GSE92538", "GSE80655", "GSE53987", "GSE12649", "GSE5388", "GSE120340"]
    infiles = []
    
    for nr in accession_nr:
        infiles.append(open(infile_root+nr+".txt"))
    
    #Define sets of genes
    gene_sets = []
    for infile in infiles:
        gene_sets.append(set_of_genes(infile))
    
    #Close files
    for infile in infiles:
        infile.close()
    
    #Find common genes (must be number of data sets is different from 6)
    common_genes = gene_sets[0].intersection(gene_sets[1], gene_sets[2], gene_sets[3], gene_sets[4], gene_sets[5])
    print("Common genes for all datasets:", len(common_genes))
    
    combos = combinations(range(6), 5)
    for el in combos:
        removed_pos = -10
        for i in range(0,6):
            if i not in el:
                removed_pos = i
        print("Common genes when", accession_nr[removed_pos], "is removed:", len(gene_sets[el[0]].intersection(gene_sets[el[1]], gene_sets[el[2]], gene_sets[el[3]], gene_sets[el[4]])))
    
    
    #Write genes to file
#    outfile = open("common_genes.txt", 'w')
#    for gene in common_genes:
#        outfile.write(gene + '\n')
#    outfile.close()
    
