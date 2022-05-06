# -*- coding: utf-8 -*-
"""
Created on Sun Oct  3 15:46:43 2021

@author: annas
This script calculates the Spearman rank correlation between the "true" correlations
calculated from an entire data set relative to Spearman rank correlations from a subgroup of the data set.
The arguments correspond to:
    1) The input file, a file with Spearman rank correlations from the subsample
    2) Y if it is wishful to make a plot
    3) "scatter" or "heatmap" depending on the wanted plot type
    """

import sys
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def calculate_correlation(correct_corr):
    if len(sys.argv) != 4:
        return 0,0
    
    try:
        #Input argument is the name of a file with estimated correlations
        subsample_corr = open(sys.argv[1])
        #subsample_corr = open("spearman_not_sun_1000genes.txt") #test set
        #Make lists with correlations
        correct_corr_list = []
        subsample_corr_list = []

        for line1 in correct_corr:
            line_split1 = line1.rstrip().split('\t')
            if line_split1[0] == line_split1[1]: #Do not include self-correlations
                next(subsample_corr)
                continue
            correct_corr_list.append(float(line_split1[2]))            
            
            line2 = subsample_corr.readline()
            line_split2 = line2.rstrip().split('\t')
            subsample_corr_list.append(float(line_split2[2]))
        
        subsample_corr.close()
         
        spearman = stats.spearmanr(correct_corr_list, subsample_corr_list)
        
        if sys.argv[2] == "Y":
            #Scatter plot
            if sys.argv[3] == "scatter":
                plt.figure(0)
                plt.scatter(subsample_corr_list,correct_corr_list, c="skyblue" )
                plt.xlim([-1, 1])
                plt.ylim([-1, 1])
                plt.xlabel("Test correlation", fontweight='bold')
                plt.ylabel("Reference correlation", fontweight='bold')
                #plt.show()
                plt.savefig(sys.argv[1] +"correlation_of_correlations_scatter"+".png")
        #Heatmap
            if sys.argv[3] == "heatmap":
                plt.figure(1)
                plt.rcParams.update({'font.size': 30})
                matplotlib.rcParams["mathtext.default"] = "regular"
                plt.hist2d(subsample_corr_list, correct_corr_list, bins=100, norm=mcolors.LogNorm(), cmap='Reds', range=[[-1, 1], [-1, 1]])
                plt.clim(1,30000)
                cb = plt.colorbar()
                cb.set_label('Number of entries')
                plt.xlabel("Test correlation", fontweight='bold')
                plt.ylabel("Reference correlation", fontweight='bold')
                #plt.show()
                plt.text(-0.9, 0.8, r'$r_s$ = $%.4f$' % (spearman[0]), fontsize=30)
                plt.plot([-1, 1], [-1,1],linestyle='dashed', color = 'black', linewidth = 2)                 
                plt.savefig(sys.argv[1] +"correlation_of_correlations_heatmap"+".png", dpi=500, bbox_inches='tight')
         
        
        return spearman
    except:
        return 0
    
if __name__ == '__main__':
    correct_corr = open("spearman_not_sun_1000genes.txt")
    spearman = calculate_correlation(correct_corr)
    
    if spearman != 0:
        try: #Print only correlation value, use as input in another script
            sys.stdout.write(str(spearman[0]))
        except:
            sys.stdout.write("Something failed\n")
    else:
        sys.stdout.write("Check your input arguments\n")
               
    correct_corr.close()
    

