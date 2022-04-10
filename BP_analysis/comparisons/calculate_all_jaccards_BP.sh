#Calculate jaccard indexes between correlations based on Fisher's Z transformed values and weighted untransformed values

#Sort file 1
echo "Sort fisher file" #Follow progress 
python3 remove_minus_and_selfcorr.py fisher_ctrl.txt 2 copy_fisher_ctrl.txt #remove minus signs and self-correlations
sort -k 3gr copy_fisher_ctrl.txt > sorted_fisher_ctrl.txt #sort numerically
rm copy_fisher_ctrl.txt #remove unnecessary copy

#Sort file 2
echo "Sort arithmetic file" #Follow progress
python3 remove_minus_and_selfcorr.py arithmetic_ctrl.txt 2 copy_arithmetic_ctrl.txt #remove minus in arithmetric average
sort -k 3gr copy_arithmetic_ctrl.txt > sorted_arithmetic_ctrl.txt #sort file numerically by arithmetic averages
rm copy_arithmetic_ctrl.txt #remove redundant file 

#Calculate jaccard indexes at n number of gene pairs
for j in 1 10 100 1000 10000 100000 1000000;
do
    for k in 1 3 5 8;
    do
	n=$[$j*$k]
	echo "Number of gene pairs = $n"
	python3 calculate_jaccard_BP.py sorted_fisher_ctrl.txt sorted_arithmetic_ctrl.txt $n jaccard_ctrl.txt #Calculate jaccard index for fisher values vs arithmetic average
    done
done


n=9906756 #maximal number of gene pairs (excluding self-correlations)
echo "Number of gene pairs = $n"
python3 calculate_jaccard_BP.py sorted_fisher_ctrl.txt sorted_arithmetic_ctrl.txt $n jaccard_ctrl.txt #Calculate jaccard index for fisher vs. arithmetic when n = max_value
    	
#Remove redundant files
#rm sorted_fisher_ctrl.txt
#rm sorted_arithmetic_ctrl.txt




