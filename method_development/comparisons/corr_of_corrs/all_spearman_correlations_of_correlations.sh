
#This script generates a new file with calculated Spearman rank correlations for all data sets (estimated vs. real values)

set -o noclobber #prevent overwriting existing files
echo -e "File number \tFisher vs real \tUntransformed average vs real" > comparison_correlation_of_correlations.txt

for i in {1..100};
do
    echo "File$i"
    what_to_write=$(python3 spearman_correlation_of_correlations.py $i N) #Find correlation of correlations
    echo -e "$what_to_write" >> comparison_correlation_of_correlations.txt
done
    
