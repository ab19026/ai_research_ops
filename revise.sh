revise_items=(
  "20261018:3"
  "20261018:4"
  "20261018:6"
  "20261016:3"
  "20261016:4"
  "20261013:2"
  "20261013:3"
  "20261013:6"
  "20261011:2"
  "20261011:3"
  "20261011:4"
  "20261009:2"
  "20261009:3"
  "20261009:4"
)

index=0
length=${#revise_items[@]}
avg_window=14
while true; do
  run=`ps -ef | grep latest`
  if [[ ! $run =~ "67108864" ]]; then
    item="${revise_items[$index]}"
    IFS=':' read -r targetdate labelpos <<< "$item"
    nohup bash run_history.sh $labelpos 50,2500,5 latest $avg_window 0.025 qxc 0 EMA_STATE 0.1 $targetdate &
    nohup bash run_history.sh $labelpos 55,2500,5 latest $avg_window 0.035 qxc 0 EMA_STATE 0.1 $targetdate &
    nohup bash run_history.sh $labelpos 60,2500,5 latest $avg_window 0.065 qxc 0 EMA_STATE 0.1 $targetdate &
    if (( index == length - 1 )); then
      index=0
      ((avg_window++))
      if (( avg_window > 16 )); then
        avg_window=14
      fi
    else
      ((index++))
    fi
  else
    echo "WAIT FOR CUSTOME"
  fi
  sleep 15
done
