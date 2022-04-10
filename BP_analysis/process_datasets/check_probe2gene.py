# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 12:01:02 2021

@author: annas
This script checks probe2gene files to make sure that each probe is just
listed once.
"""

probe2genes = open("entrez2name.txt") #File with probe and gene names
next(probe2genes) #skip header
infile = "bipolar_disorder_GSE120340_entrez.txt"
outfile = "bipolar_disorder_GSE120340_entrez_no_ambiguity.txt"

pos_probe = 1 #position of probe names in probe2genes
pos_name = 0 #positiob of gene names in probe2genes

list_probes = []

for line in probe2genes:
    #Split line in the first infile
    split_line = line.rstrip().split('\t')
    #Make list
    try: 
        if split_line[pos_probe] and split_line[pos_name]:
            list_probes.append(split_line[pos_probe])
    except:
        continue
    
set_probes = set(list_probes)

if (len(set_probes) == len(list_probes)):
    print("No duplicates of probes")
    
else:
    print("Problem: some probes are duplicated")
    duplicate = []
    for el in list_probes:
        if list_probes.count(el) > 1:
            duplicate.append(el)
    
    data = open(infile)
    data_out = open(outfile, 'w')
    count = 0
    for line in data:
        split_line = line.rstrip().split('\t')
        if split_line[0] in duplicate:
            count += 1
            continue
        else:
            data_out.write(line)
    data.close()
    data_out.close()        
    print("The file contains", count, "ambiguity probes")
    
probe2genes.close()
