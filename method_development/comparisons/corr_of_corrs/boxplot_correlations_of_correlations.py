# -*- coding: utf-8 -*-
"""
Created on Fri Oct  1 15:15:08 2021

@author: annas
This scripts create a box plot for correlations of correlations.
"""

import sys
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import statistics

def generate_box_plot(infile):
    fisher = [] #initialize list
    untransformed_average = [] #initialize list
    
    for line in infile:
        line_split = line.rstrip().split('\t')
        fisher.append(float(line_split[1]))
        untransformed_average.append(float(line_split[2]))
    
    median_fisher = statistics.median(fisher)
    sys.stdout.write("Median value of Fisher's Z transformed averages: "+ str(median_fisher)+ ".\n")
    median_untransformed = statistics.median(untransformed_average) 
    sys.stdout.write("Median value of utransformed averages: "+ str(median_untransformed)+ ".\n")
    
    data = [fisher, untransformed_average]
    labels = ["Transformed average", "Untransformed average"]
    
    matplotlib.rc('xtick', labelsize=20) 
    matplotlib.rc('ytick', labelsize=21)
    
    fig, ax = plt.subplots(figsize=(12,6.86))
    bp = ax.boxplot(data, notch=True, labels=labels,patch_artist = True)
    
    colors = ["indigo", "lime"]
    for patch, color in zip(bp['boxes'], colors): 
        patch.set(color = "black", linewidth=1.5)
        patch.set_facecolor(color)
        
    for element in ['whiskers', 'fliers', 'means', 'medians', 'caps']:
        plt.setp(bp[element], color="black", linewidth=1.5)
    plt.setp(bp['whiskers'], linestyle = '-')
    
    ax.set_ylabel('Correlation of correlations', fontweight='bold', fontsize=24)
    ax.set_xlabel("Test method", fontweight='bold', fontsize=24)
    
    
    plt.savefig("boxplot_correlation_of_correlations.png", dpi=500, bbox_inches='tight')
    plt.show()

if __name__ == '__main__':
    infile = open("comparison_correlation_of_correlations.txt")
    next(infile) #skip first line
    generate_box_plot(infile)
    infile.close()
