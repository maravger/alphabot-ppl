import RPi.GPIO as GPIO
import time
import sys
import signal
from math import pi, fabs, cos, sin
from AlphaBot import AlphaBot
import multiprocessing

R = 0.034 # wheel radius (m) 6,6 cm 
T = 0.2
r = 0.0165  #wood wheel radious
L = 0.132   # distance between  wheels 
Ab = AlphaBot()
e = 0.1
wmax = 50
wmin= 50
#def signal_handler(sig, frame):
        #print('You pressed Ctrl+C!')
#        Ab.stop()
#        sys.exit(0)
#signal.signal(signal.SIGINT, signal_handler)
#print('Press Ctrl+C')
#signal.pause()
class MicroControler(object) :

    def move_and_control(self, a):
        start_time = time.time()
         
        reference_position = a
        xo = a[0]
        yo = a[1]
        fo = a[2]
        xref = a[3]
        yref = a[4]
        fref = a[5]
        orientation = 0 
        while((fabs(xref-xo) >= xref*e) and (fabs(fref-fo) >= fref*e)): #yo) >= yref*e)  
            # set velocities to reach xref,yref,fref
            # prwta peristrofikh meta metaforikh
            if (fabs(fref-fo) > 0.1):
                w= (fref-fo)*L/(2*R*T)
                print ("gwnia problhma")
                print ("w PERISTROFI MONTELO rad/sec: "+str(w))
                #Ab.stop()
                #time.sleep(4)
                if w < 0:
                    orientation = 2
                    right_speed = wmax
                    left_speed = wmax
                else: 
                    orientation = 3
                    right_speed = -wmax
                    left_speed = -wmax
                 
                print ("apoklisi gwnias se rad: "+str(fref-fo))
                print ("w PERISTROFI rad/sec: "+str(w))
                #print str(w)
            
            
            
            
            else:
                w = (xref-xo)/(R*T)
                print ("w rad/sec: "+str(w))
                if w>wmax: w = wmax
                if 0<w<wmax : w=wmax
                if w<0:
                    w= -wmin
                    orientation = 1 
                elif w<wmin: 
                    w = wmin
                    orientation = 0
                else: 
                    orientation = 0
                right_speed = -w
                left_speed = w
                print ("w rad/sec: "+str(w))
            



            print ("apostasi apo stoxo se cm: "+str(fabs(xref-xo)) )
            #kinisi

            print (str(right_speed) , str(left_speed))
            Ab.setMotor(right_speed,left_speed)
        
            #fork processes and grab results after T 
            manager = multiprocessing.Manager()
            return_dict = manager.dict()
            jobs = []
            p = multiprocessing.Process(target=self.right_velocity,args=(0,  return_dict))
            jobs.append(p)
            p.daemon=True
            p.start()
            k = multiprocessing.Process(target=self.left_velocity,args = ( 1 , return_dict))
            jobs.append(k)
            k.daemon=True
            k.start()
            #p.terminate()
            #k.terminate()
            p.join(T)
            k.join(T)
            print ("velocities and time: right-left: "+ str(return_dict.values()))
            
            wr = return_dict[0]
            wl = return_dict[1]
            dt = (return_dict[2]+return_dict[3])/2
            #calculate new xo,yo,fo
            if orientation == 1 :
                wr= -wr
                wl= -wl
                print ("phgainw opisthen")
            if orientation ==0  or orientation==1:
                xo = xo + dt*cos(fo)*R*(wr+wl)/2 
                yo = yo + dt*sin(fo)*R*(wr+wl)/2 
            #if orientation == 3 : 
                #wr = -wr
                #wl=  -wl
            if orientation == 3 : 
                wr = -wr 
                wl = -wl
            
            print ("skata"+str(wr) , str(wl))
            fo = fo + dt * R*(wr-wl)/L
            
            
            #if fo > 2*pi : fo = fo - 2*pi
            print ("xo: "+str(xo), " yo: "+str(yo) ,  " fo: "+str(fo))
            Ab.stop()
            #time.sleep(10)

        
        end_time = time.time()
        x = end_time - start_time 
        print str(x)
        #time.sleep(1-x)
        
        Ab.stop()
        

    def right_velocity(self, procnum, return_dict):
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
                    #print (str(w) + " rad/s")
                    #u = R * w # cm
                    #u = u / 100
                    #print (str(w)+" 1 rad/s")
                    return_dict[procnum] = w #linear_velocity_right
                    return_dict[2] = dtime #linear_velocity_right
                    #prev_time = time.time()

                    #if (changes == 20) :
                    #    changes = 0
                        #now_time = time.time()
                        #print (str(now_time))
                        #dtime= now_time - prev_time

                        #prev_time = time.time()
                        #print (str(dtime))
                        #w = 2*pi  / dtime # s^2
                        #print (str(w) + " rad/s")
                        #u = R * w # cm
                        #u = u / 100
                        #print (str(u)+" m/s")
                        #return_dict[procnum] = w #linear_velocity_right
                        #prev_time = time.time()
                        #break ; 
            elif (DR_status == 1):
                if DR_status != prev_status:
                    prev_status = 1
        #linear_velocity_right = angular_velocity_right * R

    def left_velocity(self, procnum, return_dict):
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
                    #prev_time = time.time()
                    #if changes == 20 :
                    #    changes =0
                        #dtime=float(time.time())-float(prev_time)
                        #prev_time = time.time()
                        #print (str(dtime))
                        #w = 2*pi  / dtime # s^2
                        #return_dict[3] = dtime #linear_velocity_right
                        #print (str(w) + " rad/s")
                        #u = R * w # cm
                        #u = u / 100
                        #print (str(u)+" m/s")
                        #return_dict[procnum] = w #linear_velocity_left 
                        #break ; 
            elif (DR_status == 1):
                if DR_status != prev_status:
                    prev_status = 1
        #linear_velocity_left = angular_velocity_left * R




