ps -ef | grep "random" | grep -v grep | awk '{print $2}' | xargs -r kill -9
ps -ef | grep "latest" | grep -v grep | awk '{print $2}' | xargs -r kill -9
ps -ef | grep "custom" | grep -v grep | awk '{print $2}' | xargs -r kill -9
ps -ef | grep "67108864" | grep -v grep | awk '{print $2}' | xargs -r kill -9
