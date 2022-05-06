# -*- coding: utf-8 -*-
"""
Created on Fri Nov 19 11:49:44 2021

@author: annas

This script calculates the root mean square error between a
test data set and a reference data set
Arguments:
    1) Name of test data set
    2) "Y" if test data set has a header
    3) Column in test file which contain the parameter of interest
    (typically -1 or -2)
    4) Name of output file
     
"""

import sys
import math

def calculate_rmse(test_file, reference_file, col):
    
    
    rss = 0 #residual sum of squares
    n = 0 #number of data poits
    
    #Go through files and update rss and n
    for line1 in reference_file:
        line_ref = line1.rstrip().split('\t')

        if line_ref[0] == line_ref[1]: #Do not include self-correlations
            next(test_file)
            continue
        
        line2 = test_file.readline()
        line_test = line2.rstrip().split('\t')
        
        rss += (float(line_test[col]) - float(line_ref[2]))**2 
        n += 1
        
    return math.sqrt(rss/(float(n))) #root mean square error
        



if __name__ == '__main__':
    #Open files
    test_file = open(sys.argv[1])
    reference_file = open("spearman_not_sun_1000genes.txt")
    if sys.argv[2] == "Y":        
        next(test_file) #skip header
    
    #Define column of intreset
    col = int(sys.argv[3])
    
    
    #Calculate residual standard error
    rmse = calculate_rmse(test_file, reference_file, col)
    
    
    #Write RMSE to file
    outfile = open(sys.argv[4], 'a')
    outfile.write(sys.argv[1] + '\t' + str(rmse) + '\n')
    
    #Close files
    test_file.close()
    reference_file.close()
    outfile.close()
