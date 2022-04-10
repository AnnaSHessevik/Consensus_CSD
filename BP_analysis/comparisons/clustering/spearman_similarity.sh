#This scripts calculates the correlation between BP or control Spearman rank correlation coefficient  sets to check the similarity
#between each set. 

set -o noclobber #prevent overwriting existing files

#Write header
echo -e "File1 \t File2 \t Corr of corrs" > comparison_ctrl_spearmans.txt #BP or ctrl depending on test

for file1 in spearman_ctrl_GSE*; #BP or ctrl depending on test
do
	for file2 in spearman_ctrl_GSE*; #BP or ctrl depending on test
	do
		#Follow script
		echo "$file1 and $file2"

		#Calculate correlation of correlations
		corr=$(python3 BP_spearman_comparison.py $file1 $file2 No None)

		#Write to file
		echo -e "$file1 \t $file2 \t $corr" >> comparison_ctrl_spearmans.txt #BP or ctrl depending on test
	done
done
