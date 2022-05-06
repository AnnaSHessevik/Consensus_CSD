# -*- coding: utf-8 -*-
"""
Created on Sun Jan 23 13:07:55 2022

@author: annas
This script reads two files resulting from the CSD analysis (from Fisher's Z transformed
and weighted untransformed averages methods) and creates a file for the merged network. 
"""

def make_set(infile):
    link_set = set()
    node_set = set()
    for line in infile:
        split_line = line.rstrip().split('\t')
        link_set.add((split_line[0].rstrip() + "+" + split_line[1].rstrip(), split_line[3].rstrip())) #set of pairs (note: cannot have set of lists)
        node_set.add(split_line[0].rstrip())
        node_set.add(split_line[1].rstrip())
    return link_set, node_set

def write_network(link_set, outfile, network_type):
    for link in link_set:
        gene_pair = link[0].split('+')
        outfile.write(gene_pair[0].rstrip() + '\t' + gene_pair[1].rstrip() + '\t' + link[1] + '\t' + network_type +'\n')
          
def write_node_attributes(node_set, outfile, network_type):
    for node in node_set:
        outfile.write(node + '\t' + network_type + '\n')


if __name__ == '__main__':
    #Open files
    infile1 = open("filtered_arithmetic_CSDSelection_10000.txt")
    infile2 = open("filtered_fisher_CSDSelection_10000.txt")

    #Create sets with edges from each input file
    link_arithmetic, nodes_arithmetic = make_set(infile1)
    link_fisher, nodes_fisher = make_set(infile2)
    
    #Close input files
    infile1.close()
    infile2.close()
    
    #Find the common nodes and links with same edge type
    common_links = link_arithmetic.intersection(link_fisher)
    common_nodes = nodes_arithmetic.intersection(nodes_fisher)
    
    #Find nodes and links unique to each file
    unique_links_arithmetic = link_arithmetic.difference(link_fisher)
    unique_nodes_arithmetic = nodes_arithmetic.difference(nodes_fisher)
    unique_links_fisher = link_fisher.difference(link_arithmetic)
    unique_nodes_fisher = nodes_fisher.difference(nodes_arithmetic)
    
    #Write the merged network to file
    outfile_links = open("merged_arithmetic_fisher.txt", 'w')
    write_network(common_links, outfile_links, "common")    
    write_network(unique_links_arithmetic, outfile_links, "arithmetic")
    write_network(unique_links_fisher, outfile_links, "fisher")
    outfile_links.close()
    
    outfile_nodes = open("merged_network_attributes.txt", 'w')
    write_node_attributes(common_nodes, outfile_nodes, "common")
    write_node_attributes(unique_nodes_arithmetic, outfile_nodes, "arithmetic")
    write_node_attributes(unique_nodes_fisher, outfile_nodes, "fisher")
    outfile_nodes.close()
    
