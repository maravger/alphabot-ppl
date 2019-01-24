import RPi.GPIO as GPIO
import time
import sys
import signal
from math import pi, fabs, cos, sin
from alphabot import AlphaBot
import multiprocessing

R = 0.034 # wheel radius (m) 6,6 cm 
T = 0.5
r = 0.0165  #wood wheel radious
L = 0.132   # distance between  wheels 
Ab = AlphaBot()
Ab.stop()
vmax = 80
vmin= 45

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
        T = 0.5 
        reference_position = a
        xo = a[0]
        yo = a[1]
        fo = a[2]
        xref = a[3]
        yref = a[4]
        fref = a[5]
        orientation = 0 
        rotational = 0 
        e = 0.1
        
        
        if fref!=fo:
            print ("rotational move")
            #if 0.5236 -e <= fref-fo <= 0.5236 + e : 
            #    Ab.setMotor(-40,-40)
            #    time.sleep(0.25)
            #    Ab.stop()
            rotational = 1
            e= 0.15
            T = 0.6

        
        counter = 2
        moves = 0 
        while((fabs(xref-xo) > fabs(xref)*e) or (fabs(fref-fo) > 0.1)) : #yo) >= yref*e)  
            dt = T 
            c = 0 
            moves += 1
            # set velocities to reach xref,yref,fref
            # prwta peristrofikh meta metaforikh
            if (fabs(fref-fo) >= e):
                if rotational == 1 and moves > 1:
                    dt = dt/ 5 
                elif rotational ==0:
                    dt = dt / 5 
                print ("dt : " + str(dt))
                # fix errors of not measuring wr,wl
                if c > 0:
                    dt = dt /8
                    c = 0
                print ("error sth gwnia " + str(fabs(fref-fo)))
                w= (fref-fo)*L/(2*R*dt) # xronos misos diplasio w
                #print ("gwnia problhma")
                print ("w PERISTROFI MONTELO rad/sec: "+str(w))
                #Ab.stop()
                #time.sleep(4)
                right_voltage = (w - B)/A
                left_voltage =  (w - D)/C
                print ("right_voltage: "+str(right_voltage)+ " left_voltage: "+str(left_voltage))
                
                if (-vmin < right_voltage < 0) : right_voltage = - vmin# + 10 
                if (right_voltage < - vmax) : right_voltage = - vmax
                if (0 <= right_voltage <  vmin) : right_voltage = vmin 
                if (right_voltage > vmax) : right_voltage = vmax
                if (-vmin < left_voltage < 0) : left_voltage = - vmin
                if (left_voltage < - vmax) : left_voltage = - vmax
                if (0 <= left_voltage <  vmin) : left_voltage = vmin
                if (left_voltage > vmax) : left_voltage = vmax
                
                #left_voltage = vmin  
                #right_voltage = vmin  
                if w < 0:  #prepei na stripsw pros ta deksia ( + , + ) 
                    orientation = 2
                    right_voltage= -right_voltage
                    left_voltage= -left_voltage


                else: # prepei na stripsw pros ta aristera ( - , - )
                    orientation = 3
                    right_voltage= -right_voltage
                    left_voltage= -left_voltage


                #print ("apoklisi gwnias se rad: "+str(fref-fo))
                print ("w PERISTROFI rad/sec: "+str(w)+ " orientation: "+str(orientation))
                print ("right_voltage: "+str(right_voltage)+ " left_voltage: "+str(left_voltage))
                #print str(w)
            
            
            
            
            elif (fabs(xref-xo)>=fabs(xref*0.1) and (rotational!= 1)):
                print ("metaforiki kinhsh")
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
                
                
                if w >= 0:
                    orientation = 0
                    right_voltage = -right_voltage # an w > 0 tote prepei na paw eutheia ara ( - , + )
                    left_voltage = +left_voltage
                if w<0:         # an w < 0 tote prepei na paw opisthen ara ( + , - )            
                    right_voltage = -right_voltage 
                    left_voltage =  left_voltage
                    orientation = 1 
              
               # print ("w rad/sec: "+str(w))
            else : 
                Ab.stop()
                #print ("STOPPPPPPPPPPPPPPPPPPPP")
                break ;  
            print ("right voltage :" + str(right_voltage) , "left_voltage "+ str(left_voltage))


            #print ("apostasi apo stoxo se cm: "+str(fabs(xref-xo)) )

            #p1rint (str(right_voltage) , str(left_voltage))
            Ab.setMotor(right_voltage, left_voltage) # PRWTA RIGHT META LEFT !!! EINAI ANAPODA STHN SETMOTOR
        
            #fork processes and grab results after dt
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
            time.sleep(dt)
            p.terminate()
            k.terminate()
            p.join(T)       
            k.join(T)
            
            # try to grab measurements
            counter = 2
            try:
                wr = return_dict[0]
                dtr = return_dict[2]

                #right_voltage = (wr - B)/A
                
                #if (-vmin < right_voltage < 0) : right_voltage = -vmin
                #if (right_voltage < - vmax) : right_voltage = -vmax
                #if (0 <= right_voltage <  vmin) : right_voltage = vmin
                #if (right_voltage > vmax) : right_voltage = vmax
                #wr = right_voltage* A + B 

            except: 
                print ("error1")
                #wr = pi /(10 * T)  
                wr = 0 
                dtr =0
                counter = counter -1 
            try:
                wl = return_dict[1]
                dtl = return_dict[3]
                #left_voltage =  (wl - D)/C

                #if (-vmin < left_voltage < 0) : left_voltage = -vmin
                #if (left_voltage < - vmax) : left_voltage = -vmax
                #if (0 <= left_voltage <  vmin) : left_voltage = vmin
                #if (left_voltage > vmax) : left_voltage = vmax
                #wl = left_voltage*C + D

            except: 
                print ("error2")
                #wl = pi / (10 * T) * 2 
                wl = 0 
                counter = counter -1 
                dtl = 0
            if counter == 2 :
                print ("dt: "+str(dt))
                dt = (dtl+dtr)/counter
                print ("dt: "+str(dt))
            else :
                dt = dt 
                c +=1

        
        #calculate new xo,yo,fo
            
            if orientation == 3: # tou eipa na stripsei aristera epitopou 
                wr = wr    # eixa paei prin deksia sta - kai twra thelw na paw aristera sta +
                wl = -wl   # ara wr - wl prepei na einai thetiko 
                

            if orientation == 2: # tou eipa na stripsei deksia epitopou
                wr = -wr   # eixa paei prin aristera sta + kai twra thelw na paw deksia sta -  
                wl =  wl   # ara wr-wl  prepei na einai arnhtiko 

            
            fo = fo + dt * R*(wr-wl)/L
            print ("measured  wr , wl , dt , f0 : "+str(wr) , str(wl), str(dt), str(fo))
            
            if fo > 2*pi : fo = fo - 2*pi    # estw oti exw kanei kuklo mhdenise
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




