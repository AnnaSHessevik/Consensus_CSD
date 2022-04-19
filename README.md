# Consensus CSD

This repository includes all code and generated networks which has been utilized in my master's thesis to develop and generate consensus CSD networks for bipolar disorder (BP). This repository is divided into two main sections: Method Development and BP analysis. These are described in more detail below. The provided code should be viewed as an extension of the conventional CSD approach, for which the code can be found at https://github.com/andre-voigt/CSD.

## Method Development
The method development of my master's thesis consists of three main steps:
1. Processing of data sets: convert to correct format for CSD analysis, translate Gencode IDs to gene names, average gene expressions if Gencode IDs correspond to the same gene name and reduce the number of genes to 1000.
2. Method(s) for combining correlation coefficients: create subgroups of the data set, calculate Spearman rank correlation coefficients for all subgroups and for the total data set and combine subgroup correlation coefficients using Fisher's Z transformed and weighted untransformed averages. Note that this steps include FindCorrAndVar.cpp from https://github.com/andre-voigt/CSD.
3. Compare the combined correlation coefficients to the reference correlations by calcualting the Spearman rank correlation coefficeint of the correlations (correlation of correlations), root mean square error (RMSE) and Jaccard indexes.
