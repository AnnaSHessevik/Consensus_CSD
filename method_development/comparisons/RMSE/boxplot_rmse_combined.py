# -*- coding: utf-8 -*-
"""
Created on Tue Jan 11 16:48:19 2022

@author: annas


This script creates a box plot for root mean square error for 
combined data sets (fisher and arithmetic average) relative to the reference data set.
"""


import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys
from scipy.stats import wilcoxon

def write_list(infile):
    liste = []
    for line in infile:
        line_split = line.rstrip().split('\t')
        liste.append(float(line_split[1]))
    return liste

def generate_boxplot(infiles):
    data = []
    for infile in infiles:
        data.append(write_list(infile))
    
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
    
    ax.set_ylabel('RMSE', fontweight='bold', fontsize=24)
    ax.set_xlabel("Test method", fontweight='bold', fontsize=24)
    
    plt.savefig("boxplot_rmse_combined.png", dpi=500, bbox_inches='tight')
    plt.show()

    #Significance test
    w,p = wilcoxon(data[0], data[1])
    sys.stdout.write(str(p) + '\n')


if __name__ == '__main__':
    #Open files
    infiles = []  
    infiles.append(open("rmse_fisher.txt"))
    infiles.append(open("rmse_arithmetic_average.txt"))    
    
    generate_boxplot(infiles)
    
    for infile in infiles:
        infile.close()