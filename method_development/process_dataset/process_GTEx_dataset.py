# -*- coding: utf-8 -*-
"""
Created on Wed Aug 25 16:27:12 2021

@author: annas

This script converts the data sets downloaded from GTEx Portal to data sets 
suitable for CSD analysis
"""

#Open files
in_file = open("Skin_Sun_Exposed.bed")
out_file = open("Formated_Skin_Sun_Exposed.txt", 'w')

#Remove the first three rows in in_files
for line in in_file:
    #Convert line to list of strings
    split_line = line.rstrip().split('\t') #Split the line
    for i in range(3,len(split_line)): #Count from element number 3.
        if i != (len(split_line)-1):
            out_file.write(split_line[i] + '\t')
        else:
            out_file.write(split_line[i] + '\n')
    
#Close files
in_file.close()
out_file.close()

