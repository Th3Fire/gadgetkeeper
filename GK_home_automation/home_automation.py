#!/usr/bin/python
 
try:
   import RPi.GPIO as GPIO
   import time
   import os
   import commands
   import picamera
 
   #Simply set these config values to 1 to enable monitoring
   enable_door_monitor = 1
   enable_window_monitor = 1
   enable_pir_monitor = 0
 
   #Change following values as necessary
   API_KEY = "b3eff99fe7624a6cb760f396db568fcf"
   THING_ID = "b8ff2e47233c11e69b064b58a7906d4e"
   DOOR_EVENT = "ccd5c37a233c11e69b064b58a7906d4e"
   WINDOW_EVENT = "374f743f233d11e69b064b58a7906d4e"
   MOTION_EVENT = 'd27bafbb233c11e69b064b58a7906d4e'
 
   URL = 'http://api.gadgetkeeper.com'
 
   #Sensor connected GPIO pin
   door_contact = 14
   window_contact = 15
   pir_contact = 18
   light_contact = 17
 
   GPIO.setmode(GPIO.BCM)
   GPIO.setup(door_contact,GPIO.IN)
   GPIO.setup(window_contact,GPIO.IN)
   GPIO.setup(pir_contact,GPIO.IN)
   GPIO.setup(light_contact,GPIO.OUT)
 
   prev_input_door = 1
   prev_input_window = 1
   prev_input_pir = 1
   shl_cmd= 'readlink -f $(dirname LKR0.00)'
   base_path = commands.getoutput(shl_cmd)
   img_base = base_path + '/images/'
   api_call_script = base_path + '/api_calls.sh'
 
   #Turn off the light at startup
   print 'Light: Off'
   #GPIO.output(light_contact,1)
   GPIO.output(light_contact,0)
 
   def capture_frame():
      cmd = 'date +"%Y-%m-%d_%H_%M"'
      date = commands.getoutput(cmd)
      with picamera.PiCamera() as cam:
         time.sleep(2)
         cam.capture(img_base + date + '.jpg')
         #time.sleep(5)
 
   #capture_frame()   #Test capture at startup
 
   while True:
     if(enable_door_monitor):
        input_door = GPIO.input(door_contact)
        if(input_door):
           if(not prev_input_door):
              print 'Door State: Open'
              prev_input_door = 1
              print 'Updating API'
              cmd = api_call_script+' '+API_KEY+' '+str(prev_input_door)+' '+URL+' '+THING_ID+' '+DOOR_EVENT
              #print cmd
              prog = commands.getoutput(cmd)
              print prog
        if(not input_door):
           if(prev_input_door):
              print 'Door State: Closed'
              prev_input_door = 0
              print 'Updating API'
              cmd = api_call_script+' '+API_KEY+' '+str(prev_input_door)+' '+URL+' '+THING_ID+' '+DOOR_EVENT
              #print cmd
              prog = commands.getoutput(cmd)
              print prog
        time.sleep(0.05)
     if(enable_window_monitor):
        input_window = GPIO.input(window_contact)
        if(input_window):
           if(not prev_input_window):
              print 'Window State: Open'
              prev_input_window = 1
              print 'Updating API'
              cmd = api_call_script+' '+API_KEY+' '+str(prev_input_window)+' '+URL+' '+THING_ID+' '+WINDOW_EVENT
              #print cmd
              prog = commands.getoutput(cmd)
              print prog
        if(not input_window):
           if(prev_input_window):
              print 'Window State: Closed'
              prev_input_window = 0
              print 'Updating API'
              cmd = api_call_script+' '+API_KEY+' '+str(prev_input_window)+' '+URL+' '+THING_ID+' '+WINDOW_EVENT
              #print cmd
              prog = commands.getoutput(cmd)
              print prog
        time.sleep(0.05)
     if(enable_pir_monitor):
        input_pir = GPIO.input(pir_contact)
        if(input_pir):
           if(not prev_input_pir):
              print 'Motion: Detected'
              prev_input_pir = 1
              capture_frame() #capture the image
              print 'Updating API'
              cmd = api_call_script+' '+API_KEY+' '+str(prev_input_pir)+' '+URL+' '+THING_ID+' '+MOTION_EVENT
              #print cmd
              prog = commands.getoutput(cmd)
              print prog
              print 'Light: ON'
              GPIO.output(light_contact,1) # Turn ON the Light
              time.sleep(5)
        if(not input_pir):
           if(prev_input_pir):
              print 'Motion: Not Detected'
              prev_input_pir = 0
              print 'Updating API'
              cmd = api_call_script+' '+API_KEY+' '+str(prev_input_pir)+' '+URL+' '+THING_ID+' '+MOTION_EVENT
              #print cmd
              prog = commands.getoutput(cmd)
              print prog
              print 'Light: Off'
              GPIO.output(light_contact,0) # Turn OFF the Light
        time.sleep(0.05)
except KeyboardInterrupt:
   GPIO.cleanup() 
