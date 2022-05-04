# -*- coding: utf-8 -*-
"""
Created on Fri Feb 25 11:14:34 2022

@author: annas
This scripts create cluster heatmap to visualize the similarity between the 
data sets used to combine correlation coefficients in the CSD analysis

"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

if __name__ == '__main__':
    infile = open("comparison_BP_spearmans.txt")
    next(infile) #skip header
    
    #Make a dictionary from the input file
    dict_similarity = dict()
    col_names = []
    for line in infile:
        line_split = line.rstrip().split('\t')
        if len(col_names) < 6:
                col_names.append(line_split[1].rstrip().split("_")[2].split(".")[0])
        try:
            dict_similarity[line_split[0].rstrip().split("_")[2].split(".")[0]].append(float(line_split[2]))
            
        except:
            dict_similarity[line_split[0].rstrip().split("_")[2].split(".")[0]] = [float(line_split[2])]
        
    #Convert dictionary to pandas dataframe
    df = pd.DataFrame.from_dict(dict_similarity, orient='index', columns=col_names)
    
        
    #Make clustermap
    plt.rcParams.update({'font.size': 22}) #change font size    
    cg = sns.clustermap(df, cmap='coolwarm', annot=True, vmin=-1, vmax=1, tree_kws={"colors":"black", "linewidth":1.3})
    plt.setp(cg.ax_heatmap.yaxis.get_majorticklabels(), rotation=0)
    plt.savefig("comparison_BP_spearmans.png", dpi=500, bbox_inches='tight')