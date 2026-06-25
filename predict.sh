mode=$1
name=$2

calc $1 $2

calc() {
    avg_window=14
    if test -f qxc/metric/status_$1; then
        let avg_window = $(cat qxc/metric/status_$1)
        count=`cat qxc/metric/find_best_$1_latest_003_$avg_window.txt | wc -l | awk '{print $1}'`
        if [ $count -lt 10 ]; then
            if [ $avg_window -lt 16 ]; then
                let avg_window = avg_window + 1
            else
                let avg_window = 14
            fi
            echo $avg_window > qxc/metric/status_$1
        fi
    else
        echo 14 > qxc/metric/status_$1
    fi
    nohup bash run.sh $mode $1 200,1500,5 latest $avg_window 0.03 $2 1 &
}
