#!/bin/bash
#For DHT11 model
#For DS18B20 model
SCRIPT="/home/pi/gadgetkeeper/read_temperature.py"
#For DHT22 model
#SCRIPT="/root/gadgetkeeper/Adafruit_DHT 22 4"
#For AM2302 model
#SCRIPT="/root/gadgetkeeper/Adafruit_DHT 2302 4"
TEMPRATURE=`$SCRIPT`
echo "$TEMPRATURE"
