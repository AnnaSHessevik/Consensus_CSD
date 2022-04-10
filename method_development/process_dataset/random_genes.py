# -*- coding: utf-8 -*-
"""
Created on Thu Sep 16 13:28:48 2021

@author: annas

Select n random genes that are present in both of the two input data sets.
These genes are written to an output file. In addition, two files
corresponding to the original input data sets but with expressions
for only the random genes are generated.
Note that only one of the data sets is relevant for the development in the master thesis.
"""

infile1 = open("averaged_gene_names_not_sun.txt")
infile2 = open("averaged_gene_names_sun.txt")

outfile1 = open("not_sun_1000genes.txt", 'w')
outfile2 = open("sun_1000genes.txt", 'w')
outfile3 = open("random_genes.txt", 'w')
n_genes = 1000

#Skip first line in infiles (sample IDs)
next(infile1)
next(infile2)

#Make two lists with genes from each data set
genes1 = set()
genes2 = set()

for line in infile1:
    split_line1 = line.strip().split('\t')
    genes1.add(split_line1[0])
    split_line2 = infile2.readline().strip().split('\t')
    genes2.add(split_line2[0])

#Find the common genes
common_genes = genes1.intersection(genes2)
print("There are", len(common_genes), "common genes in the data sets")

#Select n_genes random genes from the common genes
random_genes = []
for i in range(0,n_genes):
    rand_gene = common_genes.pop()
    random_genes.append(rand_gene)
    outfile3.write(rand_gene + '\n')

#Reset reading position in the inpot files
infile1.seek(0, 0)
infile2.seek(0, 0)

#Copy first line in input files to corresponding output files
outfile1.write(infile1.readline())
outfile2.write(infile2.readline())

for line1 in infile1:
    split_line1 = line1.strip().split('\t')
    if split_line1[0] in random_genes:
        outfile1.write(line1)
   
    line2 = infile2.readline()
    split_line2 = line2.strip().split('\t')
    if split_line2[0] in random_genes:
        outfile2.write(line2)

infile1.close()
infile2.close()
outfile1.close()
outfile2.close()
outfile3.close()
    
    



