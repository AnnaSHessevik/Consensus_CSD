# -*- coding: utf-8 -*-
"""
Created on Wed Oct 27 14:43:39 2021

@author: annas
This script creates two data sets with control or case (biploar 
disorder) samples from the GSE80655.
"""
#Open input files
raw_data = open("GSE80655_normalized_counts.txt")
mapping_file = open("mapping_GSE80655.txt")

#Output files
bp_file = open("bipolar_disorder_GSE80655_probes.txt", 'w')
control_file = open("control_GSE80655_probes.txt", 'w')

#Get a list of IDs corresponding to bipolar disorder and control
bp = set()
control = set()

for line in mapping_file:
    line_split = line.rstrip().split('\t')
    id_and_disorder = line_split[1].split('_')
    if (id_and_disorder[1] == "DLPFC" and id_and_disorder[2] == "B"):
        bp.add(id_and_disorder[-1])
    elif (id_and_disorder[1] == "DLPFC" and id_and_disorder[2] == "C"):
        control.add(id_and_disorder[-1])

#Get a list of indexes for IDs corresponding to bipolar disorder and control
i = 0 #counter
bp_index = []
control_index = []

#First line contains sample IDs
ids = raw_data.readline().rstrip().split('\t')


for word in ids:
    if word in bp:
        bp_index.append(i)
    elif word in control:
        control_index.append(i)

    i += 1        

#Write output to files
raw_data.seek(0, 0) #Move to top of the input file


for line in raw_data:
    line_split = line.rstrip().split('\t')
    #Always write gene name/probe to file
    bp_file.write(line_split[0])
    control_file.write(line_split[0])
    
    #write spesific gene expressions to files
    for pos in bp_index:
        bp_file.write('\t'+line_split[pos])
    bp_file.write('\n')
        
    for pos in control_index:
        control_file.write('\t'+line_split[pos])
    control_file.write('\n')
    

mapping_file.close()
raw_data.close()
bp_file.close()
control_file.close()


