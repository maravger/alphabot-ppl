from RPIO import PWM
import argparse
from time import sleep

# This function is separate from the rest of the functionality as it needs sudo 
# rights to run.
servo = PWM.Servo()

ap = argparse.ArgumentParser()
ap.add_argument("-w", "--width", help = "pulse width in microseconds")
ap.add_argument("-s", "--servo", help = "number of servo-pin")
args = vars(ap.parse_args())

servo.set_servo(int(args["servo"]),int( args["width"]))
sleep(1)
