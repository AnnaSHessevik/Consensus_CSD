# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 15:35:01 2022

@author: annas
This script replots the degree distribution for networks identified from Cytoscape.
This allows colours and other properties to be altered and fitted to the graphical style in my master's thesis. 
"""

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


def power_law(x, a, b):
    return a*np.power(x, b)

def plot_dd(G, col, pars, r2, fig_name):    
    degs = [d for n, d in G.degree()] #Get all degrees
    values, counts = np.unique(degs, return_counts=True) #Get sorted unique vakues and number of time each appear       
    
    fig, ax = plt.subplots()
    
    plt.plot(values, counts, "o", c = "black")
    plt.xlabel("Degree", fontweight='bold', fontsize=16)
    plt.ylabel("Number of nodes", fontweight='bold', fontsize=16)
    ax.set_xscale('log')
    ax.set_yscale('log')
    plt.xlim([1,51])
    plt.ylim([1,450])
    #Manual addition of wanted tics (not best method, replicate Cytoscape)
    ax.set_xticks([1, 10, 30, 50])
    ax.set_yticks([1,10,100,400])
    ax.set_xticklabels([1,10,30,50])
    ax.set_yticklabels([1,10,100,400])
    
    #Fit power law, gives different result than Cytoscape
    #pars, cov = curve_fit(f=power_law, xdata=values, ydata=counts, p0=[0, 0], bounds=(-np.inf, np.inf))
    
    #Replicated power law from Cytoscape
    ax.plot(values, power_law(values, *pars), linestyle='--', linewidth=2, color=col)
    plt.text(12,250, r'$y=%.2fx^{%.3f}$' % (pars[0], pars[1]))
    plt.text(12, 150, r'$R^2=%.3f$' % r2)
    
    
    plt.savefig(fig_name, dpi=500, bbox_inches='tight')


if __name__ == '__main__':
    #Open files
    arithmetic_file = open("filtered_arithmetic_CSDSelection_10000.txt", 'rb')
    fisher_file = open("filtered_fisher_CSDSelection_10000.txt", 'rb')
    
    #Create networks
    G_arithmetic = nx.read_edgelist(arithmetic_file, data=[('weight',float), ('edge type', str)])
    G_fisher = nx.read_edgelist(fisher_file, data=[('weight',float), ('edge type', str)])  
    
    #Close files
    arithmetic_file.close()
    fisher_file.close()
    
    #Create degree distribution, replicated from Cytoscape
    plt.rcParams['font.size'] = '14' #Change font size
    plot_dd(G_arithmetic, "lime", [238.32, -1.743], 0.899, "deg_dist_arithmetic.png")
    plot_dd(G_fisher, "indigo", [336.96, -1.862], 0.937, "deg_dist_fisher.png")
    
    
    
