import RPi.GPIO as GPIO
import time
import sys
import signal
from math import pi, fabs, cos, sin
from AlphaBot import AlphaBot
import multiprocessing

R = 0.034 # wheel radius (m) 6,6 cm 
T = 0.3
r = 0.0165  #wood wheel radious
L = 0.132   # distance between  wheels 
Ab = AlphaBot()
e = 0.1
vmax = 100
vmin= 30

#for wr the equation for voltage is v = (wr - B)/ A
A = 0.16136027
B = 1.2869597
#for wl the equation for voltage is v = (wr - D)/ C
C = 0.16225248
D = -0.3943191


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
        dt = T
        while((fabs(xref-xo) >= fabs(xref)*e) or (fabs(fref-fo) >= 0.1)): #yo) >= yref*e)  
            # set velocities to reach xref,yref,fref
            # prwta peristrofikh meta metaforikh
            if (fabs(fref-fo) >= 0.1):
                w= (fref-fo)*L/(2*R*T)
                #print ("gwnia problhma")
                #print ("w PERISTROFI MONTELO rad/sec: "+str(w))
                #Ab.stop()
                #time.sleep(4)
                right_voltage = (w - B)/A
                left_voltage =  (w - D)/C
                
                if (-vmin < right_voltage < 0) : right_voltage = vmin
                if (right_voltage < - vmax) : right_voltage = vmax
                if (0 <= right_voltage <  vmin) : right_voltage = vmin
                if (right_voltage > vmax) : right_voltage = vmax
                if (-vmin < left_voltage < 0) : left_voltage = vmin
                if (left_voltage < - vmax) : left_voltage = vmax
                if (0 <= left_voltage <  vmin) : left_voltage = vmin
                if (left_voltage > vmax) : left_voltage = vmax
                
                if w < 0:  #prepei na stripsw pros ta deksia
                    orientation = 2
                    right_voltage= right_voltage
                    left_voltage= left_voltage


                else: # prepei na stripsw pros ta aristera
                    orientation = 3
                    right_voltage= -right_voltage
                    left_voltage=-left_voltage


                #print ("apoklisi gwnias se rad: "+str(fref-fo))
                print ("w PERISTROFI rad/sec: "+str(w)+ " orientation: "+str(orientation))
                #print str(w)
            
            
            
            
            elif (fabs(xref-xo)>=fabs(xref*e)):
                w = (xref-xo)/(R*dt)
                #print ("w rad/sec: "+str(w))
                right_voltage = (w - B)/A
                left_voltage =  (w - D)/C
                
                if (-vmin < right_voltage < 0) : right_voltage = -vmin
                if (right_voltage < - vmax) : right_voltage = -vmax
                if (0 <= right_voltage <  vmin) : right_voltage = vmin
                if (right_voltage > vmax) : right_voltage = vmax
                if (-vmin < left_voltage < 0) : left_voltage = -vmin
                if (left_voltage < - vmax) : left_voltage = -vmax
                if (0 <= left_voltage <  vmin) : left_voltage = vmin
                if (left_voltage > vmax) : left_voltage = vmax
                
                
               
                right_voltage = right_voltage 
                left_voltage = -left_voltage
                if w<0:
                    right_voltage = right_voltage 
                    left_voltage = left_voltage
                    orientation = 1 
                else: 
                    orientation = 0
                
              
               # print ("w rad/sec: "+str(w))
            else : 
                Ab.stop()
                #print ("STOPPPPPPPPPPPPPPPPPPPP")
                break ;  
            #print ("right voltage :" + str(right_voltage) , "left_voltage "+ str(left_voltage))


            #print ("apostasi apo stoxo se cm: "+str(fabs(xref-xo)) )
            #kinisi

            #p1rint (str(right_voltage) , str(left_voltage))
            Ab.setMotor(left_voltage,right_voltage)
        
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

            time.sleep(T)
            p.terminate()
            k.terminate()
            p.join(T)       
            k.join(T)
            #print ("velocities and time: right-left: "+ str(return_dict.values()))
            counter = 2
            try:
                wr = return_dict[0]
                dtr = return_dict[2]
            except: 
                print ("error1")
                #wr = pi /(10 * T)  
                wr = 0 
                dtr =0
                counter = counter -1 
            try:
                wl = return_dict[1]
                dtl = return_dict[3]
            except: 
                print ("error2")
                wl = pi / (10 * T) * 2 
                #wl = 0 
                counter = counter -1 
                dtl = 0
            if counter != 0 :
                dt = (dtl+dtr)/counter
            else : dt = T 

        
        #calculate new xo,yo,fo
            
            if orientation == 3: 
                wr = +wr 
                wl = -wl

            if orientation == 2:
                wr = -wr
                wl = wl 
            
            print ("measured  wr , wl , dt ,  previous f0 : "+str(wr) , str(wl), str(dt), str(fo))
            fo = fo + dt * R*(wr-wl)/L
            
            
            if fo > 2*pi : fo = fo - 2*pi
            if fo < -2*pi : fo = fo + 2*pi
            
            
            if orientation == 1 :
                wr= -wr
                wl= -wl
                print ("phgainw opisthen")
            
            
            if orientation ==0  or orientation==1:
                xo = xo + dt*cos(fo)*R*(wr+wl)/2 
                yo = yo + dt*sin(fo)*R*(wr+wl)/2 
        
            if fo > 2*pi : fo = fo - 2*pi
            if fo < -2*pi : fo = fo + 2*pi
            print ("xo: "+str(xo), " yo: "+str(yo) ,  " fo: "+str(fo))
            Ab.stop()
            time.sleep(0.5)

        
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




