# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 15:55:27 2021

@author: annas
This script "averages" Spearman rank correlations in input data sets based on 
Fisher's Z transformation and weighted untransformed averages.
The input data sets must contain the same gene pairs.
If arguments are passed to this script from the command line, they must follow these rules:
    Argument 1 is the number of datasets
    Argument 2 is a string of sample sizes separated by -
    Argument 3 is a string of input file names separated by -
    Argument 4 is the name of the output file
"""

from math import log
from math import exp
import sys
import re

########################################################################################################

#Write header of outout file
def write_header(outfile, num_datasets, infiles_number):
    outfile.write("Gene 1\tGene 2\t")
    for i in range(0,num_datasets):
        outfile.write("Spearman_" + infiles_number[i] + '\t')
        outfile.write("Fisher Z_"+ infiles_number[i] + '\t')
    outfile.write("Average Z\tBactransformed Spearman\tWeighted aritmetric averaged Spearman\n")


#Caluclate and write Fisher Zs, averaged Zs, bactransformed spearman ranks and 
    #aritmetic average of S to output file
def write_output(infiles, num_datasets, sizes_datasets):
    #Use first file as a reference file to read all files line by line
    for line in infiles[0]:
        #Reset all lists and values
        spearman_ranks = []
        fisher_zs = []
        z_numerator = 0
        z_denominator = 0
        z_average = 0
        z_backtransformed = 0
        r_numerator = 0
        r_average = 0
        
        #Split line in the first infile
        split_line = line.rstrip().split('\t')
        
        #Write gene names and first spearman rank correlation to output file
        outfile.write(split_line[0] + '\t' + split_line[1])
        
        #Write to output file and save all spearman rank correlations and Fisher Zs from all files
        for i in range(0,num_datasets):
            if i != 0:
                #Read next line in input file i. Save this line as list.
                split_line = infiles[i].readline().rstrip().split('\t')
            
            outfile.write('\t' + str(split_line[2])) #Write spearman rank correlation coefficient to output file
            spearman_ranks.append(float(split_line[2])) #Add spearman rank correlation coefficient to list
            
            #Calculate Fisher Z and save it to output file
            z = fisher_transformation(float(split_line[2]))
            outfile.write('\t' + str(z))
            #Save Fisher Z in list
            fisher_zs.append(z)
        
        #Calculate average Fisher Z and 
        #weighted aritmetric average of the spearman rank correlation coefficients
        for j in range(0, num_datasets):
            z_numerator += (sizes_datasets[j] - 3)*fisher_zs[j] #Numerator of averaged Fisher Z
            z_denominator += (sizes_datasets[j]-3) #Denominator of average of Fisher Z
            r_numerator += sizes_datasets[j]*spearman_ranks[j]
            
        z_average = z_numerator/z_denominator
        r_average = r_numerator/sum(sizes_datasets)
        
        #Backtransform averaged Fisher Z to spearman rank correlation coefficient
        z_backtransformed = (exp(2*z_average)-1)/(exp(2*z_average)+1)
        
        #Write Fisher Z value, its backtransformed value and weighted
        #aritmetric average of spearman rank correlation coefficients to output file
        outfile.write('\t' + str(z_average) + '\t' + str(z_backtransformed) + '\t' + str(r_average) + '\n')
        
        
            
        
def fisher_transformation(r):
    if r == 1: #fisher approaches infinity
        z = 5
    elif r == -1: #fisher approaches -infinity
        z = -5
    else:    
        z = (1/2)*log((1+r)/(1-r))    #natural logarithm
    
    return z


#########################################################################################################
"""Edit here"""
if __name__ == '__main__':
    if len(sys.argv) != 5:
        sys.stdout.write(str(len(sys.argv)) + " Not enough arguments passed. The default settings are used")
        
        #Test dataset
        num_datasets = 2 #Must be specified by the user. Corresponds to the number of data sets
        sizes_datasets = [18, 46] #Must be specified by the user. Correspond to sizes of the data sets. The order is important 
    
        infiles = [] #List which will contain all files that are used to calculate averages
        infiles_number = []
        #Define input files. Must be spesified by user.
        #Here, all input files have names in the same format, example: filex.txt where x corresponds to the data set number
        #If a different style is used, the input files must be specified outside the for loop
        #Save the data set number (make this code in line with the code that take arguments)
        for i in range (0, num_datasets):
            infiles.append(open("tumor_spearman" + str(i+1) + ".txt"))
            infiles_number.append(str(i+1))
            
        outfile_name = "combined_tumor_spearman_test.txt" #Name of output file. Must be specified by user.
        outfile = open(outfile_name, 'w')
    
    else:
        num_datasets = int(sys.argv[1]) #Argument 1 is the number of data sets
        sizes_datasets_strings = sys.argv[2].rstrip().split("-") #Argument 2 is a string with all sample sizes separated by -
        sizes_datasets = []
        #Convert the sizes to ints
        for size in sizes_datasets_strings:
            sizes_datasets.append(int(size))
            
        infiles_name = sys.argv[3].rstrip().split("-") #Argument 3 is a string with all input filenames separated by -
        #Open the input files
        infiles = []
        for name in infiles_name:
            infiles.append(open(name))
        
        #Save the number of the input file (GEO accession number) to make the output file more reader friendly
        infiles_number = []
        for name in infiles_name:
            name_split = name.split('.') #seperate .txt from rest of file names
            name_split2 = name_split[0].split('_')
            infiles_number.append(name_split2[-1])
            
            
        outfile = open(sys.argv[4], 'w') #Argument 4 is the output file name
    
    
    #Write header of outfile
    write_header(outfile, num_datasets, infiles_number)
    
    #Read line by line from the input files. Calculate Fishers Zs, average the Zs and 
    #backtransform to correlation coefficient. In addition, the arithmetic average of 
    #the correlations (for each gene pair) is calculated.
    write_output(infiles, num_datasets, sizes_datasets)
    
    #Close files
    for infile in infiles:
        infile.close()
        
    outfile.close()




