#This script calculates Jaccard indexes between "true" correlations between gene pairs and estimated correlations.

python3 remove_minus_and_selfcorr.py spearman_not_sun_1000genes.txt 2 copy_spearman_not_sun_1000genes.txt #remove minus signs and self-correlations
sort -k 3gr copy_spearman_not_sun_1000genes.txt > sorted_numerically_spearman_not_sun_1000genes.txt #sort numerically
rm copy_spearman_not_sun_1000genes.txt #remove unnecessary copy

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
	    python3 calculate_jaccard.py sorted_numerically_spearman_not_sun_1000genes.txt sorted_fisher_$file $n jaccard_fisher #Calculate jaccard index for correct vs. fisher values	    
	    python3 calculate_jaccard.py sorted_numerically_spearman_not_sun_1000genes.txt sorted_arithmetic_$file $n jaccard_arithmetic #Caluclate jaccard index for correct vs. arritmetric values
	    
	done
    done

    n=999000 #maximal number of gene pairs (excluding self-correlations)
    echo "Number of gene pairs = $n"
    python3 calculate_jaccard.py sorted_numerically_spearman_not_sun_1000genes.txt sorted_fisher_$file $n jaccard_fisher #Calculate jaccard index for correct vs. fisher values
    python3 calculate_jaccard.py sorted_numerically_spearman_not_sun_1000genes.txt sorted_arithmetic_$file $n jaccard_arithmetic #Caluclate jaccard index for correct vs. arithmetic values
    	
    #Remove redundant files
    rm sorted_fisher_$file
    rm sorted_arithmetic_$file
done

#Remove redundant file
rm sorted_numerically_spearman_not_sun_1000genes.txt



#Calculate means and standard deviations
echo "Calculation of mean and standard deviatons"
i=0
for j in 1 10 100 1000 10000 100000;
do

    for k in 1 3 5 8;
    do
	n=$[$j*$k]
	echo "Number of gene pairs = $n"
	python3 jaccard_mean_std.py jaccard_fisher$n.txt $n summary_fisher_jaccards.txt #calculate mean and standard deviation for jaccard indexes based on fisher transformed correlations
	python3 jaccard_mean_std.py jaccard_arithmetic$n.txt $n summary_arithmetic_jaccards.txt #calucalte mean and standad deviation for jaccard indexes based on arithmetic averages of correlations
    done
done

n=999000 #maximal number of gene pairs (excluding self-correlations)
echo "Number of gene pairs = $n"
python3 jaccard_mean_std.py jaccard_fisher$n.txt $n summary_fisher_jaccards.txt #calculate mean and standard deviation for jaccard indexes based on fisher transformed correlations
python3 jaccard_mean_std.py jaccard_arithmetic$n.txt $n summary_arithmetic_jaccards.txt #calucalte mean and standad deviation for jaccard indexes based on arithmetic averages of correlations
