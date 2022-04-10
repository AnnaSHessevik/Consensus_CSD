# -*- coding: utf-8 -*-
"""

@author: annas
This script performs the paired Wilcoxon signed-rank test for RMSE.
Modified version of mann_witney_wilcoxon.py
"""

from scipy.stats import wilcoxon
#from scipy.stats import mannwhitneyu

import matplotlib.pyplot as plt


def significance_test(infile1, infile2, outfile):
    fisher = [] #initialize list
    arithmetric_average = [] #initialize list
    difference = []
    x=[i for i in range(1,101)]
    
    #Create lists from file
    for line1 in infile1:
        line1_split = line1.rstrip().split('\t')
        fisher.append(float(line1_split[1]))
        
        line2 = infile2.readline()
        line2_split = line2.rstrip().split('\t')
        arithmetric_average.append(float(line2_split[1]))
        
        difference.append(float(line2_split[1])-float(line1_split[1]))

    #Perform significance tests    
    w,p = wilcoxon(fisher, arithmetric_average)
   # U1, p2 = mannwhitneyu(fisher, arithmetric_average) #unpaired test

    #Vizualization of scores in file
    plt.rcParams['font.size'] = '18' #Change font size
    plt.figure(0)
    plt.scatter(x, difference, c="firebrick")
    plt.ylim(min(difference),max(difference))
    plt.xlim(0,101)
    plt.ylim(min(difference)-0.0001, max(difference))
    plt.ticklabel_format(style='scientific', scilimits=[-4,6])    
    plt.xlabel("Simulation number", fontweight='bold')
    plt.ylabel("Pairwise difference", fontweight='bold')

   
    plt.savefig("wilcoxon_rmse.png", dpi=500, bbox_inches='tight')
    #outfile.write("Fisher vs. real \tUntransformed average vs. real\t" + str(p) + '\n')

    plt.figure(1)
    plt.ticklabel_format(style='scientific', scilimits=[-2,6]) 
    plt.hist(difference, bins=20, color="firebrick")
    plt.xlabel("Pairwise difference", fontweight='bold')
    plt.ylabel("Frequency", fontweight='bold')
    plt.savefig("rmse_differences_distribution.png",dpi=500, bbox_inches='tight')
    
if __name__ == '__main__':
    #open files
    infile1 = open("rmse_fisher.txt")
    infile2 = open("rmse_arithmetic_average.txt")
   
    outfile = open("significance_tests_rmse_fisher_vs_arithmetic.txt", 'w')
    #Perform significance test
    significance_test(infile1, infile2, outfile)
    #Close files
    infile1.close()
    infile2.close()
    outfile.close()
