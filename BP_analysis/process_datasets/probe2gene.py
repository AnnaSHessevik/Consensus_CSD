# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 09:25:39 2021

@author: annas
This script translates probes to gene names. 
A data set with probes and a file with probe to gene names 
should be provided. Position of the probe and gene names 
should also be specified.
"""

#Change input parameters here
data_file = open("control_GSE80655_probes.txt") #data set
probe2genes = open("probe2gene_GSE80655.txt") #File with probe and gene names
next(probe2genes) #skip header

pos_probe = 1 #position of probe names in probe2genes
pos_name = 0 #position of gene names in probe2genes

outfile = open("control_GSE80655_gene_names.txt", 'w') #name of output file

#Make a dictionary with probe names as keys and gene names as values
dict1 = dict()

for line in probe2genes:
    #Split line in the first infile
    split_line = line.rstrip().split('\t')
    #Make dictionary
    try:
        if "///" in split_line[pos_name]: #skip probes which correspond to more than one gene (spesific for GSE53987, GSE5388, GSE12649)
            continue
        if not split_line[pos_name] or not split_line[pos_probe]: #skip empty lines
            continue
        dict1[split_line[pos_probe]] = split_line[pos_name]
    except:
        continue


#Copy the first line in the data file to output file
outfile.write(data_file.readline())

#Translate probe ids in expression file to gene names
genes = list()
no_genes = list()
for line in data_file:
    #Split line in the expression file
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
        #probes without gene names are omitted
        
#Simple tests:
#Check if there are duplicates in the gene names
genes_set = set(genes)
if len(genes_set) < len(genes):
    print("There are duplicates in the list")
else:
    print("Thare are no duplicates")

if len(no_genes) > 0:
    print("Some probe ids miss gene names")
else:
    print("All probe ids have gene names")
    
data_file.close()
probe2genes.close()
outfile.close()

