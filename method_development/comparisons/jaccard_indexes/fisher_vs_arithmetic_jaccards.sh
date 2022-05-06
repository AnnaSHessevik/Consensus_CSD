#This script calculates Jaccard indexes between correlation coefficient based on Fisher's Z transformed and weighted untransformed averages.

i=0 #counter

for file in combined_spearman_not_sun*; #Compare "correct" values with estimated values
do
    ((i++))
    echo "Loop number $i: $file" #follow the loop
    python3 remove_minus_and_selfcorr.py $file -1 "copy_$file" #remove minus in arithmetric average
    python3 remove_minus_and_selfcorr.py "copy_$file" -2 "no_minus_$file" #remove minus in backtransformed average
    rm copy_$file #remove redundant file
    sort -k 3gr no_minus_$file > sorted_fisher_$file #sort file numerically by backtransformed averages
    sort -k 4gr no_minus_$file > sorted_arithmetic_$file #sort file numerically by arithmetic averages
    rm no_minus_$file #remove redundant file 

    #Calculate jaccard indexes at n number of gene pairs
    for j in 1 10 100 1000 10000 100000;
    do

	for k in 1 3 5 8;
	do
	    n=$[$j*$k]
	    echo "Number of gene pairs = $n"
	    python3 calculate_jaccard.py sorted_fisher_$file sorted_arithmetic_$file $n jaccard_fisher_vs_arithmetic #Calculate jaccard index for fisher vs. arithmetic values	    
	    
	done
    done

    n=999000 #maximal number of gene pairs (excluding self-correlations)
    echo "Number of gene pairs = $n"
    python3 calculate_jaccard.py sorted_fisher_$file sorted_arithmetic_$file $n jaccard_fisher_vs_arithmetic #Calculate jaccard index for fisher vs. arithmetic values

    #Remove redundant files
    rm sorted_fisher_$file
    rm sorted_arithmetic_$file
done




#Calculate means and standard deviations
echo "Calculation of mean and standard deviatons"
i=0
for j in 1 10 100 1000 10000 100000;
do

    for k in 1 3 5 8;
    do
	n=$[$j*$k]
	echo "Number of gene pairs = $n"
	python3 jaccard_mean_std.py jaccard_fisher_vs_arithmetic$n.txt $n summary_jaccard_fisher_vs_arithmetic.txt #calculate mean and standard deviation for jaccard indexes
    done
done

n=999000 #maximal number of gene pairs (excluding self-correlations)
echo "Number of gene pairs = $n"
python3 jaccard_mean_std.py jaccard_fisher_vs_arithmetic$n.txt $n summary_jaccard_fisher_vs_arithmetic.txt #calculate mean and standard deviation for jaccard indexes based on fisher transformed correlations

