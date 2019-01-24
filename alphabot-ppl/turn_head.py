from RPIO import PWM
import argparse
from time import sleep

servo = PWM.Servo()

ap = argparse.ArgumentParser()
ap.add_argument("-w", "--width", help = "pulse width in microseconds")
ap.add_argument("-s", "--servo", help = "number of servo-pin")
args = vars(ap.parse_args())

servo.set_servo(int(args["servo"]),int( args["width"]))
sleep(1)
#servo.stop_servo(int(args["servo"]))
