import io 
from picamera2 import Picamera2, Preview
picam2 = Picamera2()
picam2.start_preview(Preview.QTGL)
picam2.start()

from ultralytics import YOLO
model = YOLO("./model.pt")

import cv2

import RPi.GPIO as GPIO

# Use GPIO pin 18
led_pin = 4

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT)

# Blink forever
try:   
    while True:
        frame = picam2.capture_array()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)
        result = model(frame)
        result[0].show()
        for box in result[0].boxes:
            x1, y1, x2, y2 = map(int, result[0].boxes.xyxy[0])
            confidence = float(box.conf[0])
            print("confidence", confidence)
            if confidence > 0.2:
                GPIO.output(led_pin, GPIO.HIGH)  # LED on
            elif confidence <= 0.2:
                GPIO.output(led_pin, GPIO.LOW)   # LED off
        if len(result[0].boxes) < 1:
            GPIO.output(led_pin, GPIO.LOW)

except KeyboardInterrupt:
    # Clean up when you press ctrl+c
    GPIO.cleanup()