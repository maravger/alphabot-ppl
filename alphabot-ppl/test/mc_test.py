from micro_controller import *
import time 

M = MicroControler()
# call with a[x0,y0,f0, xref, yref, fref ], x,y in cm and f in rad 

#a=[0,0,0,0,0,0.523598]

# - sth gwnia shmainei stripse deksia
# + sth gwnia shmainei stripse aristera

a=[0,0,0,0.5,0,0]
#a=[0,0,0,0,0,0.4]

#a=[0,0,0,0,0,-1.65]


M.move_and_control(a)
time.sleep(2)

'''
a=[0,0,0,0.25,0,0]
M.move_and_control(a)
time.sleep(2)




a=[0,0,0,0.25,0,0]
M.move_and_control(a)
print ("PROTI KINISI TELOS 25 CM ")
time.sleep(2)


a=[0.25,0,0,0.5,0,0]
M.move_and_control(a)
print ("deuteri KINISI TELOS 25 CM ")
time.sleep(2)

a=[0.5,0,0,0.5,0,-1.65]
M.move_and_control(a)
print ("TRITI KINISI TELOS 90 moires  ")
time.sleep(2)

a=[0,0,0,-0.25,0,0]
M.move_and_control(a)
print ("TETARTI KINISI TELOS 25 CM ")
time.sleep(2)


a=[0,0,0,0,0,-1.65]
M.move_and_control(a)
print ("PEMPTI KINISI TELOS 90 MOIRES ")
'''


'''
0.5235987756 rad 30 
0.7853981634 rad 45
1.0471975512 rad 60
1.5707963268 rad 90
2.0943951024 rad 120
2.3561944902 rad 135
2.6179938780 rad 150
3.1415926536 rad 180
4.7123889804 rad 270
6.2831853072 rad 360
'''

