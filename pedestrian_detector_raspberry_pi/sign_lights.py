# from picamzero import Camera
# from time import sleep

# cam = Camera()
# cam.start_preview()

# sleep(15)

import RPi.GPIO as GPIO
import time

# Use GPIO pin 18
led_pin = 14

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)


# Blink forever
try:
    while True:
        GPIO.output(led_pin, GPIO.HIGH)  # LED on
        GPIO.output(15, GPIO.HIGH)
        GPIO.output(18, GPIO.HIGH)
        time.sleep(2)                    # Wait 1 second
        GPIO.output(led_pin, GPIO.LOW)   # LED off
        GPIO.output(15, GPIO.LOW)
        GPIO.output(18, GPIO.LOW)

        time.sleep(2)                    # Wait 1 second
        
except KeyboardInterrupt:
    # Clean up when you press ctrl+c
    GPIO.cleanup()
