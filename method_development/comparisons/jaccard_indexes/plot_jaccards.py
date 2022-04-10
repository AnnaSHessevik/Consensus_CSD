# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 17:20:16 2021

@author: annas
This script creates a plot of Jaccard indexes relative to number of 
investigated gene pairs
"""
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt

def x_y_std(infile):
    x = []
    y = []
    std = []
    for line in infile:
        line_split = line.rstrip().split('\t')
        x.append(int(line_split[0]))
        y.append(float(line_split[1]))
        std.append(float(line_split[2]))
    return x,y,std

def generate_plot(infiles):
    fig, ax = plt.subplots()
    #Define labels and colors
    lab = ["Subsample \nsize 10-19", "Subsample \nsize 20-29", "Subsample \nsize 30-39", 
           "Subsample \nsize 40-49", "Transformed \naverage", "Untransformed \naverage"]
    i = 0
    col = ["firebrick", "darkorange", "pink", "skyblue", "indigo", "lime"]
    
    #Make plot for each file, include errors
    for infile in infiles: 
        x,y,std = x_y_std(infile)
        ax.errorbar(x, y, yerr=std, fmt='o--',markersize = 5, markeredgecolor ="black", linestyle = (0,(5,5)), markeredgewidth = 0.5, linewidth=1, capsize = 3, color = col[i], label = lab[i])
        i += 1
    
    #Add labels, correct scale etc.
    ax.set_ylabel('Jaccard index', fontweight='bold')
    ax.set_xlabel("Number of investigated gene pairs", fontweight='bold')
    ax.set_xscale('log')
    plt.ylim((0,1))
    plt.xlim(1, 1000000)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.27), ncol=3, fontsize = "small", edgecolor = "gray")
    #Save figure
    plt.savefig("all_jaccards.png", dpi=500, bbox_inches='tight')
    plt.show()


if __name__ == '__main__':
    #Open files
    infiles = []
    infiles.append(open("summary_jaccards_subsample_size10-19.txt"))
    infiles.append(open("summary_jaccards_subsample_size20-29.txt"))
    infiles.append(open("summary_jaccards_subsample_size30-39.txt"))   
    infiles.append(open("summary_jaccards_subsample_size40-49.txt"))  
    infiles.append(open("summary_fisher_jaccards.txt"))
    infiles.append(open("summary_arithmetic_jaccards.txt"))    
    
    #Make plot
    generate_plot(infiles)
    
    #Close files
    for infile in infiles:
        infile.close()
