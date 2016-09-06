#! /usr/bin/python
# This file is used to post GPS data to dweet.io via GPSD.
# To run this file please install necessary components as follows
# sudo apt-get install -y gpsd gpsd-clients python-gps
# Then simulate GPS via gpsfake -o -n -c 0.1 gpslogs.txt   

import os
from gps import *
from time import *
import time
import threading
import dweepy
 
gpsd = None #seting the global variable
sender = 'iotify-demo'

myDweet = {}  

if sender == 'iotify-demo': 
    print("Please replace sender with something else")
    exit()

print("Your GPS dashboard is available at https://dweet.io/follow/"+sender)
    
os.system('clear') #clear the terminal (optional)
 
class GPSMain(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd 
    gpsd = gps(mode=WATCH_ENABLE) 
    self.current_value = None
    self.running = True 
 
  def run(self):
    global gpsd
    while gpsp.running:
      gpsd.next() 
 
if __name__ == '__main__':
  gpsp = GPSMain() 
  try:
    gpsp.start()
    while True:
      os.system('clear')
      myDweet['latitude'] = gpsd.fix.latitude
      myDweet['longitude'] = gpsd.fix.longitude
      print
      print ' GPS Statistics'
      print '----------------------------------------'
      print 'latitude    ' , gpsd.fix.latitude
      print 'longitude   ' , gpsd.fix.longitude
      print 'time utc    ' , gpsd.utc,' + ', gpsd.fix.time
      print 'altitude (m)' , gpsd.fix.altitude
      print 'speed (m/s) ' , gpsd.fix.speed
      print '----------------------------------------'

      dweepy.dweet_for(sender, myDweet );  
      time.sleep(3) #set to whatever
 
  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    gpsp.running = False
    gpsp.join() # wait for the thread to finish what it's doing
  print "Done.\nExiting."
