# -*- coding: utf-8 -*-
"""
Created on Thu Jan 13 12:41:51 2022

@author: annas
This script removes the genes which have all expression values
equal to 0 in GSE80655 from the total list of common genes (for all datasets)
The final list of common genes are written to the file called 
final_common_genes.txt
"""

if __name__ == '__main__':
    #Open files
    infile1 = open("genes_zero_expression_GSE80655.txt")
    infile2 = open("common_genes.txt")
    outfile = open("final_common_genes.txt", 'w')
    
    #Convert infile1 to list of gene names
    remove_genes = []
    for line in infile1:
        line_split = line.rstrip().split('\t') #Not necessary but included to make sure the right format is used
        remove_genes.append(line_split[0])
        
    #Copy the list of common genes to new file, but exclude the genes in remove_genes
    for line in infile2:
        line_split = line.rstrip().split('\t') #Not necessary but included to make sure the right format is used
        if line_split[0] not in remove_genes:
            outfile.write(line)
    
    #Close the files
    infile1.close()
    infile2.close()
    outfile.close()
    

