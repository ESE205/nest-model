import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from time import sleep # Import the sleep function from the time module

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW)

while True:
	GPIO.output(8, GPIO.HIGH)
	sleep(1)
	GPIO.output(8, GPIO.LOW)
	sleep(1)
