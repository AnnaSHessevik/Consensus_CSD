# -*- coding: utf-8 -*-
"""
Created on Tue Jan 11 11:33:18 2022

@author: annas
This script creates a box plot for root mean square error for 
test data sets (combined and subsamples) relative to the reference data set.
"""


import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt

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
    
    labels = ["Subgroup\nsize 10-19", "Subgroup\nsize 20-29", "Subgroup\nsize 30-39", "Subgroup\nsize 40-49", "Transformed\naverage", "   Untransformed\naverage"]
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
    
    ax.set_ylabel('Root mean square error', fontweight='bold', fontsize=12)
    ax.set_xlabel("Method for estimating test correlation coefficients", fontweight='bold', fontsize=12)
    
    
    plt.savefig("boxplot_rmse.png", dpi=500, bbox_inches='tight')
    

if __name__ == '__main__':
    #Open files
    infiles = []
    infiles.append(open("rmse_subsample_size10-19.txt"))
    infiles.append(open("rmse_subsample_size20-29.txt"))
    infiles.append(open("rmse_subsample_size30-39.txt"))   
    infiles.append(open("rmse_subsample_size40-49.txt"))  
    infiles.append(open("rmse_fisher.txt"))
    infiles.append(open("rmse_arithmetic_average.txt"))    
    
    generate_boxplot(infiles)
    
    for infile in infiles:
        infile.close()
                    