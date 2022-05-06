#This script goes through all the subsample files and generates their corresponding spearman rank correlations using a slightly modified FindCorrAndVar.cpp.
#The sample size is given by the file not_sun_1000genes_sample_sizes.txt (not included at github)

ulimit -s unlimited #enable use of FindCorrAndVar.cpp
i=0 #counter

for file in not_sun_1000genes_subsample*; #go through all subsamples
do
	((i++))
	echo "Loop number $i: $file" #follow the loop
	sample_size=$(python3 get_sample_size.py $file)	 #find correct sample size
	subsample_number=${file:27} 	#identify subsample number
	output_filename="spearman_subsample$subsample_number" #name the output file
	
	#Run modified FindCorrAndVar
	g++ -O3 -o compile_subsample FindCorrAndVar_modified.cpp 
	./compile_subsample $file $output_filename $sample_size
done





