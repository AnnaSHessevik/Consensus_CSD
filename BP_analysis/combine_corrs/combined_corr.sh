#This script combines correlation coefficients

sample_type=ctrl #Specified by user, BP or ctrl

num_datasets=0  #do not change
sample_sizes="" #string of sample sizes, do not change
file_names="" #string of input files, do not change
output_file="combined_corr_ctrl.txt" #specified by user



for file in spearman_ctrl_*; #remember to change
do
	((num_datasets++))
	sample_size=$(python3 get_sample_size_BP.py sorted_$file $sample_type) #find sample size (2. argument is BP or ctrl depending on expression files)
	if [ $num_datasets -eq 1 ];
	then
		file_names="${file}"
		sample_sizes="${sample_size}"
        else
		file_names="${file_names}-${file}" #string of file names for each repetition, separated by -
		sample_sizes="${sample_sizes}-${sample_size}" #string of sample sizes separated by -
	fi
done

echo "$file_names"
echo "$sample_sizes"

python3 improved_fisher_transformation.py $num_datasets $sample_sizes $file_names $output_file
