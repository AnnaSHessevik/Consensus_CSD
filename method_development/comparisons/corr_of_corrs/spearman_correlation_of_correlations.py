# -*- coding: utf-8 -*-
"""
Created on Thu Sep 30 12:26:49 2021

@author: annas
This script calculates the Spearman rank correlation between the "true" correlations
calculated from an entire data set relative to the estimated combined correlation
coefficients from averages of several subgroups.
The arguments correspond to:
    1) the sampling number
    2) "Y" if it is wishful to generate a scatter plot
"""



import sys
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def calculate_correlation(correct_corr):
    if len(sys.argv) != 3:
        return 0,0
    
    try:
        #Input argument is the name of a file with estimated correlations
        estimated_corr = open("combined_spearman_not_sun"+sys.argv[1]+".txt")
        next(estimated_corr)
        
        #Make lists with correlations
        correct_corr_list = []
        fisher = []
        aritmetric_average = []
        
        for line1 in correct_corr:
            line_split1 = line1.rstrip().split('\t')
            if line_split1[0] == line_split1[1]: #Do not include self-correlations
                next(estimated_corr)
                continue
            correct_corr_list.append(float(line_split1[2]))            
            
            line2 = estimated_corr.readline()
            line_split2 = line2.rstrip().split('\t')
            fisher.append(float(line_split2[-2]))
            aritmetric_average.append(float(line_split2[-1]))
        
        estimated_corr.close()
                    
        spearman_fisher = stats.spearmanr(correct_corr_list, fisher)
        spearman_average = stats.spearmanr(correct_corr_list, aritmetric_average)
        
        if sys.argv[2] == "Y":
            plt.figure(0)
            plt.scatter(fisher,correct_corr_list, c="indigo")
            plt.xlabel("Estimated combined Spearman rank correlation coefficient \nusing Fisher's Z transformed values")
            plt.ylabel("Spearman rank correlation coefficient from reference data set")
            plt.savefig("fisher" + sys.argv[1] +".png", dpi=500, bbox_inches='tight')
            
            plt.figure(1)
            plt.scatter(aritmetric_average, correct_corr_list, c="lime")
            plt.xlabel("Estimated combined Spearman rank correlation coefficient \nusing untransformed values")
            plt.ylabel("Spearman rank correlation coefficient from reference data set")
            plt.savefig("aritmetric_average" + sys.argv[1] +".png", dpi=500, bbox_inches='tight')
        
        
        return spearman_fisher, spearman_average
    except:
        return 0,0
    
if __name__ == '__main__':
    correct_corr = open("spearman_not_sun_1000genes.txt")
    spearman_fisher, spearman_average = calculate_correlation(correct_corr)
    
    if spearman_fisher != 0:
        try:
           # sys.stdout.write("File" + sys.argv[1] + '\n')
           # sys.stdout.write("Spearman correlation between correct and estimated correlation coefficients using: \n")
           # sys.stdout.write("Average of Fisher transformed values: " + str(spearman_fisher[0]) + '\n')
           # sys.stdout.write("Average of untransformed values: " + str(spearman_average[0]) + '\n')
            sys.stdout.write("File"+sys.argv[1]+'\t'+str(spearman_fisher[0])+'\t'+str(spearman_average[0])+'\n')
    
        except:
            sys.stdout.write("Something failed\n")
    else:
        sys.stdout.write("Check your input arguments\n")
               
    correct_corr.close()
    

