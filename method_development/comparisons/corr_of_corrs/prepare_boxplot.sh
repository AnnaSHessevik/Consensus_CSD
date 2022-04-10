
echo -e "File name \t Spearman rank correlation coefficient" > correlation_subsamples10-19.txt
echo -e "File name \t Spearman rank correlation coefficient" > correlation_subsamples20-29.txt
echo -e "File name \t Spearman rank correlation coefficient" > correlation_subsamples30-39.txt
echo -e "File name \t Spearman rank correlation coefficient" > correlation_subsamples40-49.txt
echo -e "File name \t Spearman rank correlation coefficient" > correlations_not_included.txt


for file in spearman_subsample*;
do
    corr=$(python3 subsample_correlation_of_correlations.py $file N none) #Calculate correlation
    sample_size=$(python3 get_sample_size.py $file) #find correct sample size
    python3 write_corr2file.py $file $corr $sample_size #write correlation to file, this depends on the subsample size
done
