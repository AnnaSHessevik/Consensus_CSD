
i=1
for file in combined_spearman_not_sun*;
do
    echo "Loop number $i: $file" 
    python3 calculate_rmse.py $file Y -2 rmse_fisher.txt
    python3 calculate_rmse.py $file Y -1 rmse_arithmetic_average.txt
    ((i++))
done
