#Calculate root mean square error for Spearman rank correlation coefficients from subsample data sets

i=1
for file in spearman_subsample*;
do
    echo "Loop number $i: $file" #Follow loop
    sample_size=$(python3 get_sample_size.py $file) #find correct sample size

    #Define output file dependent on sample size
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

    outfile="rmse_subsample_size"$size_range".txt"
    
    python3 calculate_rmse.py $file N 2 $outfile #Calculate rmse
    
    ((i++))
done
