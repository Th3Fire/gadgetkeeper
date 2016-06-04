#!/usr/bin/python
 
import time
import mosquitto
import random
import commands
 
###############################################
 
# change this thing ID as required 
THING_ID="a144b64e231c11e69b064b58a7906d4e"
BROKER_NAME="api.gadgetkeeper.com"
 
###############################################
 
topic = 'thing.' + THING_ID
broker = BROKER_NAME
client_name = "device-1"
last_id = ""
 
def on_message(mosq, obj, msg):
    global last_id
    print 'Request: ' +  msg.payload
    id,jsn,cmd = msg.payload.split(',', 2 );
    #print id
    #print jsn
    #print cmd
    if last_id == id:
        print 'Update successful'
        return
    last_id = id
    #data_val = 20.00
    #data_val = random.uniform(1.5, 100.9) #genarate random value for testing
    #read temperature from the sensor 
    shl_cmd = '/home/pi/gadgetkeeper/read_temperature.sh'
    #read humidity from the sensor
    #shl_cmd = '/root/gadgetkeeper/read_humidity.sh'
    data_val = commands.getoutput(shl_cmd)
    if data_val:
        print 'Sensor reading: ' + data_val
    else:
        time.sleep(2) #delay 2s and try again
        data_val = commands.getoutput(shl_cmd)
    if data_val:
        print 'Sensor reading: ' + data_val
    else:
        data_val = -1000.0 # If sensor reading fails assign this value
        print 'Sensor read error'
    reply_msg = id + ',' + jsn + ',' + "\"result\":" + str(data_val) + '}'
    print 'Response: ' + reply_msg
    #client_rply = mosquitto.Mosquitto("device-1")
    #client_rply.connect(broker)
    #client_rply.publish(topic, reply_msg ,0) 
 
    reply_msg_new = reply_msg.replace('"', '\\"')
    shl_cmd = '/usr/local/bin/mosquitto_pub  -h ' + broker + ' -p  1883 -t ' + topic + ' -m "' + reply_msg_new + '"'
    #print shl_cmd
    reply_prog = commands.getoutput(shl_cmd)
 
client = mosquitto.Mosquitto(client_name)
client.connect(broker)
client.subscribe(topic,0)
client.on_message = on_message
while True:
    client.loop(15)
    time.sleep(2)
