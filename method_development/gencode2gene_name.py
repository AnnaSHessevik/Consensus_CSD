# -*- coding: utf-8 -*-
"""
Created on Fri Sep 10 12:58:11 2021

@author: annas
Checked for duplicates and missing identifiers in data set.
Generates a file where Gencode IDs are translated to gene names, otherwise equal to input data set.
"""

infile1 = open("gencode2gene_names.txt")
infile2 = open("Formated_Skin_Sun_Exposed.txt")
outfile = open("gene_names_sun.txt", 'w')

#Make a dictionary with gencodes as keys and gene names as values
dict1 = dict()

for line in infile1:
    #Split line in the first infile
    split_line = line.rstrip().split('\t')
    #Make dictionary
    dict1[split_line[0]] = split_line[1]

#Copy the first line in the infile2 to the output file
outfile.write(infile2.readline())

#Translate gencode ids in expression file to gene names
genes = list()
no_genes = list()

for line in infile2:
    #Split line in the first infile
    split_line = line.rstrip().split('\t')
    
    #Convert to gene name
    try:
        genes.append(dict1[split_line[0]]) #Add to list
        outfile.write(dict1[split_line[0]]) #write to output file
        #copy remaining of input line to output file
        for i in split_line:
            if i == split_line[0]:
                continue
            outfile.write('\t' + i)
        outfile.write('\n')
        
    except:
        no_genes.append(split_line[0])
        #not write Gencode IDs without gene names to output file
    

#Check if there are duplicates in the gene names
genes_set = set(genes)
if len(genes_set) < len(genes):
    print("There are", len(genes)-len(genes_set), "duplicates in the list")
else:
    print("Thare are no duplicates")

if len(no_genes) > 0:
    print(len(no_genes), "GenCode ids miss gene names")
else:
    print("All GenCode ids have gene names")
    
infile1.close()
infile2.close()
outfile.close()


