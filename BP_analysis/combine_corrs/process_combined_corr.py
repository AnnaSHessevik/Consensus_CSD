# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 15:17:49 2021

@author: annas
This script processes output from improved_fisher_transformation.py to
a readable format for subsequent CSD analysis.
"""

if __name__ == '__main__':
    #Open files
    infile = open("combined_corr_ctrl.txt")
    next(infile)
    outfile1 = open("fisher_ctrl.txt", 'w')
    outfile2 = open("arithmetic_ctrl.txt", 'w')
    
    #Copy gene names and combined correlations to files
    for line in infile:
        line_split = line.rstrip().split('\t')
        outfile1.write(line_split[0] + '\t' + line_split[1] + '\t' + line_split[-2] + '\t' + '0' + '\n')
        outfile2.write(line_split[0] + '\t' + line_split[1] + '\t' + line_split[-1] + '\t' + '0' + '\n')
    
    #Close files
    infile.close()
    outfile1.close()
    outfile2.close()
