avg_window=$1
name=$2
nohup bash run.sh 5 35,2500,5 latest $avg_window 0.03 "$name" 0 EMA_STATE 0.1 &
nohup bash run.sh 5 30,2500,5 latest $avg_window 0.06 "$name" 0 EMA_STATE 0.1 &
nohup bash run.sh 4 25,2500,5 latest $avg_window 0.01 "$name" 0 EMA_STATE 0.1 &
nohup bash run.sh 4 35,2500,5 latest $avg_window 0.03 "$name" 0 EMA_STATE 0.1 &
nohup bash run.sh 4 20,2500,5 latest $avg_window 0.05 "$name" 0 EMA_STATE 0.1 &
nohup bash run.sh 4 30,2500,5 latest $avg_window 0.07 "$name" 0 EMA_STATE 0.1 &
nohup bash run.sh 4 15,2500,5 latest $avg_window 0.04 "$name" 0 EMA_STATE 0.1 &
