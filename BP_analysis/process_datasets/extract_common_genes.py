# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 10:20:27 2021

@author: annas
This scripts read expression files and a file with common genes and write 
new expression files which only include the common genes.
"""



if __name__ == '__main__':
    #Open files
    infile_root = "almost_CSD_bipolar_disorder_"
    outfile_root = "CSD_bipolar_disorder_"
    accession_nr = ["GSE80655"] #["GSE92538", "GSE80655", "GSE53987", "GSE12649", "GSE5388", "GSE120340"]
    infiles = []
    outfiles = []
    
    for nr in accession_nr:
        infiles.append(infile_root+nr+".txt")
        outfiles.append(outfile_root+nr+".txt")
        
    f_common = open("final_common_genes.txt")
    
    #Write common genes to a list
    common_genes = set()
    for line in f_common:
        line_split = line.rstrip().split('\t')
        common_genes.add(line_split[0])
    
    f_common.close()
    
    #Extract common genes from expression files and write corresponding gene
    #expressions to a new file
    for i in range(0,len(infiles)):
        working_infile = open(infiles[i])
        working_outfile = open(outfiles[i], 'w')
        
        #Write first line from infile to outfile
        working_outfile.write(working_infile.readline())
        
        #Write subsequent lines in infile to outfile if the genes are common for
        #all expression files
        for line in working_infile:
            line_split = line.rstrip().split('\t')
            if line_split[0] in common_genes:
                working_outfile.write(line)
        
        #Close files
        working_infile.close()
        working_outfile.close()
    
    
