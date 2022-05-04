# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 14:02:09 2022

@author: annas
Modified version of plot_jaccards.py
This script creates a plot of Jaccard indexes relative to number of 
investigated gene pairs
"""
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt

def x_y(infile):
    x = []
    y = []
    #std = []
    for line in infile:
        line_split = line.rstrip().split('\t')
        x.append(int(line_split[0]))
        y.append(float(line_split[1]))
    return x,y

def generate_plot(infiles):
    fig, ax = plt.subplots()
    #Define labels and colors
    lab = ["BP", "Control"]
    i = 0
    col = ["indigo", "lime"]
    
    #Make plot for each file
    for infile in infiles: 
        x,y = x_y(infile)
        plt.plot(x,y, 'o--', markersize = 5, markeredgecolor ="black", linestyle = (0,(5,5)), markeredgewidth = 0.5, linewidth=1, color = col[i], label = lab[i])
        i += 1
    
    #Add labels, correct scale etc.
    plt.rcParams['font.size'] = '12' #Change font size
    ax.set_ylabel('Jaccard index', fontweight='bold')
    ax.set_xlabel("Number of investigated gene pairs", fontweight='bold')
    ax.set_xscale('log')
    plt.ylim((0,1))
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=2, fontsize = "medium", edgecolor = "gray")
    #Save figure
    plt.savefig("all_jaccards_BP.png", dpi=500, bbox_inches='tight')
    plt.show()


if __name__ == '__main__':
    #Open files
    infiles = []
    infiles.append(open("jaccard_fisher_BP.txt"))
    infiles.append(open("jaccard_arithmetic_BP.txt"))    
    
    #Make plot
    generate_plot(infiles)
    
    #Close files
    for infile in infiles:
        infile.close()
