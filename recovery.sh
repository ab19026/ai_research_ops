avg_window=$1
name=$2
nohup bash run.sh 3 35,1500,5 latest $avg_window 0.02 "$name" 0 EMA_STATE 0.1 &
nohup bash run.sh 3 30,1500,5 latest $avg_window 0.04 "$name" 0 EMA_STATE 0.1 &
nohup bash run.sh 3 25,1500,5 latest $avg_window 0.07 "$name" 0 EMA_STATE 0.1 &
nohup bash run.sh 3 1200,2500,5 latest $avg_window 0.02 "$name" 0 EMA_STATE 0.1 &
nohup bash run.sh 3 1210,2500,5 latest $avg_window 0.05 "$name" 0 EMA_STATE 0.1 &
nohup bash run.sh 3 1300,2500,5 latest $avg_window 0.08 "$name" 0 EMA_STATE 0.1 &
nohup bash run.sh 4 20,1200,5 latest $avg_window 0.03 "$name" 0 EMA_STATE 0.1 &
