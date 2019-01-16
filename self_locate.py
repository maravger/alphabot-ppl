import os
import subprocess
from AlphaBot import AlphaBot
import RPi.GPIO as GPIO
from io import BytesIO
from time import sleep
from picamera import PiCamera
from PIL import Image
from dna import *
import math
import argparse

Ab = AlphaBot()
Dna = Dna()
Ab.stop()
S1 = 27 # or 22

camera = PiCamera()
camera.resolution = (2592, 1944)

################################################################# 
################# For prototype testing only ####################
#################################################################
#ap = argparse.ArgumentParser()
#ap.add_argument("-d", "--distance", help = "distance from target")
#args = vars(ap.parse_args())

#dist = float(args["distance"])

# 1 degree = 11.11ms pulse width, 0 degrees = 2650ms, 180 degrees = 650 
#if (dist >= 250):
#    degrees = 90
#else:
#    degrees = 90 - math.atan(75 / (250 - dist))
#left_width = str(int(2700 - (degrees*11.11)) / 10 * 10)
#right_width = str(int(650 + (degrees*11.11)) / 10 * 10)
#################################################################

# Turn head LEFT
with open(os.devnull, 'wb') as devnull:
    subprocess.check_call(['sudo', 'python', 'turn_head.py', '-s', '27', '-w', '2650'], stdout=devnull, stderr=subprocess.STDOUT)
sleep(1)
left = open('left.jpg', 'wb')
camera.capture(left)
left.close()
    
Dna.find_distance_and_angle('left.jpg')
print("\n")
# Turn head RIGHT
with open(os.devnull, 'wb') as devnull:
    subprocess.check_call(['sudo', 'python', 'turn_head.py', '-s', '27', '-w', '650'], stdout=devnull, stderr=subprocess.STDOUT)
sleep(1)
right = open('right.jpg', 'wb')
camera.capture(right)
right.close()
Dna.find_distance_and_angle('right.jpg')
print("-------------------------------")
