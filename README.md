# Consensus CSD

This repository includes all code and generated networks which has been utilized in my master's thesis to develop and generate consensus CSD networks for bipolar disorder (BP). This repository is divided into two main sections: Method Development and Analysis of Bipolar Disorder. These are described in more detail below. Note that some parts of the method development and analysis of BP use the same or similar code. In these cases, the scripts are included twice for clarity (once in Method Development and once in Analysis of Bipolar Disorder).
The provided code should be viewed as an extension of the conventional CSD approach, for which the code can be found at https://github.com/andre-voigt/CSD.

## Method Development
The method development of my master's thesis consists of three main steps:
1. **Process data set**: convert the data set to an appropriate format for CSD analysis, translate Gencode IDs to gene names, average gene expressions if some Gencode IDs correspond to the same gene name and reduce the number of genes to 1000.
2. **Split the data set and re-combine correlation coefficients**: create subgroups of the data set, calculate Spearman rank correlation coefficients for all subgroups and for the total data set and combine subgroup correlation coefficients using Fisher's Z transformed and weighted untransformed averages.
3. **Comparisons**: compare the combined correlation coefficients to the reference correlations by calculating the Spearman rank correlation coefficient of the correlations (correlation of correlations), root mean square error (RMSE) and Jaccard indexes.

## Analysis of Bipolar Disorder
The consensus CSD analysis of BP consists of five major steps as listed below. Note that the folder called BP_analysis also includes a file with the generated CSD network(s) for BP.
1. **Process data sets**: normalize data set if required, extract BP and control samples, convert probe IDs to gene names and omit ambiguous and non-zero expression probes/genes and non-universally represented genes.
2. **Calculate and combine correlation coefficients**: calculate Spearman rank correlation coefficients for all processed data sets, combine correlation coefficients using Fisher's Z transformed and weighted untransformed averages and process the combined correlation coefficients into a readable format for further CSD analysis.
3. **Conventional CSD analysis and significance filtering**: run the remaining part of the CSD analysis as explained at https://github.com/andre-voigt/CSD. An additional step with significance filtering of the correlations have also been included. 
4. **Network analysis**: investigation and calculation of degree distribution (from Cytoscape), network assortativity, average clustering and identification of communities, hubs and characteristics of known disease genes for BP. The network analyses also included functional analyses, but these were mainly conducted using external software.
5. **Comparisons**: clustering analysis of Spearman rank correlation coefficients from each data set, comparison of Fisher's Z transformed and weighted untransformed averages at the level of correlation coefficients by calculating correlation of correlations and Jaccard indexes, comparison of Fisher's Z transformed and weighted untransformed averages at the network level by evaluating characteristics and identity of nodes and links and by visualizing the overlap of the networks, and comparison of underlying correlation coefficients in the CSD network based on weighted untransformed averages to basal ganglia (part of the functional analyses).

## General Consensus CSD Analysis
Many of the above steps specifically apply to the analysis of the test, BP or control data sets. If it is wishful to use to code to generate consensus CSD networks for other conditions/disorders/diseases, the following 
