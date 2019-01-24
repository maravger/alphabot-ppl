import RPi.GPIO as GPIO
import time
from AlphaBot import AlphaBot

SERVO = 27
TRIG = 17
ECHO = 5

Ab = AlphaBot()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(SERVO, GPIO.OUT, initial=GPIO.LOW) 
GPIO.setup(TRIG,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(ECHO,GPIO.IN)
p = GPIO.PWM(SERVO,50)
p.start(0)

def ServoAngle(angle):
	p.ChangeDutyCycle(2.5 + 10.0 * angle / 180)

def Distance():
	GPIO.output(TRIG,GPIO.HIGH)
	time.sleep(0.000015)
	GPIO.output(TRIG,GPIO.LOW)
	while not GPIO.input(ECHO):
		pass
	t1 = time.time()
	while GPIO.input(ECHO):
		pass
	t2 = time.time()
	return (t2-t1)*34000/2

ServoAngle(90)		
print("Ultrasonic_Obstacle_Avoidance")
try:
	while True:
		middleDistance = Distance()
		print("MiddleDistance = %0.2f cm"%middleDistance)
		if middleDistance <= 20:
			Ab.stop()
#			time.sleep(0.5)
			ServoAngle(5)
			time.sleep(1)
			rightDistance = Distance()
			print("RightDistance = %0.2f cm"%rightDistance)
#			time.sleep(0.5)
			ServoAngle(180)
			time.sleep(1)
			leftDistance = Distance()
			print("LeftDistance = %0.2f cm"%leftDistance)
#			time.sleep(0.5)	
			ServoAngle(90)
			time.sleep(1)
			if rightDistance <20 and leftDistance < 20:
				Ab.backward()
				time.sleep(0.3)
				Ab.stop()
			elif rightDistance >= leftDistance:
				Ab.right()
				time.sleep(0.3)
				Ab.stop()
			else:
				Ab.left()
				time.sleep(0.3)
				Ab.stop()
			time.sleep(0.3)
		else:
			Ab.forward()
			time.sleep(0.02)

except KeyboardInterrupt:
	GPIO.cleanup();
