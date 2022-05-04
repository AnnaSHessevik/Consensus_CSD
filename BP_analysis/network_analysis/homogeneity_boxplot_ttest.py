# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 16:27:39 2022

@author: annas
This script creates a boxplot of degree vs. node homeogenity of a
CSD network and calculate p-value of homogeneity difference between
hubs and intermediate genes.
"""

import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from scipy.stats import ttest_ind
from scipy.stats import spearmanr

if __name__ == '__main__':
    #open file
    infile = open("arithmetic_homogeneity.txt")
    max_degree = 49
    next(infile) #skip first line
    
    #Initialize dict
    data = dict()
    for i in range(1,max_degree+1):
        data[i] = []
    
    #Read degree and homogeneity from file
    for line in infile:
        line_split = line.rstrip().split('\t')
        degree = int(line_split[1])
        homogeneity = float(line_split[5])
        data[degree].append(homogeneity)

    #close file
    infile.close()
    
    #Make dictionary suitable for boxplot
    data = dict(sorted(data.items()))
    degrees, homogeneity = data.keys(), data.values()
    
    #Make boxplot
    #matplotlib.rc('xtick', labelsize=8) 
    #matplotlib.rc('ytick', labelsize=12)
    meanpointprop = dict(marker='D', markeredgecolor='black', markerfacecolor='firebrick')
    fig, ax = plt.subplots()
    bp = ax.boxplot(homogeneity, notch=False,patch_artist = True, showmeans=True, meanprops=meanpointprop)
    plt.xscale('log')
    plt.ylim(0.3,1.02)
    plt.xlim(0.8,55)
    
    formatter = ScalarFormatter()
    formatter.set_scientific(False)
    ax.xaxis.set_major_formatter(formatter)
    #plt.xticks(range(1, len(degrees)+1), degrees)
    plt.xticks([1,2,5,10,25,49])
    
    #colors = ["firebrick", "darkorange", "pink", "skyblue", "indigo", "lime"]
    for patch in bp['boxes']: 
        patch.set(color = "indigo")
        patch.set_facecolor("white")
        
    for element in ['whiskers', 'fliers', 'caps']:
        plt.setp(bp[element], color="indigo")
    plt.setp(bp["medians"], color="firebrick")
    
    ax.set_ylabel('Homogeneity', fontweight='bold', fontsize=14)
    ax.set_xlabel("Degree", fontweight='bold', fontsize=14)
    
    
    plt.savefig("homogeneity_boxplot.png", dpi=500, bbox_inches='tight')
    
    #T-test
    #Sort intermediate nodes and hubs in two groups
    h_hubs = []
    h_intermediate = []
    deg = 1
    
    for el in homogeneity:
        if deg > 2 and deg < 10: #intermediate degrees: 3-9
            for h in el:
                h_intermediate.append(h)
        elif deg > 9: #hubs
            for h in el:
                h_hubs.append(h)
        deg += 1
    
    p = ttest_ind(h_hubs, h_intermediate, alternative = "greater")
    print("p-value:", p)

    #Correlation between degree and homogeneity
    h_hubs_intermediate = []
    xs = []
    deg = 1
    
    for el in homogeneity:
        if deg > 2:
            for h in el:
                h_hubs_intermediate.append(h)
                xs.append(deg)
        deg += 1
    
    #Spearman rank correlation coefficients
    rho = spearmanr(h_hubs_intermediate, xs, alternative = "greater")
    print("Spearman rank correlation coefficeint:", rho)        
        
    