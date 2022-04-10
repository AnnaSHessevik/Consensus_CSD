# -*- coding: utf-8 -*-
"""
Created on Thu Jan 13 12:26:21 2022

@author: annas

This script identifies the number and name of genes with 
all gene expressions equal to 0 in the data set GSE80655. 
The gene names are written to a file called genes_zero_expression.txt"""

def identify_zeros(infile):
    gene_names = []
    num_genes = 0
    for line in infile: #Read lines in file
        line_split = line.rstrip().split('\t')
        not_zero = True
        first_element = True
        #Check each element in the line and investigate if all elements are equal to 0
        for el in line_split:
            if first_element:
                first_element = False
                gene_name = el
                continue
            if float(el) != 0:
                not_zero = True
                break
            else:
                not_zero = False
        #If all elements in the line are 0, register this gene
        if not_zero == False:
            num_genes += 1
            gene_names.append(gene_name)

    print("Number of genes with all expression values equal to", 0, "is", num_genes)

    return gene_names


if __name__ == '__main__':
    #Open files
    infile1 = open("almost_CSD_bipolar_disorder_GSE80655.txt") #open file
    infile2 = open("almost_CSD_control_GSE80655.txt") #open file
    next(infile1) #skip header
    next(infile2) #skip header

    #Identify genes with all gene expression values equal to 0
    gene_names1 = set(identify_zeros(infile1))
    gene_names2 = set(identify_zeros(infile2))

    #Find total number of genes were all gene expression values are equal to 0 in at least one condition
    common_genes = gene_names1.union(gene_names2)

    #Display the findings
    for el in common_genes:
        print(el)

    print("Total number of genes where all expression values are 0:", len(common_genes))

	#Close the files
    infile1.close()
    infile2.close()
    
    #Write the gene names to file
    outfile = open("genes_zero_expression_GSE80655.txt", 'w')
    for gene in common_genes:
        outfile.write(gene + "\n")
        
    outfile.close()
    

