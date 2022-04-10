# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 10:50:32 2022

@author: annas
This script compares correlations from BP DLPFC, control DLPFC and
basal ganglia by investigating if correlations from basal 
and BP are on the same side of the control.
Note that the files must be sorted before the analysis.
"""
from math import log
import sys
import numpy as np

#Transform correlation to Fisher's Z
def fisher_transformation(r):
    if r == 1: #fisher approaches infinity
        z = 5
    elif r == -1: #fisher approaches -infinity
        z = -5
    else:    
        z = (1/2)*log((1+r)/(1-r))    #natural logarithm
    
    return z

#Calculate difference between BP and contrl relative to basal ganglia and write characteristics for the difference to file
def differences_cors(x_BP, x_ctrl, x_ganglia, outfile):
    #Calculate difference
    diff_ctrl_BP = x_ctrl - x_BP
    diff_ctrl_ganglia = x_ctrl - x_ganglia
    
    #Write differences to file
    outfile.write(str(diff_ctrl_BP) + '\t' + str(diff_ctrl_ganglia) + '\t')
    
    #initialize counters
    count_same = 0
    count_opposite = 0
    
    #Determine if BP and basal ganglia is on the same side relative to control
    if np.sign(diff_ctrl_BP) == np.sign(diff_ctrl_ganglia):
        outfile.write("1\n")
        count_same = 1
    
    else:
        outfile.write("0\n")
        count_opposite = 1
        
    return count_same, count_opposite


if __name__ == '__main__':
    #Open files
    infile1 = open("sorted_extracted_CSD_basal_ganglia.txt")
    next(infile1) #skip header
    infile2 = open("sorted_filtered_CSD_for_ganglia_comparison.txt") 
    next(infile2) #skip header
    outfile1 = open("rho_comparison_direction.txt", "w")
    outfile2 = open("z_comparison_direction.txt", "w")
    
    #Write header to outfiles
    outfile1.write("Gene1_BP\tGene2_BP\tGene1_ganglia\tGene2_ganglia\trho_BP\trho_ctrl\trho_ganglia\tEdge type\trho_ctrl-rho_BP\trho_ctrl-rho_ganglia\tSame side/sign?\n")
    outfile2.write("Gene1_BP\tGene2_BP\tGene1_ganglia\tGene2_ganglia\trho_BP\trho_ctrl\trho_ganglia\tEdge type\tz_BP\tz_ctrl\tz_ganglia\tz_ctrl-z_BP\tz_ctrl-z_ganglia\tSame side/sign?\n")
    
    #initialize counters
    count_rho_same_sign = 0
    count_rho_opposite_sign = 0
    count_z_same_sign = 0
    count_z_opposite_sign = 0
    
    
    #Read each line in the files, and make sure that there is a match between the genes
    for line1 in infile1:
        line_split1 = line1.rstrip().split('\t')
        gene_pair = (line_split1[0], line_split1[1])
        
        line2 = infile2.readline()
        line_split2 = line2.rstrip().split('\t')
        
        #Make sure that the same gene pair is investigated
        while (line_split1[0], line_split1[1]) != (line_split2[0], line_split2[1]):
            #note that we will not have an infinite loop as all gene pairs in infile1 must be in infile2 
            line2 = infile2.readline()
            line_split2 = line2.rstrip().split('\t')
        
        #Write gene names, rhos and edge type to outfiles
        gene1_ganglia = line_split1[0]
        gene2_ganglia = line_split1[1]
        gene1_BP = line_split2[0]
        gene2_BP = line_split2[1]
        rho_BP = line_split2[2]
        rho_ctrl = line_split2[3]
        rho_ganglia = line_split1[4]
        edge_type = line_split2[4]
        
        outfile1.write(gene1_BP + '\t' + gene2_BP + '\t' + gene1_ganglia + '\t' + gene2_ganglia + '\t' + rho_BP + '\t' + rho_ctrl + '\t' + rho_ganglia + '\t' + edge_type + '\t')
        outfile2.write(gene1_BP + '\t' + gene2_BP + '\t' + gene1_ganglia + '\t' + gene2_ganglia + '\t' + rho_BP + '\t' + rho_ctrl + '\t' + rho_ganglia + '\t' + edge_type + '\t')
       
        
        #Skip gene pair if rho_ganglia = NaN
        if (line_split1[4] == "nan"):
            outfile1.write('\n')
            outfile2.write('\n')
            continue
        
        #Investigate direction (BP and basal ganglia relative to control) directly from correlations
        count_same, count_opposite = differences_cors(float(rho_BP), float(rho_ctrl), float(rho_ganglia), outfile1)
        #Update counts for BP and ctrl based on which is closes to basal ganglia data
        count_rho_same_sign += count_same
        count_rho_opposite_sign += count_opposite

        
        #Calculate difference using Fisher's Z tranformed values of correlations
        z_BP = fisher_transformation(float(rho_BP))
        outfile2.write(str(z_BP) + '\t')
        
        z_ctrl = fisher_transformation(float(rho_ctrl))
        outfile2.write(str(z_ctrl) + '\t')
        
        z_ganglia = fisher_transformation(float(rho_ganglia))
        outfile2.write(str(z_ganglia) + '\t')
        
        z_count_same, z_count_opposite = differences_cors(z_BP, z_ctrl, z_ganglia, outfile2)
        #Update counts for BP and ctrl based on which is closes to basal ganglia data
        count_z_same_sign += z_count_same
        count_z_opposite_sign += z_count_opposite
        
      
        
    #close files
    infile1.close()
    infile2.close()
    outfile1.close()
    outfile2.close()
    
    #Write counts
    sys.stdout.write("Correlations from BP are on the same side as basal ganglia " + str(count_rho_same_sign) + " times (relative to control) based on correlation differences\n")
    sys.stdout.write("Correlations from BP are on the opposite side to basal ganglia " + str(count_rho_opposite_sign) + " times (relative to control) based on correlation differences\n")
    sys.stdout.write("Correlations from BP are on the same side as basal ganglia " + str(count_z_same_sign) + " times (relative to control) based on Fisher's Z differences\n")
    sys.stdout.write("Correlations from BP are on the opposite side to basal ganglia " + str(count_z_opposite_sign) + " times (relative to control) based on Fisher's Z differences\n")
    

   