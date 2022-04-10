# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 09:59:43 2021

@author: annas
This script removes duplicate gene names in a gene expression file
"""

#Change input parameters here
data_file = open("control_GSE80655_gene_names.txt") #data set
outfile = open("control_preprocessed_GSE80655.txt", 'w') #name of output file


#--------------------------------------------------------------------#
#Create a dictionary where the keys correspond to gene names and 
#the values correspond to number of duplicates
#Note that header is also included. This is not a problem as the header only appear once
dict_duplicates = dict()

#Read each line in the file
for line in data_file:
    #Convert line to list of strings
    split_line = line.rstrip().split('\t')
    #First element in the line is the gene name
    gene_name = split_line[0]
    
    #Increase the value of the gene_name with 1 in the dictionary
    try:
        dict_duplicates[gene_name] += 1
    #If the gene name do not exist, create a new entity
    except:
        dict_duplicates[gene_name] = 1

#--------------------------------------------------------------------#
#Write the input expression file to an output file, but remove duplicated genes
data_file.seek(0,0) #Move to top of the input file

for line in data_file:
    #Convert line to list of strings
    split_line = line.rstrip().split('\t')
    
    #If the gene name appear more than once in the file, skip this line
    if dict_duplicates[split_line[0]] > 1:    
        continue
    
    outfile.write(line)

#--------------------------------------------------------------------#
#Close files
data_file.close()
outfile.close()
