# from picamzero import Camera
# from time import sleep

# cam = Camera()
# cam.start_preview()

# sleep(15)

import RPi.GPIO as GPIO
import time

# Use GPIO pin 18
led_pin = 4

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT)

# Blink forever
try:
    while True:
        GPIO.output(led_pin, GPIO.HIGH)  # LED on
        time.sleep(5)                    # Wait 1 second
        GPIO.output(led_pin, GPIO.LOW)   # LED off
        time.sleep(5)                    # Wait 1 second
        
except KeyboardInterrupt:
    # Clean up when you press ctrl+c
    GPIO.cleanup()
