# External module imports
import RPi.GPIO as GPIO
import time
import dweepy
from sht21 import SHT21

sender = 'iotify-demo'
# Pin Definitons:
doorSensor = 7 # Broadcom pin 18 (P1 pin 12)
windowSensor = 8 # Broadcom pin 23 (P1 pin 16)
alarmOut = 9 # Broadcom pin 22 (P1 pin 15)
myDweet = {}  

if sender == 'iotify-demo': 
    print("Please replace sender with something else")
    exit()

# Pin Setup:
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
print("Setting Output")
GPIO.setup(alarmOut, GPIO.LOW) # LED pin set as output

print("Setting Input")
GPIO.setup(doorSensor, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Button pin set
GPIO.setup(windowSensor, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Button pin set
sht = SHT21(1)

print("Your dashboard is available at https://dweet.io/follow/"+sender)
time.sleep(1.0)
alarm = False


# Initial state for LEDs:
GPIO.output(alarmOut, GPIO.LOW)


print("Here we go! Press CTRL+C to exit")
try:
    while 1:
        alarm = False
        myDweet['DoorAlarm'] = False 
        myDweet['WindowAlarm'] = False 
        myDweet['FireAlarm'] = False
        myDweet['WaterAlarm'] = False 

        if GPIO.input(doorSensor): # button is released
            myDweet['DoorAlarm'] = True 
            alarm = True
        if GPIO.input(windowSensor): # button is released
            myDweet['WindowAlarm'] = True 
            alarm = True
        if sht.read_temperature() > 100: #excessive heat
            myDweet['FireAlarm'] = True 
            alarm = True
        if sht.read_humidity() > 80: #abnormal humidity
            myDweet['WaterAlarm'] = True 
            alarm = True
    
        if alarm:
            GPIO.output(alarmOut, GPIO.HIGH)
        else:
            GPIO.output(alarmOut, GPIO.LOW)
            
        time.sleep(1) 
        dweepy.dweet_for(sender, myDweet );  
except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
    GPIO.cleanup() # cleanup all GPIO
