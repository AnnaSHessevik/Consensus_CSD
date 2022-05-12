# Consensus CSD

This repository includes all scripts which have been utilized in my master's thesis to develop and generate consensus CSD networks for bipolar disorder (BP). This repository is divided into two main sections: Method Development and Analysis of Bipolar Disorder. These are described in more detail below. Note that some parts of the method development and analysis of BP use the same or similar code. In these cases, the scripts are included twice for clarity (once in Method Development and once in Analysis of Bipolar Disorder).
The provided code should be viewed as an extension of the conventional CSD approach, which is available at https://github.com/andre-voigt/CSD.

## Method Development
The method development of my master's thesis consists of three main steps:
1. **Process data set**: convert the data set to an appropriate format for CSD analysis, translate Gencode IDs to gene names, average gene expressions if some Gencode IDs correspond to the same gene names and reduce the number of genes to 1000.
2. **Split the data set and re-combine correlation coefficients**: create subgroups of the data set, calculate Spearman rank correlation coefficients for all subgroups and for the total data set and combine subgroup correlation coefficients using Fisher's Z transformed and weighted untransformed averages.
3. **Comparisons**: compare the combined correlation coefficients to the reference correlations by calculating the Spearman rank correlation coefficient of the correlations (correlation of correlations), root mean square error (RMSE) and Jaccard indexes.

## Analysis of Bipolar Disorder
The consensus CSD analysis of BP consists of five major steps as listed below. Note that the folder called BP_analysis also includes a file with the generated CSD network(s) for BP.
1. **Process data sets**: normalize data sets if required, extract BP and control samples, convert probe IDs to gene names and omit ambiguous and zero expression probes/genes and non-universally represented genes.
2. **Calculate and combine correlation coefficients**: calculate Spearman rank correlation coefficients for all processed data sets, combine correlation coefficients using Fisher's Z transformed and weighted untransformed averages and process the combined correlation coefficients into a readable format for further CSD analysis.
3. **Conventional CSD analysis and significance filtering**: run the remaining part of the CSD analysis as explained at https://github.com/andre-voigt/CSD. An additional step with significance filtering of the correlations has also been included. 
4. **Network analysis**: investigation and calculation of degree distribution (from Cytoscape), network assortativity, average clustering and identification of communities, hubs and characteristics of known disease genes for BP. The network analyses also included functional analyses, but these were mainly conducted using external software.
5. **Comparisons**: clustering analysis of Spearman rank correlation coefficients from each data set, comparison of Fisher's Z transformed and weighted untransformed averages at the level of correlation coefficients by calculating correlation of correlations and Jaccard indexes, comparison of Fisher's Z transformed and weighted untransformed averages at the network level by evaluating characteristics and identities of nodes and links and by visualizing the overlap of the networks, as well as comparison of underlying correlation coefficients in the CSD network based on weighted untransformed averages to basal ganglia (part of the functional analyses).

## General Consensus CSD Analysis
The developed methods for creating consensus CSD networks may be applied to other conditions/disorders/diseases. In these cases, it is important to process the data sets in advance. The input files are expected to have the same format as outlined in the conventional CSD approach (https://github.com/andre-voigt/CSD). In addition, all data sets must contain the same genes. In order to create a final consensus CSD network, the following commands should be run:
1. **./sort_and_FindCorr.sh**: sorts expression files and calculates Spearman rank correlation coefficients.
2. **./combined_corr.sh**: generates the appropriate format and gives input into improved_fisher_transformation.py, which combines correlation coefficients using both Fisher's Z transformed and weighted untransformed averages. Alternatively, one may apply the command python3 improved_fisher_transformation.py directly.
3. **python3 process_combined_corr.py**: converts the output file from step 2 into a readable format for subsequent CSD analysis.
4. **python2 FindCSD.py** and **python2 CreateNetwork.py**: compute C, S and D scores and create the CSD network as described at https://github.com/andre-voigt/CSD.
5. **python3 check_underlying_corr.py**, **significance_filtering.xlsx** and **python3 filter_CSD.py**: identify underlying correlations of the links in the CSD network, calculate corrected p-values and exclude insignificant correlations. Note that the significance_filtering.xlsx requires manual investigation and cannot be "run" in the conventional sense. 

