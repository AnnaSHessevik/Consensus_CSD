# -*- coding: utf-8 -*-
"""
Created on Wed Sep 22 12:32:02 2021

@author: annas

This script find the sample size of a given gene expression file with 
the format somethingi_j.txt. j is the number of the subsampling of sampling round i
"""

import sys
import linecache
import re


#Make sure that meaningful arguments are given
def look_up_sample_size():
    if len(sys.argv) != 2:
        return '0'
        
    else:
        name_ExpData = sys.argv[1]
        name_split = name_ExpData.split('.')
        last_six = name_split[0][-6:] #get the last 6 characters
        split_last_six = last_six.split('_')
        #remove all non numeric characters and find line and row number
        line_number = int(re.sub('[^0-9]','',split_last_six[0])) #corresponds to sampling round
        row_number = int(re.sub('[^0-9]','',split_last_six[1])) - 1 #corresponds to the subsampling number (-1 to start at 0)
        
        #Read spesific line in sample size file
        read_line = linecache.getline("not_sun_1000genes_sample_sizes.txt", line_number)
        split_line = read_line.rstrip().split('\t')
        #Get the sample size of the spesific subsample
        sample_size = split_line[row_number]
        
        return sample_size

if __name__ == '__main__':
    sys.stdout.write(look_up_sample_size()+'\n')
    
    
