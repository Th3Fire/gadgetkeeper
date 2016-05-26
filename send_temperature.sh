#!/bin/bash 
 
#For DHT11 model
#For DS18B20 model
SCRIPT="/home/pi/gadgetkeeper/read_temperature.py"
#For DHT22 model
#SCRIPT="/root/gadgetkeeper/Adafruit_DHT 22 4"
#For AM2302 model
#SCRIPT="/root/gadgetkeeper/Adafruit_DHT 2302 4"
#TEMPRATURE=`$SCRIPT | grep "Temp" | awk -F " " '{print $3}'`
TRY=1
while [ $TRY -le 5 ]
do
    TEMPRATURE=`$SCRIPT | grep "Temp" | awk -F " " '{print $3}'`
    if [ "$TEMPRATURE" != "" ]; then
        echo "Current temperature: $TEMPRATURE"
        /home/pi/gadgetkeeper/set_value.sh "$TEMPRATURE"
        exit 0
    else
        echo "Retry after 2s"
        sleep 2
        TRY=`expr $TRY + 1`
    fi
done
