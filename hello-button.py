# External module imports
import RPi.GPIO as GPIO
import time

print("Hello Button")

buttonPin = 9
prevButtonState = True
buttonState = True

print("Setting Broadcom Mode")
# Pin Setup:
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme

GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
time.sleep(0.5) 

#print initial settings
buttonState = GPIO.input(buttonPin);
print "Initial state is ", 'pressed' if buttonState else 'released';

try:
    while 1:
        buttonState = GPIO.input(buttonPin);
        if prevButtonState != buttonState:
            print "Button is ", 'pressed' if buttonState else 'released';
        # save last state
        prevButtonState = buttonState;    
        time.sleep(0.1) 
except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
    GPIO.cleanup() # cleanup all GPIO
