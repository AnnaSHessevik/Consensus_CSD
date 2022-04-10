# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 16:16:18 2021

@author: annas
Average gene expressions for GenCode IDs which correspond to the same gene name.
Very similar to Combine_gene_expressions.py
"""

#Create a dictionary where the keys corresponds to gene names and the 
#values corresponds to a list of lists of gene expressions for each gene name
def make_expression_dict(filename):
    dict_expression = {}
    #Read each line in the file
    for line in filename:
        #Convert line to list of strings
        split_line = line.rstrip().split('\t') #Split the line
        #First element in the line is the gene name
        gene_name = split_line[0]
        
        
        #Add the other elements in the line to a list of gene expressions
        expressions = []
        for i in range(1, len(split_line)):
            expressions.append(float(split_line[i]))
        try:
            dict_expression[gene_name].append(expressions)
        except:
            dict_expression[gene_name] = [expressions]
    return dict_expression    

#Average expression values for gene names which correspond to more than one
    #gene names. Write the values directly to file.

def average_expressions(dict_expressions, outfile):
    #Go through each key in the input dictonary. 
    for key in dict_expressions:
        outfile.write(key)
        
        #If the gene is unique, we keep the values from dict_expressions and 
        #write them directly to the output file
        if len(dict_expressions[key]) == 1:
            for val in dict_expressions[key]:
                for el in val:
                    outfile.write('\t' + str(el))
        
        #If the gene is nonuniqe, calculate the average expressions
        else:
            for i in range(0, len(dict_expressions[key][0])):
                average = 0
                for j in range(0, len(dict_expressions[key])):
                    average += dict_expressions[key][j][i]
                average /= len(dict_expressions[key])
                outfile.write('\t'+str(average))
        outfile.write('\n')



#--------------------------------------------------------------#
"""Edit here"""
#Read files
infile = open("gene_names_not_sun.txt")
outfile = open("averaged_gene_names_not_sun.txt", 'w')

#Copy first line in infile to outfile
outfile.write(infile.readline())

#Create dictionary with gene names and list of expression values
dict_expression = make_expression_dict(infile)

#Write gene names and averaged expression values to out_files
average_expressions(dict_expression, outfile)

#Close files
infile.close()
outfile.close()


