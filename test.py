import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from time import sleep # Import the sleep function from the time module

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(12, GPIO.IN);

while True:
	input = GPIO.input(12)
	if(input):
		GPIO.output(8, GPIO.HIGH)
	else:
		GPIO.output(8, GPIO.LOW)
