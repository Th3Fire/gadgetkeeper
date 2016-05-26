#!/bin/bash
#replace the api_key
API_KEY="17cbbd53be8a42808c1d524df80501dc"
#replace the thing_id
THING_ID="a144b64e231c11e69b064b58a7906d4e"
#replace the property_id
PROPERTY_ID="b7d56271231c11e69b064b58a7906d4e"
URL="http://api.gadgetkeeper.com"
TMP_FILE="/tmp/tmp.txt"
  
curl -i -X GET -H "X-ApiKey: $API_KEY" "$URL/v1/things/$THING_ID/properties/$PROPERTY_ID/value.json" > "$TMP_FILE" 2> /dev/null
if [ -f "$TMP_FILE" ]; then
    IS_OK=`cat "$TMP_FILE" | head -1 | grep "200 OK"`
    #echo $IS_OK
    #cat "$TMP_FILE" | head -1
    if [ "$IS_OK" != "" ]; then
        RESULT=`cat "$TMP_FILE" | tail -1`
        echo Value: $RESULT
    else
        echo "Error"
        cat "$TMP_FILE" | head -1
    fi
    #rm -f "$TMP_FILE"
else
    echo "Error"
fi
