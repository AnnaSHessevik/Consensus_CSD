# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 14:45:26 2021

@author: annas
This script calculates mean and standard deviation of an input file
with jaccard indexes (in column 2)
Arguments:
    1) Name of input file (no header)
    2) Number of investigated gene pairs
    2) Name of output file
"""
import sys
import statistics

def mean_and_std(infile, num_pairs, outfile):
    jaccards = []
    #Make list with jaccard indexes
    for line in infile:
        line_split = line.rstrip().split('\t')
        jaccards.append(float(line_split[1]))
    
    #Calculate mean
    mean_jaccard = statistics.mean(jaccards)
    #Calulate (sample) standard deviation
    std_jaccards = statistics.stdev(jaccards, mean_jaccard)
    
    #Write results to file
    outfile.write(num_pairs + '\t' + str(mean_jaccard) + '\t' + str(std_jaccards) +'\n')



if __name__ == '__main__':
    #File with jaccard indexes
    infile = open(sys.argv[1])
    num_pairs = sys.argv[2]
    outfile = open(sys.argv[3], 'a')
    
    #Calculate mean and standard deviation and write these to file
    mean_and_std(infile, num_pairs, outfile)
    
    #Close files
    infile.close()
    outfile.close()
