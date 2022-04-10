# -*- coding: utf-8 -*-
"""
Created on Wed Sep 22 12:32:02 2021

@author: annas

This script find the sample size of a given gene expression file with 
the format something_GEOx.txt, where x correspond to the GEO accession number. 
Arguments:
    1) Name of data set with expression values
    2) BP or ctrl depending on whether the bipolar disorder or control
    samples are analysed.
"""

import sys
import linecache
import re


#Make sure that meaningful arguments are given
def look_up_sample_size():
    if len(sys.argv) != 3:
        return '0'
        
    else:
        #Isolate the accession number from the file name
        name_ExpData = sys.argv[1]
        name_split = name_ExpData.split('.')
        name_split2 = name_split[0].split('_')
        geo_nr = name_split2[-1]
        
        #Define if we are interested in bipolar disorder or control samples
        BP_or_ctrl = sys.argv[2]
        sample_sizes = open("sample_sizes_" + BP_or_ctrl + ".txt")
        
        #Find sample size from accession number
        sample_size = '0'
        for line in sample_sizes:
            split_line = line.rstrip().split('\t')
            if split_line[0] == geo_nr:
                sample_size = split_line[1]

        return sample_size

if __name__ == '__main__':
    sys.stdout.write(look_up_sample_size()+'\n')
    
    
