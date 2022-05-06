# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 14:02:35 2021

@author: annas
This script removes negative signs in a spesified column in an input file
and writes the result to an output file.
In addition, this script removes self-correlations

Arguments:
    1) Input filename
    2) Column where - should be removed (NB: starts at 0) (last column = -1)
    3) Output filename
"""
import sys

def transform_data(infile, col, outfile):
    for line in infile:
        line_split = line.rstrip().split('\t')
        if line_split[0] == line_split[1]: #skip self-correlations
            continue
        if "-" in line_split[col][0]: #remove - sign
            line_split[col] = line_split[col][1:]
        
        #if "combined" in sys.argv[1] and not "copy" in sys.argv[1]: #New file in combined files only contain averages based on fisher and arithmetric average
        #    line_split = [line_split[0], line_split[1], line_split[-2], line_split[-1]]
        
        for word in line_split:
            outfile.write(word + '\t')
        outfile.write('\n')


if __name__ == '__main__':
    #Input file
    infile = open(sys.argv[1])
    col = int(sys.argv[2])
    outfile = open(sys.argv[3], 'w')
    #if "combined" in sys.argv[1] and not "copy" in sys.argv[1]:
    #    next(infile) #skip first line in infile (header)
    transform_data(infile, col, outfile)
    infile.close()
    outfile.close()
