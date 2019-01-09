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
GPIO.setup(S1, GPIO.OUT)
PS1 = GPIO.PWM(S1,50)
PS1.start(50)

def set_servo(angle):
    PS1.ChangeDutyCycle(12.5 - 10.0 * float(angle) / 180)

camera = PiCamera()
camera.resolution = (2592, 1944)
while(1):
    # Turn head LEFT
    set_servo(-5)
    sleep(1)
    left = open('left.jpg', 'wb')
    camera.capture(left)
    left.close()
    Dna.dna('left.jpg')
    # Turn head RIGHT
    set_servo(171)
    sleep(1)
    right = open('right.jpg', 'wb')
    camera.capture(right)
    right.close()
    Dna.dna('right.jpg')

