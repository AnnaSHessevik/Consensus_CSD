# -*- coding: utf-8 -*-
"""
Created on Fri Sep 17 13:43:18 2021

@author: annas
Split a given data set into subsets with 10-49 samples. In some cases,
a maximum of 58 samples are allowed to make the subsets correspond to the
full data set.
A file is generated to indicate the subsample sizes of the random splits.
Note that one line in this file corresponds to one round of subsampling.
"""

from random import seed
from random import randint
from random import shuffle

#Create non-overlapping subsamples of random sizes between 10-49 (might have exceptions)
def subsampling(id_index, outfile1):
    random_split = [] #will contain list of lists where the elements correspond to the random splitting of the original dataset
    pos = 0 #current position in id_index list
    random_integer = 0 #Initialization
    
    while len(id_index) > pos:
        #Generate a random subsample
        random_integer = randint(10, 49)
        
        #Add random subsample to list
        random_split.append(id_index[pos:pos+random_integer]) 
        
        #Change the position in the id_index list
        pos += random_integer
        
        #If there are between 1-9 elements left in the id_index,
        #add these to the last added subsample
        if (pos > len(id_index)-10):
            random_split[-1] += (id_index[pos:len(id_index)])
            pos = len(id_index) #update position
            
        #Write the subsample size to file
        outfile1.write(str(len(random_split[-1])) + '\t')
        
        #If there are between 10-49 elements left in the id_index,
        #add these as a seperate subsample
        if ((pos < len(id_index) - 9) and (pos > len(id_index) - 50)):
            random_split.append(id_index[pos:len(id_index)])
            #Write subsable size to file
            outfile1.write(str(len(random_split[-1])) + '\t') 
            #update position
            pos = len(id_index)
    
    outfile1.write('\n')
    return random_split


def subsamples2file(random_split, infile, outfile_names, i):
    #Move to top of the input file
    infile.seek(0, 0)
    
    #Make a list of input files
    outfiles = []
    for k in range(0,len(random_split)):
        outfiles.append(open(outfile_names + str(i+1) + "_" + str(k+1) + ".txt", 'w')) #filename such as file1_1.txt
            
    for line in infile:
        split_line = line.rstrip().split('\t') #split the line
        
        for m in range(0,len(random_split)):
            #Always write the gene name (and gene_id) to the output files
            outfiles[m].write(split_line[0])
            
            #Write subsample
            for id_index in random_split[m]:
                outfiles[m].write('\t' + split_line[id_index])                    
            
            outfiles[m].write('\n')
            
    for outfile in outfiles:
        outfile.close()
            

"""Edit here"""
n_subsampling = 100 #Number of subsamplig processes
infile = open("sorted_not_sun_1000genes.txt") #NB: sorted!!
outfile1 = open("not_sun_1000genes_sample_sizes.txt", 'w')
outfile_names = "not_sun_1000genes_subsample"
chosen_number = 0 #influence the random seed

#Make a list of the samples IDs
ids = infile.readline().rstrip().split('\t') #Split the line in the header

#Note: first element in the ID list is gene_id (not spesific sample)
#Pair the samples IDs with its index in the file
id_index = []
for i in range(1,len(ids)):
    id_index.append(i) #Add 1 because the original first element is empty in the ID list

#Subsampling
for i in range(0,n_subsampling):
    seed(i+chosen_number) #Make the results reproducible due to pseudorandom properties
    
    #Shuffle the ID list
    shuffle(id_index)
    
    #Create non-overlapping subsamples of random sizes between 10-49 (might have exceptions)
    #Write the subsample sizes to outfile1
    random_split = subsampling(id_index, outfile1)
    
    #Write the subsamples and their expression to distinct output files
    subsamples2file(random_split, infile, outfile_names, i)
    

infile.close()
outfile1.close()
