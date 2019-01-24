import time 
from math import pi
import matplotlib.pyplot as plt
import numpy as np
import csv
import json
import os 
import RPi.GPIO as GPIO
import time
import sys
import signal
from math import pi, fabs, cos, sin
from AlphaBot import AlphaBot
import multiprocessing

R = 0.034 # wheel radius (m) 6,6 cm 
T = 0.5
r = 0.0165  #wood wheel radious
L = 0.132   # distance between  wheels 
Ab = AlphaBot()


def main():
    a=[]
    d=[]
    x=[]
    y=[]
    l=[]
################### 30 anti gia 90 
    for k in range(30,101,5) :
        wr=wl = 0
        b=[]
        c=[]
        for i in range(0,5) :
            temp1 , temp2 = measurement(k)
            wr += temp1
            wl += temp2 
            Ab.stop()
            time.sleep(3)
        wr = wr /float(5) 
        wl = wl /float(5) 
        b = [wr,wl]
        c = [k,wr,wl]
        a.append(b)
        d.append(c)
        x.append(wr)
        y.append(wl)
        l.append(float(k))
        
        Ab.stop()
        time.sleep(3)
    
    

    t = np.arange(30.0, 101.0, 5)
    plt.plot(a)
    plt.xlabel('time (s)')
    plt.ylabel('voltage (mV)')
    plt.title('About as simple as it gets, folks')
    plt.grid(True)
    plt.savefig("test.png")
    plt.show()
    

    filename = "./statsclient"
    with open(filename, 'a') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        # If opened for the first time, insert header row
        if os.path.getsize(filename) == 0:
            wr.writerow(["k","wr","wl"])
        wr.writerows(d) 

#    A,B = curve_fit(f, l, x)[0] # your data x, y to fit
#    print str(A) ,str(B)
'''

    x = np.linspace(-100,100,100)
    y = A*x+B
    plt.plot(x, y, '-r', label='y=Ax+B')
    plt.title('Graph of y=2x+1')
    plt.xlabel('x', color='#1C2833')
    plt.ylabel('y', color='#1C2833')
    plt.legend(loc='upper left')
    plt.grid()
    plt.savefig("line.png")
    #plt.show()
'''

#def f(x, A, B): # this is your 'straight line' y=f(x)
#    return A*x + B



def measurement(k) : 
    Ab.setMotor(-k,k)
        
    #fork processes and grab results after T 
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    jobs = []
    p = multiprocessing.Process(target=right_velocity,args=(0,  return_dict))
    jobs.append(p)
    p.daemon=True
    p.start()
    k = multiprocessing.Process(target=left_velocity,args = ( 1 , return_dict))
    jobs.append(k)
    k.daemon=True
    k.start()
    
    time.sleep(T)
    p.terminate()
    k.terminate()
    p.join(T)
    k.join(T)
    print ("velocities and time: right-left: "+ str(return_dict.values()))
    
    wr = return_dict[0]
    wl = return_dict[1]
    dt = (return_dict[2]+return_dict[3])/2

    return wr,wl


def right_velocity(procnum, return_dict):
        DR = 8
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(DR,GPIO.IN,GPIO.PUD_UP)
        
        prev_status= 0
        changes = 0
        prev_time = time.time()
        while True:
            DR_status = GPIO.input(DR)
            if(DR_status == 0):
                if DR_status != prev_status:
                    prev_status = 0 
                    changes += 1
        
                    now_time = time.time()
                    dtime= now_time - prev_time
                    #print (str(dtime))
                    #print (str(changes))
                    w = (pi*changes)/(10* dtime) # s^2
                   
                    #print (str(w)+" 1 rad/s")
                    return_dict[procnum] = w #linear_velocity_right
                    return_dict[2] = dtime #linear_velocity_right
                   
            elif (DR_status == 1):
                if DR_status != prev_status:
                    prev_status = 1
        #linear_velocity_right = angular_velocity_right * R

def left_velocity(procnum, return_dict):
    DR = 7
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(DR,GPIO.IN,GPIO.PUD_UP)
    
    prev_status= 0
    changes = 0
    prev_time = time.time()
    while True:
        DR_status = GPIO.input(DR)
        if(DR_status == 0):
            if DR_status != prev_status:
                prev_status = 0 
                changes += 1
                
                now_time = time.time()
                dtime= now_time - prev_time
                #print (str(dtime))
                w = (pi*changes)/(10* dtime) # s^2
                #print (str(w)+" 2 rad/s")
                return_dict[procnum] = w #linear_velocity_right
                return_dict[3] = dtime #linear_velocity_right
        elif (DR_status == 1):
            if DR_status != prev_status:
                prev_status = 1
    



if __name__ == "__main__":
    main()

