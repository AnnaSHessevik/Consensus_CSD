# -*- coding: utf-8 -*-
"""
Created on Fri Oct  1 15:15:08 2021

@author: annas
This script creates a box plot for correlations of correlations.
The boxes correspond to correlations of correlations calculated for
subsamples with different sample sizes and the combined scores.
"""

import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt


def write_list(infile):
    liste = []
    next(infile)
    for line in infile:
        line_split = line.rstrip().split('\t')
        liste.append(float(line_split[1]))
    return liste
        

def generate_box_plot(infile, infile2, infile3, infile4, infile5):
    #Create list with correlations of correlations from combined scores
    fisher = [] #initialize list
    untransformed_average = [] #initialize list
    for line in infile:
        line_split = line.rstrip().split('\t')
        fisher.append(float(line_split[1]))
        untransformed_average.append(float(line_split[2]))
    
    #Create list with correlations of correlations from subsamples
    spearman10 = write_list(infile2)
    spearman20 = write_list(infile3)
    spearman30 = write_list(infile4)
    spearman40 = write_list(infile5)
                
    data = [spearman10, spearman20, spearman30, spearman40,fisher, untransformed_average]
    labels = ["Subgroup\nsize 10-19", "Subgroup\nsize 20-29", "Subgroup\nsize 30-39", "Subgroup\nsize 40-49", "Transformed \naverage", "   Untransformed \naverage"]
    
    matplotlib.rc('xtick', labelsize=8) 
    matplotlib.rc('ytick', labelsize=12)
    
    fig, ax = plt.subplots()
    bp = ax.boxplot(data, notch=True, labels=labels,patch_artist = True)
    
    colors = ["firebrick", "darkorange", "pink", "skyblue", "indigo", "lime"]
    for patch, color in zip(bp['boxes'], colors): 
        patch.set(color = "black")
        patch.set_facecolor(color)
        
    for element in ['whiskers', 'fliers', 'means', 'medians', 'caps']:
        plt.setp(bp[element], color="black")
    
    ax.set_ylabel('Spearman rank correlation \nof test and reference correlation', fontweight='bold', fontsize=12)
    ax.set_xlabel("Method for estimating test correlation coefficients", fontweight='bold', fontsize=12)
    
    plt.ylim((0.3,1.02))
    
    plt.savefig("boxplot_all_corr2corr.png", dpi=500, bbox_inches='tight')
    #plt.show()
    
if __name__ == '__main__':
    infile = open("comparison_correlation_of_correlations.txt")
    next(infile) #skip first line
    infile2 = open("correlation_subsamples10-19.txt")
    infile3 = open("correlation_subsamples20-29.txt")
    infile4 = open("correlation_subsamples30-39.txt")
    infile5 = open("correlation_subsamples40-49.txt")
    
    
    generate_box_plot(infile, infile2, infile3, infile4, infile5)
    
    infile.close()
    infile2.close()
    infile3.close()
    infile4.close()
    infile5.close()



