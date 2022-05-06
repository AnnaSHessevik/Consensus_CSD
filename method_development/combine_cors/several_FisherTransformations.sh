#This script goes through all the Spearman rank correlation coefficient files and
#generates combined coefficients for each repition.
#The sample size is given by the file not_sun_1000genes_sample_sizes.txt (not provided at github)


for rep in {1..100}; #Controls number of repetitions
do
	num_datasets=0 #initialization number of data sets in each repetition
	sample_size="" #string of sample sizes
	file_names="" #string of input files
	output_file="combined_spearman_not_sun${rep}.txt"

	for file in spearman_subsample${rep}_*; #go through all subsamples
	do
		((num_datasets++))
		subsample_size=$(python3 get_sample_size.py $file) #find correct sample size

		if [ $num_datasets -eq 1 ];
		then
			file_names="${file}"
			sample_size="${subsample_size}"
		else
			file_names="${file_names}-${file}" #string of file names for each repetition, separated by -
			sample_size="${sample_size}-${subsample_size}" #string og sample sizes separated by -
		fi
	done

	echo "Loop number $rep: Generating $output_file"
	#echo "$num_datasets"
	#echo "$sample_size"
	#echo "$file_names"
	#echo "$output_file"
	python3 improved_fisher_transformation.py $num_datasets $sample_size $file_names $output_file


done






