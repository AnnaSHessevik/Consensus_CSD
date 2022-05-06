#This script calculates Jaccard indexes between "true" correlations between gene pairs and subgroup correlations

python3 remove_minus_and_selfcorr.py spearman_not_sun_1000genes.txt 2 copy_spearman_not_sun_1000genes.txt #remove minus signs and self-correlations
sort -k 3gr copy_spearman_not_sun_1000genes.txt > numerically_sorted_spearman_not_sun_1000genes.txt #sort numerically
rm copy_spearman_not_sun_1000genes.txt #remove unnecessary copy

i=0 #counter

for file in spearman_subsample*; #Compare "correct" values with estimated values
do
    ((i++))
    echo "Loop number $i: $file" #follow the loop
    python3 remove_minus_and_selfcorr.py $file 2 "copy_$file" #remove self-correlations and minus in correlations
    
    sort -k 3gr copy_$file > numerically_sorted_$file #sort file numerically by backtransformed averages
    rm copy_$file #remove redundant file
    
    sample_size=$(python3 get_sample_size.py $file) #find correct sample size
    if (($sample_size > 9)) && (($sample_size < 20));
    then
	size_range="10-19"
    elif (($sample_size > 19)) && (($sample_size < 30));
    then
	size_range="20-29"
    elif (($sample_size > 29)) && (($sample_size < 40));
    then
	size_range="30-39"
    elif (($sample_size > 29)) && (($sample_size < 50));
    then
	size_range="40-49"
    else
	size_range="not_included"
    fi
    
    outfile="jaccard_subsample_size"$size_range"_"

    for j in 1 10 100 1000 10000 100000;
    do

	for k in 1 3 5 8;
	do
	    n=$[$j*$k]
	    echo "Number of gene pairs = $n"
	    python3 calculate_jaccard.py numerically_sorted_spearman_not_sun_1000genes.txt numerically_sorted_$file $n $outfile #Calculate jaccard index for correct vs. subsample values
	done
    done
    n=999000 #maximal number of gene pairs (excluding self-correlations)
    echo "Number of gene pairs = $n"
    python3 calculate_jaccard.py numerically_sorted_spearman_not_sun_1000genes.txt numerically_sorted_$file $n $outfile #Calculate jaccard index for correct vs. subsample values
    
    rm numerically_sorted_$file
    
done

rm numerically_sorted_spearman_not_sun_1000genes.txt


#Calculate means and standard deviations
echo "Calculation of mean and standard deviatons"
for j in 1 10 100 1000 10000 100000;
do
    for k in 1 3 5 8;
    do
	n=$[$j*$k]
	for size_range in "10-19" "20-29" "30-39" "40-49";
	do
	    echo "Sample size $size_range, n=$n"
	    python3 jaccard_mean_std.py "jaccard_subsample_size"$size_range"_"$n".txt" $n "summary_jaccards_subsample_size"$size_range".txt" #calculate mean and standard deviation for jaccard indexes
	done
    done
done

n=999000 #maximal number of gene pairs (excluding self-correlations)
for size_range in "10-19" "20-29" "30-39" "40-49";
do
    echo "Sample size $size_range, n=$n"
    python3 jaccard_mean_std.py "jaccard_subsample_size"$size_range"_"$n".txt" $n "summary_jaccards_subsample_size"$size_range".txt" #calculate mean and standard deviation for jaccard indexes
done


