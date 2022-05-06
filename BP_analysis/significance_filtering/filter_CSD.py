# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 10:28:22 2022

@author: annas
This script excludes insignificant gene pairs from the CSD network.
"""
def make_list(infile):
    gene_pairs = [] #list with significant gene pairs
    
    #Read lines in file and write gene pair to list
    for line in infile:
        split_line = line.rstrip().split('\t') #split the line
        gene_pairs.append((split_line[0].rstrip(), split_line[1].rstrip()))

    return gene_pairs        

def write_significant_pairs(infile, gene_pairs, outfile):
    for line in infile:
      split_line = line.rstrip().split('\t') #split the line
      
      #Write significant gene pairs to outfile
      if (split_line[0].rstrip(), split_line[1].rstrip()) in gene_pairs:
          outfile.write(line)

if __name__ == '__main__':
    #Open files
    infile1 = open("fisher_CSDSelection_10000.txt")
    infile2 = open("fisher_significant_gene_pairs.txt")
    next(infile2) #skip header
    outfile = open("filtered_fisher_CSDSelection_10000.txt", "w")
    
    #Make list of gene pairs from infile2 (significant gene pairs)
    gene_pairs = make_list(infile2)
    
    #Filter out insignificant gene pairs from infile1 and write significant gene pairs to the outfile
    write_significant_pairs(infile1, gene_pairs, outfile)
    
    #Close files
    infile1.close()
    infile2.close()
    outfile.close()
    
    
