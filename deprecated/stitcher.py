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

with open(os.devnull, 'wb') as devnull:
    subprocess.check_call(['sudo', 'python', 'turn_head.py', '-s', '27', '-w', '2300'], stdout=devnull, stderr=subprocess.STDOUT)
sleep(1)
pic = open('0.jpg', 'wb')
camera.capture(pic)
pic.close()

with open(os.devnull, 'wb') as devnull:
    subprocess.check_call(['sudo', 'python', 'turn_head.py', '-s', '27', '-w', '1950'], stdout=devnull, stderr=subprocess.STDOUT)
sleep(1)
pic = open('1.jpg', 'wb')
camera.capture(pic)
pic.close()

with open(os.devnull, 'wb') as devnull:
    subprocess.check_call(['sudo', 'python', 'turn_head.py', '-s', '27', '-w', '1600'], stdout=devnull, stderr=subprocess.STDOUT)
sleep(1)
pic = open('2.jpg', 'wb')
camera.capture(pic)
pic.close()

with open(os.devnull, 'wb') as devnull:
    subprocess.check_call(['sudo', 'python', 'turn_head.py', '-s', '27', '-w', '1300'], stdout=devnull, stderr=subprocess.STDOUT)
sleep(1)
pic = open('3.jpg', 'wb')
camera.capture(pic)
pic.close()


with open(os.devnull, 'wb') as devnull:
    subprocess.check_call(['sudo', 'python', 'turn_head.py', '-s', '27', '-w', '950'], stdout=devnull, stderr=subprocess.STDOUT)
sleep(1)
pic = open('4.jpg', 'wb')
camera.capture(pic)
pic.close()

with open(os.devnull, 'wb') as devnull:
    subprocess.check_call(['sudo', 'python', 'turn_head.py', '-s', '27', '-w', '650'], stdout=devnull, stderr=subprocess.STDOUT)
sleep(1)
pic = open('5.jpg', 'wb')
camera.capture(pic)
pic.close()
