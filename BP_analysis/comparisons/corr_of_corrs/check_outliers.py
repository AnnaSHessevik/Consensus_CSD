# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 11:43:02 2022

@author: annas
This script identifies the outliers between combined correaltion
coefficients based on Fisher's Z transformed and weighted untransformed values.
"""

import sys

if __name__ == '__main__':
    #Open files
    infile1 = open("fisher_BP.txt")
    infile2 = open("arithmetic_BP.txt") 
    infile3 = open("combined_corr_BP.txt")
    next(infile3)
    #Create set with names of outlier genes
    genes = set()
    
    #Go through files
    for line1 in infile1:
        line_split1 = line1.rstrip().split('\t')
        if line_split1[0] == line_split1[1]: #Do not include self-correlations
            next(infile2)
            next(infile3)
            continue
        
        line2 = infile2.readline()
        line_split2 = line2.rstrip().split('\t')
        
        #Identify outliers and write to file
        if abs(float(line_split1[2]) - float(line_split2[2])) > 0.4:
            sys.stdout.write(line_split1[0] + " and " + line_split1[1] + '\n')
            sys.stdout.write(line_split1[2] + " and " + line_split2[2] + '\n')
            line3 = infile3.readline()
            sys.stdout.write(line3 + '\n')
            genes.add(line_split1[0])
            genes.add(line_split1[1])
        else:
            next(infile3)
            
    infile1.close()
    infile2.close()
    infile3.close()
    
    #Look spesifically at gene expression of identified genes in GSE80655
    sys.stdout.write("Gene expression in GSE80655: \n")        
    infile4 = open("sorted_CSD_bipolar_disorder_GSE80655.txt")
    for line in infile4:
        line_split = line.rstrip().split('\t')
        if line_split[0] in genes:
            sys.stdout.write(line)
    infile4.close()

