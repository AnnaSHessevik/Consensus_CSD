# -*- coding: utf-8 -*-
"""
Created on Wed Jan 12 13:03:08 2022


@author: annas
This script is a modified version of subsample_correlation_of_correlations.
It calculates the Spearman rank correlation between two data sets.

The arguments correspond to:
    1) Reference file (to which the other file will be compared, here: file with Spearman rank correlations from a data set)
    2) The input file, a file with Spearman rank correlations (here: file with Spearman rank correlations from a second data set)
    3) Y if it is wishful to make a plot
    4) "scatter" or "heatmap" depending on the wanted plot type
    
Remember to change the colorbar range of the heatmap
"""

import sys
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def calculate_correlation(fisher_corr):
    if len(sys.argv) != 5:
        return 0,0
    
    try:
        #Input argument is the name of a file with estimated correlations
        test_corr = open(sys.argv[2])
        #Make lists with correlations
        fisher_corr_list = []
        test_corr_list = []
        
        for line1 in fisher_corr:
            line_split1 = line1.rstrip().split('\t')
            if line_split1[0] == line_split1[1]: #Do not include self-correlations
                next(test_corr)
                continue
            fisher_corr_list.append(float(line_split1[2]))            
            
            line2 = test_corr.readline()
            line_split2 = line2.rstrip().split('\t')
            test_corr_list.append(float(line_split2[2]))
        
        test_corr.close()
                    
        spearman = stats.spearmanr(fisher_corr_list, test_corr_list)
        
        if sys.argv[3] == "Y":
            plt.rcParams.update({'font.size': 18})
            matplotlib.rcParams["mathtext.default"] = "regular"
            
            #Scatter plot
            if sys.argv[4] == "scatter":
                plt.figure(0)
                plt.scatter(test_corr_list,fisher_corr_list, c="skyblue")
                plt.xlim([-1, 1])
                plt.ylim([-1, 1])
                plt.xlabel("Data set 1", fontweight='bold')
                plt.ylabel("Data set 2", fontweight='bold')
                plt.show()
                plt.savefig(sys.argv[2] +"correlation_of_correlations_scatter"+".png")
            #Heatmap
            elif sys.argv[4] == "heatmap":
                plt.figure(1)            
                plt.hist2d(test_corr_list, fisher_corr_list, bins=100, norm=mcolors.LogNorm(), cmap='Reds', range=[[-1, 1], [-1, 1]])
                plt.clim(1,350000)
                cb = plt.colorbar()
                cb.set_label('Number of entries')
                plt.xlabel("Data set 1", fontweight='bold')
                plt.ylabel("Data set 2", fontweight='bold')
                plt.text(-0.9, 0.8, r'$r_s$ = $%.4f$' % (spearman[0]), fontsize=18)
                #plt.show()
                plt.plot([-1, 1], [-1,1],linestyle='dashed', color = 'black')
                plt.savefig(sys.argv[2] +"similarity_heatmap.png", dpi=500, bbox_inches='tight')
        return spearman
    except:
        return 0
    
if __name__ == '__main__':
    fisher_corr = open(sys.argv[1])
    spearman = calculate_correlation(fisher_corr)
    
    if spearman != 0:
        try: #Print correlation value
            sys.stdout.write(str(spearman[0]))
        except:
            sys.stdout.write("Something failed\n")
    else:
        sys.stdout.write("Check your input arguments\n")
               
    fisher_corr.close()
    

