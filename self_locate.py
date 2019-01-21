import os
import subprocess
from AlphaBot import AlphaBot
import RPi.GPIO as GPIO
from io import BytesIO
from time import sleep
from picamera import PiCamera
from PIL import Image
from dna import *
import not_found_error

Ab = AlphaBot()
Dna = Dna()
Ab.stop()
S1 = 27 # or 22

camera = PiCamera()
camera.resolution = (2592, 1944)

beacons_found = 0
pulse_width = 2650
step = 300 # 300ms ~= 30Deg
distance = []
angle = []
color = []

# Distance and angle from at least 2 Beacons is needed for accurate localisation
while ((beacons_found < 2) and (pulse_width >= 900)):
    # Scan area with a 30-angle step
    pulse_width -= step
    with open(os.devnull, 'wb') as devnull:
        subprocess.check_call(['sudo', 'python', 'turn_head.py', '-s', '27', '-w', str(pulse_width)], stdout=devnull, stderr=subprocess.STDOUT)
    sleep(1)
    candidate = open('candidate'+str(pulse_width)+'.jpg', 'wb')
    camera.capture(candidate)
    candidate.close()
    try:
        d, a, c = Dna.find_distance_and_angle('candidate'+str(pulse_width)+'.jpg')
        # Check for already-found color
        if c not in color:
            distance.append(d)
            angle.append((pulse_width-1650)/11.11 - a)
            color.append(c)
            beacons_found += 1
            print("Beacons found: " + str(beacons_found))
        else:
            print("Beacon already found, not updating")
        print("-------------------------------\n")
    except NotFoundError:
        continue

print("-------------------------------")
print distance, angle, color
# Straigthen camera's position before exiting
with open(os.devnull, 'wb') as devnull:
        subprocess.check_call(['sudo', 'python', 'turn_head.py', '-s', '27', '-w', '1600'], stdout=devnull, stderr=subprocess.STDOUT)

