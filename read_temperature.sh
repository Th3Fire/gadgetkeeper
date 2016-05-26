#!/bin/bash
#For DHT11 model
#For DS18B20
SCRIPT="/home/pi/gadgetkeeper/read_temperature.py"
#For DHT22 model
#SCRIPT="/root/gadgetkeeper/Adafruit_DHT 22 4" 
 
#For AM2302 model
#SCRIPT="/root/gadgetkeeper/Adafruit_DHT 2302 4"
TEMPRATURE=`$SCRIPT | grep "Temp" | awk -F " " '{print $3}'`
echo "$TEMPRATURE"
