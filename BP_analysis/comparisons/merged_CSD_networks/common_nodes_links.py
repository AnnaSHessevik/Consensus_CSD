# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 16:32:54 2021

@author: annas
This script finds common nodes and edges, and calculates Jaccard indexes,
for the CSD networks for bipolar disorder based on both Fisher's Z transformed
and weighted untransformed averages.
"""

def make_set(infile):
    link_set = set()
    node_set = set()
    for line in infile:
        split_line = line.rstrip().split('\t')
        link_set.add((split_line[0].rstrip(), split_line[1].rstrip()))
        node_set.add(split_line[0].rstrip())
        node_set.add(split_line[1].rstrip())
    return link_set, node_set

def jaccard(set1, set2):
    intersection = len((set1).intersection(set2))
    union = (len(set1) + len(set2)) - intersection
    return (float(intersection) / union)

if __name__ == '__main__':
    #Open files
    infile1 = open("filtered_arithmetic_CSDSelection_10000.txt")
    infile2 = open("filtered_fisher_CSDSelection_10000.txt")

    #Create sets with edges from each input file
    link_set1, node_set1 = make_set(infile1)
    link_set2, node_set2 = make_set(infile2)
    
    #Close input files
    infile1.close()
    infile2.close()
    
    #Find common nodes and edges
    common_links = link_set1.intersection(link_set2)
    common_nodes = node_set1.intersection(node_set2)

    #Calculate Jaccard indexes
    jaccard_links = jaccard(link_set1, link_set2)
    jaccard_nodes = jaccard(node_set1, node_set2)
    
    #Print number of nodes and edges in each file.
    print("Arithmetic file has", len(node_set1), "nodes and", len(link_set1)/2, " links." )
    print("Fisher file has", len(node_set2), "nodes and", len(link_set2)/2, " links." )
    #Print number of common nodes and edges
    print("The files have", len(common_nodes), "common nodes and", len(common_links)/2, "common links." )
    #Print Jaccard index
    print("The Jaccard indexes for links and nodes are", jaccard_links, "and", jaccard_nodes, ", respectively")
        
