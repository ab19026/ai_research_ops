count=0
name=$1
avg_window=14
rm -rf $name/metric/*
while [ $count -lt 5 ]
do
    run=`ps -ef | grep latest`
    if [[ ! $run =~ "67108864" ]]; then
        rm -rf *.h5
        # if test -f $name/metric/crt_avg_win; then
        #     let avg_window=$(cat $name/metric/crt_avg_win)
        #     if [ $avg_window -lt 16 ]; then
        #         let avg_window=avg_window+1
        #     else
        #         let avg_window=14
        #     fi
        #     echo $avg_window > $name/metric/crt_avg_win
        # else
        #     echo 14 > $name/metric/crt_avg_win
        # fi
        if [[ "$name" == qxc ]]; then
            nohup bash run.sh 0 200,1500,5 latest "$avg_window" 0.03 "$name" 1 &
            nohup bash run.sh 1 200,1500,5 latest "$avg_window" 0.03 "$name" 1 &
            nohup bash run.sh 2 200,1500,5 latest "$avg_window" 0.03 "$name" 1 &
            nohup bash run.sh 3 200,1500,5 latest "$avg_window" 0.03 "$name" 1 &
            nohup bash run.sh 4 200,1500,5 latest "$avg_window" 0.03 "$name" 1 &
            nohup bash run.sh 5 200,1500,5 latest "$avg_window" 0.03 "$name" 1 &
            nohup bash run.sh 6 200,1500,5 latest "$avg_window" 0.03 "$name" 1 &
        elif [[ "$name" == qxc_full ]]; then
            nohup bash run.sh 0 245,1500,5 latest "$avg_window" 0.03 "$name" 0 &
            nohup bash run.sh 1 235,1500,5 latest "$avg_window" 0.03 "$name" 0 &
            nohup bash run.sh 2 215,1500,5 latest "$avg_window" 0.03 "$name" 0 &
            nohup bash run.sh 3 260,1500,5 latest "$avg_window" 0.03 "$name" 0 &
            nohup bash run.sh 4 220,1500,5 latest "$avg_window" 0.03 "$name" 0 &
            nohup bash run.sh 5 200,1500,5 latest "$avg_window" 0.03 "$name" 0 &
            nohup bash run.sh 6 200,1500,5 latest "$avg_window" 0.03 "$name" 0 &
        elif [[ "$name" == pls_full ]]; then
            rm -rf *.bak
            if [ -d "$name/metric" ] && [ "$(ls $name/metric)" ]; then
                dt=$(head -n1 pls_future | awk '{print $1}' | tr -d '-')
                if [ -d "$name/$dt" ] && [ "$(ls $name/$dt)" ]; then
                    python3 base.py MERGE 0 $name $dt metric
                    python3 base.py MERGE 1 $name $dt metric
                    python3 base.py MERGE 2 $name $dt metric
                    rm -rf $name/metric/*
                else
                    mkdir $name/$dt
                    mv $name/metric/* $name/$dt
                fi
            fi
            head -n 1 pls_future >> pls_raw_txt && sed -i '.bak' '1d' pls_future
            # nohup bash run.sh 0 200,1500,5 latest "$avg_window" 0.03 "$name" 0 &
            # nohup bash run.sh 0 210,1500,5 latest "$avg_window" 0.04 "$name" 0 &
            # nohup bash run.sh 0 220,1500,5 latest "$avg_window" 0.05 "$name" 0 &
            # nohup bash run.sh 0 230,1500,5 latest "$avg_window" 0.06 "$name" 0 &
            nohup bash run.sh 0 200,1500,5 latest 15 0.03 "$name" 0 &
            nohup bash run.sh 0 210,1500,5 latest 16 0.03 "$name" 0 &
            nohup bash run.sh 1 220,1500,5 latest 14 0.03 "$name" 0 &
            nohup bash run.sh 1 230,1500,5 latest 16 0.03 "$name" 0 &
            nohup bash run.sh 2 200,1500,5 latest 14 0.03 "$name" 0 &
            nohup bash run.sh 2 210,1500,5 latest 15 0.03 "$name" 0 &
            nohup bash run.sh 2 220,1500,5 latest 16 0.03 "$name" 0 &
        fi
    else
        echo "WAIT FOR CUSTOME"
    fi
    sleep 10
done
