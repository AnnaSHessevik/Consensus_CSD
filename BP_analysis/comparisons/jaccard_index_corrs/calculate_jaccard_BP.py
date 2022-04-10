# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 15:43:28 2021

@author: annas
This script calculates the Jaccard index of an input file relative to
a file with "correct" correlations.
NB: input files must be sorted beforehand. This is performed directly in 
the command line in my code (see jaccard_combined.sh).
Arguments:
    1) Sorted file with "correct" correlations (sorted based on correlation coefficients)
    2) Sorted file with estimated correlations (sorted based on correlation coefficients).
    First line must be removed.
    3) Top n gene pairs that will be investigated
    4) Output filename, for instance jaccard_fisher.txt or jaccard_arithmetric_average.txt
"""
import sys


def make_list(infile,n): #Make a list of top n gene pairs in input file
    gene_pairs = []
    for i in range(0,n):
        line = infile.readline()
        line_split = line.rstrip().split('\t')
        gene_pairs.append(line_split[0]+"+"+line_split[1])
    return gene_pairs

#Calculate Jaccard index        
def jaccard(correct_pairs, estimated_pairs):
    intersection = len(list(set(correct_pairs).intersection(estimated_pairs)))
    union = (len(correct_pairs) + len(estimated_pairs)) - intersection
    return float(intersection) / union

#Write Jaccard index to file
def write_jaccard(jaccard_index, n, outfile_name):
    outfile = open(outfile_name, 'a')
    outfile.write(str(n) +'\t'+str(jaccard_index)+'\n') #slight modification from original script
    outfile.close()


if __name__ == '__main__':
    #File with correct correlations between gene pairs
    correct_corr = open(sys.argv[1])
    #File with estimated correlations between gene pairs
    estimated_corr = open(sys.argv[2])
    #Number of gene pairs which will be investigated
    n = int(sys.argv[3])
    
    #Make lists of top n gene pairs in the input files
    correct_pairs = make_list(correct_corr, n)
    estimated_pairs = make_list(estimated_corr, n)
    
    #Close the input files
    correct_corr.close()
    estimated_corr.close()
    
    #Calculate jaccard index
    jaccard_index = jaccard(correct_pairs, estimated_pairs)
    
    #Write jaccard index to appropiate file
    outfile_name = sys.argv[4] #+ ".txt" #slight modification from original script
    write_jaccard(jaccard_index, n, outfile_name)
    
    
    
    
    
