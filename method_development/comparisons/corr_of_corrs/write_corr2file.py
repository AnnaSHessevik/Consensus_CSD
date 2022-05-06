# -*- coding: utf-8 -*-
"""
Created on Sun Oct  3 16:33:10 2021

@author: annas

This script writes the correlation of correlation (reference vs. subgorup) to a file.
The chosen file is dependent on the subsample size of the origial file 
where the correlation was calculated.
Arguments:
    1) Name of input file from which the correlation was calculated
    2) The correlation coefficient
    3) The sample size of the subsample
"""

import sys

def write_corr2file(input_filename, corr, outfile):
    f = open(outfile, 'a')
    f.write('\n' + input_filename + '\t' + corr)
    f.close()

if __name__ == '__main__':
    input_filename = sys.argv[1]
    corr = sys.argv[2]
    sample_size = int(sys.argv[3])
    
    if sample_size >= 10 and sample_size < 20:
        outfile = "correlation_subsamples10-19.txt"
    
    elif sample_size >= 20 and sample_size < 30:
        outfile = "correlation_subsamples20-29.txt"

    elif sample_size >= 30 and sample_size < 40:
        outfile = "correlation_subsamples30-39.txt"
        
    elif sample_size >= 40 and sample_size < 50:
        outfile = "correlation_subsamples40-49.txt"
    
    else:
        outfile = "correlations_not_included.txt"
    
    write_corr2file(input_filename, corr, outfile)
    
