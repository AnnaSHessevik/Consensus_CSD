# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 14:02:09 2022

@author: annas
Modified version of plot_jaccards.py
This script creates a plot of Jaccard indexes relative to number of 
investigated gene pairs
"""
#import matplotlib
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
    fig, ax = plt.subplots(figsize=(7,4))
    #Define labels and colors
    lab = ["GSE92538", "GSE80655", "GSE53987", "GSE5388", "GSE12649", "GSE120340", "Transformed"] #Remember to change depeding on wanted plot
    i = 0
    col = ["firebrick", "darkorange", "pink", "skyblue", "forestgreen", "magenta", "indigo"]
    
    #Make plot for each file
    for infile in infiles: 
        x,y = x_y(infile)
        plt.plot(x,y, 'o--', markersize = 5, markeredgecolor ="black", linestyle = (0,(5,5)), markeredgewidth = 0.5, linewidth=1, color = col[i], label = lab[i])
        i += 1
    
    #Add labels, correct scale etc.
    ax.set_ylabel('Jaccard index', fontweight='bold', fontsize=13)
    ax.set_xlabel("Number of investigated gene pairs", fontweight='bold', fontsize=13)
    ax.set_xscale('log')
    plt.xticks(fontsize=13)
    plt.yticks(fontsize=13)
    plt.ylim((0,1))
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.24), ncol=4, fontsize = "11", edgecolor = "gray")
    plt.xlim((1,10000000))
	#Save figure
    plt.savefig("jaccards_arithmetic_BP.png", dpi=500, bbox_inches='tight')
    plt.show()


if __name__ == '__main__':
    #Open files
    infiles = []
    #Open file with Jaccard indexes for combined values vs. subsamples
    geo = ["GSE92538", "GSE80655", "GSE53987", "GSE5388", "GSE12649", "GSE120340"]
    for nr in geo:
        filename = "jaccard_arithmetic_vs_spearman_BP_" + nr + ".txt" #remember to change fisher and BP depending on wanted plot
        infiles.append(open(filename))
    infiles.append(open("jaccard_BP.txt")) #Fisher's Z vs arithmetic   
    
    #Make plot
    generate_plot(infiles)
    
    #Close files
    for infile in infiles:
        infile.close()
