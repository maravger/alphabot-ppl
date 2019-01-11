import RPi.GPIO as GPIO
import time 
from math import pi
from AlphaBot import AlphaBot
DR = 7

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(DR,GPIO.IN,GPIO.PUD_UP)
Ab = AlphaBot()

prev_status= 0
changes = 0
prev_time = time.time()
while True:
    Ab.setMotor(40,40)
    #Ab.forward()
    #time.sleep(1)
    DR_status = GPIO.input(DR)
    #print DR_status
    
    if(DR_status == 0):
        #print("kouniemai")
        #if DR_status == prev_status :
            #print ("keno")
        if DR_status != prev_status:
            prev_status = 0 
            print ("kouniemai")
            changes += 1
            if changes == 20 :
                changes =0
                #print (str(time.time())) 
                #print (str(prev_time))
                dtime=float(time.time())-float(prev_time)
                prev_time = time.time()
                print ("kuklos")
                print (str(dtime))
                w = 2*pi  / dtime # s^2
                w = w 
                print (str(w) + " rad/s")
                u = 6.6 * w # cm
                u = u / 100
                print (str(u)+" m/s")
        #print str(prev_status)
    elif (DR_status == 1):
        #print("den kouniemai")
        #if DR_status == prev_status :
            #print ("ksilo")
        if DR_status != prev_status:
            prev_status = 1
            #print ("stekomai")
        #print str(prev_status)
    #Ab.right()
    #time.sleep(2)
