label_dim=$1
data_len=$2
metric_mode=$3
avg_window=$4
drop_rate=$5
name=$6
shrink=$7
smooth_mode=$8
smooth_alpha=$9
target_date=${10}
count=0

# echo $label_dim
# echo $data_len
# echo $metric_mode
# echo $avg_window
# echo $drop_rate
# echo $name
# echo $shrink
# echo $smooth_mode
# echo $smooth_alpha
# echo $target_date

IFS=',' read scope0 scope1 scope2 <<< "$data_len"
for ((l=scope0; l <= scope1; l += scope2)); do
    python 67108864.py MODE_FIND "$shrink" "${label_dim},${l}" "$metric_mode" "$avg_window" "$drop_rate" "$name" "$smooth_mode" "$smooth_alpha" "$target_date"
done

