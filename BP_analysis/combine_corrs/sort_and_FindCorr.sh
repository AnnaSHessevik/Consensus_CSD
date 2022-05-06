
#This script sorts gene expression files and goes through all expression data sets for bipolar disorder
# and calculates their corresponding Spearman rank correlations using a slightly modified FindCorrAndVar.cpp.
#Sample sizes are given in sample_sizes_BP.txt and samples_sizes_ctrl.txt (not provided at github)

ulimit -s unlimited #enable use of FindCorrAndVar.cpp
i=0 #counter

#Change following parameters, remember to also change for loop and output_filename
sample_type=ctrl #BP or ctrl
pos_accession_nr=12

for file in CSD_control_GSE80655*; #Depends on input (either CSD_bipolar_disorder_GSE* or CSD_control_GSE*)
do
	((i++))
	echo "Loop number $i: $file" #follow the loop
	(head -n 1 $file && tail -n +2 $file | sort) > sorted_$file #sort expression data set, but keep header
	sample_size=$(python3 get_sample_size_BP.py sorted_$file $sample_type) #find sample size (2. argument is BP or ctrl depending on expression files)
	accession_nr=${file:pos_accession_nr} #GEO accession number (with .txt) 
	output_filename=spearman_ctrl_$accession_nr #name of output file

	echo "$sample_size"
	echo "$accession_nr"
	echo "$output_filename"

	#Calculate spearman rank correlations
	g++ -O3 -o compile_BP FindCorrAndVar_modified.cpp
        ./compile_BP sorted_$file $output_filename $sample_size

done
