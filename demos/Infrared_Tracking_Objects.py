import RPi.GPIO as GPIO
import time
from AlphaBot import AlphaBot
import smbus

Ab = AlphaBot()

DR = 16
DL = 19


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(DR,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(DL,GPIO.IN,GPIO.PUD_UP)

Ab.stop()
try:
	while True:

		DR_status = GPIO.input(DR)
		DL_status = GPIO.input(DL)
		if((DL_status == 0) and (DR_status == 0)):
			Ab.forward()
			print("forward")
		elif((DL_status == 1) and (DR_status == 0)):
			Ab.right()
			print("right")
		elif((DL_status == 0) and (DR_status == 1)):
			Ab.left()
			print("left")
		else:
			Ab.stop()
			print("stop")

except KeyboardInterrupt:
	GPIO.cleanup();

