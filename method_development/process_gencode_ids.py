# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 13:13:51 2021

@author: annas
This file process the gencode.v26.GRCh38.genes.gtf from GTEx Portal. A new file is
generated which contain the Gencode ID in the first row and the corresponding 
gene name in the second row. Only genes are included in the new file.
"""

infile = open("gencode.v26.GRCh38.genes.gtf")
outfile = open("gencode2gene_names.txt", 'w')

#skip the 5 first lines in the input file
for i in range(0,6):
    next(infile)
    
for line in infile:
    #Split line in the first infile
    split_line = line.rstrip().split('\t')
    
    #Ignore lines which do not specify genes (for intance exons)
    if split_line[2] != "gene":
        continue
    
    #Write Gencode ID to file and its corresponding gene name
    #Split attribute element in the current line
    attribute_split = split_line[8].split(';')
    #Write gene ID to output file
    outfile.write(attribute_split[0].split(' ')[1].replace('"', "") + '\t')
    #Write gene name to output file
    outfile.write(attribute_split[3].lstrip().split(' ')[1].replace('"', "") + '\n')
    
    
infile.close()
outfile.close()    
    
    
    