# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 11:47:03 2021

@author: annas
This script performs the paired Wilcoxon signed-rank test
"""

from scipy.stats import wilcoxon
from scipy.stats import mannwhitneyu

import matplotlib.pyplot as plt


def significance_test(infile, outfile):
    fisher = [] #initialize list
    arithmetric_average = [] #initialize list
    difference = []
    x=[i for i in range(1,101)]
    #Create lists from file
    for line in infile:
        line_split = line.rstrip().split('\t')
        fisher.append(float(line_split[1]))
        arithmetric_average.append(float(line_split[2]))
        difference.append(float(line_split[2])-float(line_split[1])) #arithmetic-fisher

    #Perform significance tests    
    w,p = wilcoxon(fisher, arithmetric_average)
    U1, p2 = mannwhitneyu(fisher, arithmetric_average)

    #Vizualization of scores in file
    plt.rcParams['font.size'] = '18' #Change font size
    plt.figure(0)
    plt.scatter(x,difference, c="firebrick")
    plt.ylim(min(difference),max(difference))
    #plt.ticklabel_format(style='plain')
    plt.xlim(0,100)
    plt.plot([0, 100], [0,0],linestyle='dashed', color = 'black')
    
    plt.xlabel("Simulation number", fontweight='bold')
    plt.ylabel("Pairwise difference", fontweight='bold')

    #plt.show()
    plt.savefig("wilcoxon_spearman.png", dpi=500, bbox_inches='tight')
    outfile.write("Fisher vs. real \tUntransformed average vs. real\t" + str(p) + '\n')
    
    plt.figure(1)
    plt.hist(difference, bins=20, color="firebrick")
    plt.xlabel("Pairwise difference", fontweight='bold')
    plt.ylabel("Frequency", fontweight='bold')
    plt.savefig("spearman_diff_distribution.png",dpi=500, bbox_inches='tight')
    

if __name__ == '__main__':
    #open files
    infile = open("comparison_correlation_of_correlations.txt")
    next(infile) #skip header
    outfile = open("significance_tests_correlations.txt", 'a')
    #Perform significance test
    significance_test(infile, outfile)
    #Close files
    infile.close()
    outfile.close()
