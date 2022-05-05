# -*- coding: utf-8 -*-
"""
Created on Thu Sep 16 14:49:38 2021

@author: annas
This script sorts data sets (which contain the same genes). As a result, the 
new data sets contain the same genes in the same order.
Note that this script is not a required step for the correct method development 
in my master's thesis as this part is based on just one data set. 
"""

def sort_files(infile, outfile):
    for line in sorted(infile):
        outfile.write(line)


infile1 = open("sun_1000genes.txt")
infile2 = open("not_sun_1000genes.txt")
outfile1 = open("sorted_sun_1000genes.txt", 'w')
outfile2 = open("sorted_not_sun_1000genes.txt", 'w')

outfile1.write(infile1.readline())
outfile2.write(infile2.readline())

sort_files(infile1, outfile1)
sort_files(infile2, outfile2)

infile1.close()
infile2.close()
outfile1.close()
outfile2.close()
    


