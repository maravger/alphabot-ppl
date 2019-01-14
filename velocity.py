import RPi.GPIO as GPIO
import time
import sys
import signal
from math import pi
from AlphaBot import AlphaBot
import multiprocessing

R = 0.034 # wheel radius (m) 6,6 cm  
Ab = AlphaBot()

def signal_handler(sig, frame):
        #print('You pressed Ctrl+C!')
        Ab.stop()
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
#print('Press Ctrl+C')
#signal.pause()

def main():
    start_time = time.time()
    right_speed = int(sys.argv[1])
    left_speed = int(sys.argv[2])
    Ab.setMotor(right_speed,left_speed)
    #while True:
        

    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    jobs = []


    p = multiprocessing.Process(target=right_velocity,args=(0, start_time,  return_dict))
    jobs.append(p)
    p.start()
        
    k = multiprocessing.Process(target=left_velocity,args = (1 , start_time, return_dict))
    jobs.append(k)
    k.start()

    p.join()
    k.join()
    print ("linear velocity left"+ str(return_dict.values()))
        #print ("linear velocity left"+ str(k))


    ####
        #u_r = right_velocity()
        #print ("\nright "+ str(u_r))
        #u_l = left_velocity()
        #print ("\nright "+ str(u_r))
        #print ("\nleft  " + str(u_l))
        #time.sleep(0.2)
    end_time = time.time()
    x = end_time - start_time 
    print str(x)
    #time.sleep(1-x)
    Ab.stop()
    

def right_velocity(procnum, prev_time, return_dict):
    DR = 8
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(DR,GPIO.IN,GPIO.PUD_UP)
    
    prev_status= 0
    changes = 0
    while True:
        DR_status = GPIO.input(DR)
        if(DR_status == 0):
            if DR_status != prev_status:
                prev_status = 0 
                changes += 1
                if (changes == 20) :
                    changes = 0
                    now_time = time.time()
                    #print (str(now_time))
                    dtime= now_time - prev_time

                    prev_time = time.time()
                    print (str(dtime))
                    w = 2*pi  / dtime # s^2
                    #print (str(w) + " rad/s")
                    u = R * w # cm
                    #u = u / 100
                    print (str(u)+" m/s")
                    return_dict[procnum] = u #linear_velocity_right
                    break ; 
        elif (DR_status == 1):
            if DR_status != prev_status:
                prev_status = 1
    #linear_velocity_right = angular_velocity_right * R

def left_velocity(procnum, prev_time, return_dict):
    DR = 7
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(DR,GPIO.IN,GPIO.PUD_UP)
    
    prev_status= 0
    changes = 0
    while True:
        DR_status = GPIO.input(DR)
        if(DR_status == 0):
            if DR_status != prev_status:
                prev_status = 0 
                changes += 1
                if changes == 20 :
                    changes =0
                    dtime=float(time.time())-float(prev_time)
                    prev_time = time.time()
                    print (str(dtime))
                    w = 2*pi  / dtime # s^2
                    #print (str(w) + " rad/s")
                    u = R * w # cm
                    #u = u / 100
                    print (str(u)+" m/s")
                    return_dict[procnum] = u #linear_velocity_left 
                    break ; 
        elif (DR_status == 1):
            if DR_status != prev_status:
                prev_status = 1
    #linear_velocity_left = angular_velocity_left * R



if __name__ == "__main__":
    main()

