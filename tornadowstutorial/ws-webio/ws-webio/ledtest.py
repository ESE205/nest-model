#!/usr/bin/python
import RPi.GPIO as GPIO
import time
#Set GPIO pins as outputs
GPIO.setmode(GPIO.BOARD)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
#Switch GPIO pins ON
GPIO.output(16, True)
GPIO.output(18, True)
#Wait 5 seconds
time.sleep(5)
#Switch GPIO pins OFF
GPIO.output(16, False)
GPIO.output(18, False)
#Reset GPIO pins to their default state
GPIO.cleanup()
