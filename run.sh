label_dim=$1
data_len=$2
metric_mode=$3
avg_window=$4
drop_rate=$5
name=$6
shrink=$7
smooth_mode=$8
count=0
IFS=',' read scope0 scope1 scope2 <<< "$data_len"
for ((l=scope0; l <= scope1; l += scope2)); do
    python 67108864.py MODE_FIND "$shrink" "${label_dim},${l}" "$metric_mode" "$avg_window" "$drop_rate" "$name" "$smooth_mode"
done

