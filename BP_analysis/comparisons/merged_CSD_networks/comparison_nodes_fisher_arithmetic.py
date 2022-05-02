# -*- coding: utf-8 -*-
"""
Created on Sun Jan 23 14:59:17 2022

@author: annas
This scripts investigate and compare nodes from two CSD networks based
on Fisher's Z transformed values or weighted untransformed means.
The following comparisons are carried out and written to file:
    1) See if the node is common
    2) Identify degree
    3) Identify common neighbours
    4) Indentify number of C, S and D links
    
    
Furthermore, this script plots degree of nodes in the CSD network based on 
weighted untransformed mean of correlations relative to 
combined correlations using Fisher's Z transformation.
This script also plots degree in each of the CSD networks
relative to Jaccard index for common neigbours between the 
two networks for node i.
"""
import networkx as nx
#import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import Counter as Counter


def write_neighbours(node, G, outfile):
    i=0
    for key in G.adj[node]:
        outfile.write(key) #Write neighbours
        i += 1
        if i < G.degree[node]:
            outfile.write(", ") #seperate neigbours by ","
        else:
            outfile.write('\t')

def jaccard(set1, set2):
    intersection = len((set1).intersection(set2))
    union = (len(set1) + len(set2)) - intersection
    return (float(intersection) / union)

def write_node_properties(G_arithmetic, G_fisher, common_nodes, outfile):
    degrees_arithmetic = [] #list of degrees for CSD network based on weighted untransformed mean of correlation coefficients
    degrees_a_specific = []
    degrees_fisher = [] #list of degrees for CSD network based on combined correlation coefficients usign Fisher's Z transformation
    degrees_f_specific = []
    jaccard_list = [] #list of Jaccard indexes for common neighbours of node i in the two CSD networks
    jaccard_specific = []

    #Write header to file
    outfile.write("Node" + '\t' + "Degree_a" + '\t' + "Degree_f" + '\t' + "Neighbours_a" + '\t' + "Neighbours_f" + '\t' + "Jaccard index of neigbours" + '\n')
    
    #Investigate node properties for each node
    for node in G_arithmetic:
        if node in common_nodes:
            #Write degree to file
            outfile.write(node + '\t' + str(G_arithmetic.degree[node]) + '\t' + str(G_fisher.degree[node]) + '\t')
            
            #Write degree to list
            degrees_arithmetic.append(G_arithmetic.degree[node])
            degrees_fisher.append(G_fisher.degree[node])
            
            #Write neighbours of node to file
            write_neighbours(node, G_arithmetic, outfile)
            write_neighbours(node, G_fisher, outfile)
            
            #Write jaccard index for common neighbours of the node
            jac = jaccard(set(G_arithmetic.adj[node]), set(G_fisher.adj[node]))        
            jaccard_list.append(jac)
            outfile.write(str(jac) + '\n')

        
        else:
            #Write degree, neigbours and jaccard (=0) to file
            outfile.write(node + '\t' + str(G_arithmetic.degree[node]) + '\t' + str(0) + '\t')
            degrees_a_specific.append(G_arithmetic.degree[node])
            degrees_f_specific.append(0)
            write_neighbours(node, G_arithmetic, outfile)
            outfile.write("-" + '\t')
            outfile.write("0" + '\n')
            jaccard_specific.append(0)
    
    for node in G_fisher:
        if node in common_nodes: #Covered by previous loop
            continue
        else:
           #Write degree, neigbours and jaccard (=0) to file
            outfile.write(node + '\t' + str(0) + '\t' + str(G_fisher.degree[node]) + '\t')
            degrees_a_specific.append(0)
            degrees_f_specific.append(G_fisher.degree[node])
            outfile.write("-" + '\t')
            write_neighbours(node, G_fisher, outfile)
            outfile.write("0" + '\n') 
            jaccard_specific.append(0)
        
    return degrees_arithmetic, degrees_fisher, jaccard_list, degrees_a_specific, degrees_f_specific, jaccard_specific


def x_y_sizes(count):
    x=[]
    y=[]
    sizes=[]
    for key in count:
        x.append(key[0])
        y.append(key[1])
        sizes.append(count[key]+15)    
    return x,y,sizes

def make_plots(var1, var2, col, x_lab, y_lab, fig_name, nr, var1_specific, var2_specific, col_specific):    
    #Create pair of var1 and var2
    #Common nodes
    var1_vs_var2 = []
    i = 0
    for var in var1:
        var1_vs_var2.append((var, var2[i]))
        i += 1
     
    #Specific nodes
    var1_vs_var2_specific = []
    i = 0
    for var in var1_specific:
        var1_vs_var2_specific.append((var, var2_specific[i]))
        i += 1
        
    #Count how many times same pair appears    
    count = Counter(var1_vs_var2)
    count_specific = Counter(var1_vs_var2_specific)
    
    #Define x, y and sizes for nodes. Sizes determined by the count above
    x,y,sizes = x_y_sizes(count)
    x_s, y_s, sizes_s = x_y_sizes(count_specific)
    
    #Plot result in a scatter plot where size of circle correspond to number of appearances.
    plt.figure(nr, figsize=(7,4.6))
    ax = plt.gca()    
    #Playing with the appearance of the plot depending on which plot is made
    if ("Jaccard" in y_lab): 
        ax.scatter(x_s,y_s,s=sizes_s, c=col_specific, alpha=0.8, label="Unique")
        ax.scatter(x,y,s=sizes, c=col, alpha=1, label="Common")
        #Determine order of labels
        handles, labels = plt.gca().get_legend_handles_labels()
        order=[1,0]
        plt.legend([handles[i] for i in order], [labels[i] for i in order], loc="lower right", bbox_to_anchor=(1,0.07))
         
        
    else:
        ax.scatter(x,y,s=sizes, c=col, alpha=1, label="Common")
        ax.scatter(x_s,y_s,s=sizes_s, c=col_specific, alpha=0.7, label="Unique")
        #Determine order of labels
        handles, labels = plt.gca().get_legend_handles_labels()
        order = [0,1]
        plt.legend([handles[i] for i in order], [labels[i] for i in order], loc="lower right", bbox_to_anchor=(1,0.07))
        
        
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    plt.xlabel(x_lab, fontweight='bold')
    plt.ylabel(y_lab, fontweight='bold')
    
    
    #plt.show()    
    plt.savefig(fig_name, dpi=500, bbox_inches='tight')


if __name__ == '__main__':
    #Open files
    arithmetic_file = open("filtered_arithmetic_CSDSelection_10000.txt", 'rb')
    fisher_file = open("filtered_fisher_CSDSelection_10000.txt", 'rb')
    outfile = open("node_properties.txt", "w")
    
    #Create networks
    G_arithmetic = nx.read_edgelist(arithmetic_file, data=[('weight',float), ('edge type', str)])
    G_fisher = nx.read_edgelist(fisher_file, data=[('weight',float), ('edge type', str)])  
    
    #Find common nodes
    nodes_arithmetic = set(G_arithmetic.nodes)
    nodes_fisher = set(G_fisher.nodes)
    common_nodes = nodes_arithmetic.intersection(nodes_fisher)
    
    #Find node properties of common nodes and write to file
    degrees_arithmetic, degrees_fisher, jaccard_list, degrees_a_specific, degrees_f_specific, jaccard_specific = write_node_properties(G_arithmetic, G_fisher, common_nodes, outfile)
    
    #Close files
    arithmetic_file.close()
    fisher_file.close()
    outfile.close()
    
    #Make plots
    plt.rcParams['font.size'] = '15' #Change font size
    make_plots(degrees_fisher, jaccard_list, "indigo", "Degree in CSD network based on Fisher's Z \ntransformed correlation coefficients", "Jaccard index", "degree_vs_jaccard_CSD_fisher_v2.png", 1, degrees_f_specific, jaccard_specific, "mediumorchid")
    make_plots(degrees_arithmetic, jaccard_list, "forestgreen", "Degree in CSD network based on weighted \nuntransformed correlation coefficients", "Jaccard index", "degree_vs_jaccard_CSD_arithmetic_v2.png", 2, degrees_a_specific, jaccard_specific, "lime")
    make_plots(degrees_arithmetic, degrees_fisher, "firebrick", "Degree in CSD network based on weighted \nuntransformed correlation coefficients", "Degree in CSD network based \non Fisher's Z transformed\n correlation coefficinets", "degree_vs_degree_CSD_v2.png", 3, degrees_a_specific, degrees_f_specific, "lightcoral")
    