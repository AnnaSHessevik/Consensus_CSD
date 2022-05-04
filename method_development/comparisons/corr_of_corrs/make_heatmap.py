# -*- coding: utf-8 -*-
"""
Created on Sun Oct  3 15:06:56 2021

@author: annas
This script creates a heatmap as an alternative to scatter plots for
visualization of combined vs. "true" Spearman rank correlation coefficients
Arguments:
    1) Repitition number
"""

import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from scipy import stats

def make_heatmap(correct_corr):
    #Input argument is the name of a file with estimated correlations
    estimated_corr = open("combined_spearman_not_sun"+sys.argv[1]+".txt")
    next(estimated_corr)
    
    #Make lists with correlations
    correct_corr_list = []
    fisher = []
    arithmetic_average = []
    
    for line1 in correct_corr:
        line_split1 = line1.rstrip().split('\t')
        if line_split1[0] == line_split1[1]: #Do not include self-correlations
            next(estimated_corr)
            continue
        correct_corr_list.append(float(line_split1[2]))            
        
        line2 = estimated_corr.readline()
        line_split2 = line2.rstrip().split('\t')
        fisher.append(float(line_split2[-2]))
        arithmetic_average.append(float(line_split2[-1]))
    
    estimated_corr.close()

    spearman_fisher = stats.spearmanr(correct_corr_list, fisher)
    spearman_arithmetic = stats.spearmanr(correct_corr_list, arithmetic_average)

    plt.rcParams.update({'font.size': 30})
    matplotlib.rcParams["mathtext.default"] = "regular"
                
    plt.figure(0)            
    plt.hist2d(fisher, correct_corr_list, bins=100, norm=mcolors.LogNorm(), cmap='Reds', range=[[-1, 1], [-1, 1]])
    plt.clim(1,30000)
    cb = plt.colorbar()
    cb.set_label('Number of entries')
    plt.xlabel("Test correlation", weight='bold')
    plt.ylabel("Reference correlation", weight='bold')
    #plt.show()
    plt.text(-0.9, 0.8, r'$r_s$ = $%.4f$' % (spearman_fisher[0]), fontsize=30)
    plt.plot([-1, 1], [-1,1],linestyle='dashed', color = 'black', linewidth=2)    
    plt.savefig("fisher_heatmap" + sys.argv[1] +".png", dpi=500, bbox_inches='tight')
    
    plt.figure(1)
    plt.hist2d(arithmetic_average, correct_corr_list, bins=100, norm=mcolors.LogNorm(), cmap='Reds', range=[[-1, 1], [-1, 1]])
    plt.clim(1,30000)
    cb = plt.colorbar()
    cb.set_label('Number of entries')
    plt.xlabel("Test correlation", weight='bold')
    plt.ylabel("Reference correlation", weight='bold')
    plt.text(-0.9, 0.8, r'$r_s$ = $%.4f$' % (spearman_arithmetic[0]), fontsize=30)
    plt.plot([-1, 1], [-1,1],linestyle='dashed', color = 'black', linewidth=2)
    
    plt.savefig("arithmetic_average_heatmap" + sys.argv[1]+".png", dpi=500, bbox_inches='tight')
    #plt.show()
        

    
if __name__ == '__main__':
    correct_corr = open("spearman_not_sun_1000genes.txt")
    make_heatmap(correct_corr)
    correct_corr.close()
