name=$1
count=0
while [ $count -lt 5 ]
do
    echo "WAIT FOR LATEST"
    sleep 10
    week=$(date +%u)
    if [ "$week" == 2 ] || [ "$week" == 5 ] || [ "$week" == 7 ]; then
        current_hour=$(date +"%H")
        if [ "$current_hour" == 14 ]; then
            mode=$(python get_latest.py $name)
            if [ "$mode" == FIXED ] || [ "$mode" == FIND ]; then
                ps -ef | grep "custom" | grep -v grep | awk '{print $2}' | xargs -r kill -9
                ps -ef | grep "latest" | grep -v grep | awk '{print $2}' | xargs -r kill -9
                ps -ef | grep "random" | grep -v grep | awk '{print $2}' | xargs -r kill -9
                ps -ef | grep "67108864" | grep -v grep | awk '{print $2}' | xargs -r kill -9
                rm -rf $name/metric/*
                nohup bash custom.sh $name &
            fi
            break
        fi
    fi
done

echo "PLEASE MANUALLY SCHEDULE THIS IN ANOTHER DAY"
