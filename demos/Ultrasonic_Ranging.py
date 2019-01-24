import RPi.GPIO as GPIO
import time

TRIG = 17
ECHO = 5

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(TRIG,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(ECHO,GPIO.IN)

def dist():
	GPIO.output(TRIG,GPIO.HIGH)
	time.sleep(0.000015)
	GPIO.output(TRIG,GPIO.LOW)
	print("1")
	while not GPIO.input(ECHO):
		pass
	t1 = time.time()
	print("T1: " + str(t1))
	print("2")
	while GPIO.input(ECHO):
		pass
	print("3")
	t2 = time.time()
	return (t2-t1)*34000/2

try:
	while True:
		print("HELLO")
		print("here")
		print("Distance:%0.2f cm" % dist())
		time.sleep(1)
except KeyboardInterrupt:
	GPIO.cleanup()
