import RPi.GPIO as GPIO
import time
from AlphaBot import AlphaBot

Ab = AlphaBot()

IR = 18
PWM = 50
n=0

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(IR,GPIO.IN,GPIO.PUD_UP)


def getkey():
	if GPIO.input(IR) == 0:
		count = 0
		while GPIO.input(IR) == 0 and count < 200:  #9ms
			count += 1
			time.sleep(0.00006)

		count = 0
		while GPIO.input(IR) == 1 and count < 80:  #4.5ms
			count += 1
			time.sleep(0.00006)

		idx = 0
		cnt = 0
		data = [0,0,0,0]
		for i in range(0,32):
			count = 0
			while GPIO.input(IR) == 0 and count < 15:    #0.56ms
				count += 1
				time.sleep(0.00006)
				
			count = 0
			while GPIO.input(IR) == 1 and count < 40:   #0: 0.56mx
				count += 1                               #1: 1.69ms
				time.sleep(0.00006)
				
			if count > 8:
				data[idx] |= 1<<cnt
			if cnt == 7:
				cnt = 0
				idx += 1
			else:
				cnt += 1
		print data
		if data[0]+data[1] == 0xFF and data[2]+data[3] == 0xFF:  #check
			return data[2]

		if data[0] == 255 and data[1] == 255 and data[2] == 15 and data[3] == 255:
			return "repeat"

			
print('IRremote Test Start ...')
Ab.stop()
try:
	while True:
		key = getkey()
		if(key != None):
			if key == "repeat":
				n = 0				 
			if key == 0x18:
				Ab.forward()
#				print("forward")
			if key == 0x08:
				Ab.left()
#				print("left")
			if key == 0x1c:
				Ab.stop()
#				print("stop")
			if key == 0x5a:
				Ab.right()
#				print("right")
			if key == 0x52:
				Ab.backward()		
#				print("backward")
			if key == 0x15:
				if(PWM + 10 < 101):
					PWM = PWM + 10
					Ab.setPWMA(PWM)
					Ab.setPWMB(PWM)
					print(PWM)
			if key == 0x07:
				if(PWM - 10 > -1):
					PWM = PWM - 10
					Ab.setPWMA(PWM)
					Ab.setPWMB(PWM)
					print(PWM)
		else:
			n += 1
			if n > 20000:
				n = 0
				Ab.stop()	
except KeyboardInterrupt:
	GPIO.cleanup();

