import os
import subprocess
from AlphaBot import AlphaBot
import RPi.GPIO as GPIO
from io import BytesIO
from time import sleep
from picamera import PiCamera
from PIL import Image
from dna import *

Ab = AlphaBot()
Dna = Dna()
Ab.stop()
S1=27 # or 22

camera = PiCamera()
camera.resolution = (2592, 1944)
while(1):
    # Turn head LEFT
    with open(os.devnull, 'wb') as devnull:
            subprocess.check_call(['sudo', 'python', 'turn_head.py', '-s', '27', '-w', '2700'], stdout=devnull, stderr=subprocess.STDOUT)
    sleep(1)
    left = open('left.jpg', 'wb')
    camera.capture(left)
    left.close()
    
    Dna.find_distance_and_angle('left.jpg')
    print("\n")
    # Turn head RIGHT
    with open(os.devnull, 'wb') as devnull:
            subprocess.check_call(['sudo', 'python', 'turn_head.py', '-s', '27', '-w', '700'], stdout=devnull, stderr=subprocess.STDOUT)
    sleep(1)
    right = open('right.jpg', 'wb')
    camera.capture(right)
    right.close()
    Dna.find_distance_and_angle('right.jpg')
    print("-------------------------------")
