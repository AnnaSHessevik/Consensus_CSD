# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 11:14:31 2022

@author: annas
This script creates a summary of the statistics for the comparison
of the BP CSD network and correlations from basal ganglia
"""
  
from scipy.stats import binomtest

def write2outfile(data, edge_type, outfile):
    #Counts (remove duplicates)
    edge_type_same = (data.count((edge_type, "1")))/2
    edge_type_opposite = (data.count((edge_type, "0")))/2
    total = edge_type_same + edge_type_opposite
    #p-value
    p = binomtest(int(edge_type_same), int(total), 2/3)
    
    outfile.write(edge_type + "\t" + str(edge_type_same) + '\t' + str(edge_type_same/(total)) + '\t' + str(edge_type_opposite) + '\t' + str(edge_type_opposite/(total)) + '\t' + str(p.pvalue) + '\n')
    
    return edge_type_same, edge_type_opposite       

if __name__ == '__main__':
    #Open files
    infile = open("rho_comparison_direction.txt")
    next(infile) #skip header
    outfile = open("summary_direction_comparison.txt", "w")
    
    #Make list of pairs with edge_type and if the gene pair
    #has same sign when BP and basal ganglia are compared to control
    data = []
    
    for line in infile:
        line_split = line.rstrip().split('\t')
        data.append((line_split[7], line_split[10]))
    
    #Write statistics to outfile
    outfile.write("Edge type\tSame side/sign\tSame side/sign[%]\tOpposite sides/signs\tOpposite sides/signs[%]\tp-value\n")
    C_same, C_opposite = write2outfile(data, "C", outfile)
    S_same, S_opposite = write2outfile(data, "S", outfile)
    D_same, D_opposite = write2outfile(data, "D", outfile)
    CSD_same = C_same + S_same + D_same
    CSD_opposite = C_opposite + S_opposite + D_opposite
    p = binomtest(int(CSD_same), int(CSD_same+CSD_opposite), 2/3) #note: E(p) = 2/3
    
    outfile.write("CSD\t" + str(CSD_same) + '\t' + str(CSD_same/(CSD_same+CSD_opposite)) + '\t' + str(CSD_opposite) + '\t' + str(CSD_opposite/(CSD_same+CSD_opposite)) + '\t' + str(p.pvalue) + '\n')
    
    #Close files
    outfile.close()
    
