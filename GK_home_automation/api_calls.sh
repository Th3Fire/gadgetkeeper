#!/bin/bash
if [ "$1" != "" ] && [ "$2" != "" ] && [ "$3" != "" ] && [ "$4" != "" ] && [ "$5" != "" ]; then
        API_KEY="$1"
        MSG="$2"
        URL="$3"
        THING_ID="$4"
        EVENT_ID="$5"
else
        echo "Missing Arguments"
        exit   
fi
CUR_DATE=$(date +%FT%T.%NZ)
TMP_FILE="/tmp/tmp.txt"
curl -i -X POST -H "X-ApiKey: $API_KEY" -H "Content-Type: text/json; charset=UTF-8" -d \
'[{"value":'$MSG',"at":"'$CUR_DATE'"}]' $URL"/v1/things/$THING_ID/events/$EVENT_ID/datapoints.json" > "$TMP_FILE" 2> /dev/null
if [ -f "$TMP_FILE" ]; then
        RESPONSE=`cat "$TMP_FILE" | head -1`
        IS_OK=`echo "$RESPONSE" | grep "HTTP/1.1 204"`
        #echo -n "Value updated "
        if [ "$IS_OK" != "" ]; then
                echo "OK"
        else
                echo "FAIL"
                echo "$RESPONSE"
        fi
else
        echo "Error"
fi
