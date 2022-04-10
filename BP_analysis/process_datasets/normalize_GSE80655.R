#This script normalizes the read counts from GSE80655 using DESeq2

#Install packages
#if (!require("BiocManager", quietly = TRUE))
#  install.packages("BiocManager")

#BiocManager::install("DESeq2")
library("DESeq2")

#Read counts
cts = read.delim("raw_data_GSE80655.txt", row.names = 1) #Important to set correct row names

#Create data with dummy variable (needed as an argument to DESeq, but not part of normalization)
samples = colnames(cts)
dummy_variable = c(rep(1,281))
coldat = data.frame(dummy_variable)
rownames(coldat) = samples

#Normalize using DESeq2
dds = DESeqDataSetFromMatrix(countData = cts, colData = coldat, design=~ 1)
dds = estimateSizeFactors(dds)
normalized_counts = counts(dds, normalized=TRUE)
write.table(normalized_counts, file="GSE80655_normalized_counts.txt", sep="\t", quote=F, col.names=NA)
