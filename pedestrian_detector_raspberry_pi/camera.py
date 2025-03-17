import io 
from picamera2 import Picamera2, Preview
picam2 = Picamera2()
picam2.start_preview(Preview.QTGL)
picam2.start()

from ultralytics import YOLO
model = YOLO("./model.pt")

import cv2
import RPi.GPIO as GPIO
from time import sleep

# Set pins
FLOOR_LIGHT_PIN = 2
SIGN_STRAIGHT_PIN = 3
SIGN_LEFT_PIN = 14
SIGN_RIGHT_PIN = 15

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(FLOOR_LIGHT_PIN, GPIO.OUT)
GPIO.setup(SIGN_STRAIGHT_PIN, GPIO.OUT)
GPIO.setup(SIGN_LEFT_PIN, GPIO.OUT)
GPIO.setup(SIGN_RIGHT_PIN, GPIO.OUT)


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
            print(f"({x1},{y1}),({x2},{y2})")

except KeyboardInterrupt:
    # Clean up when you press ctrl+c
    GPIO.cleanup()


def turnFloorLightOn():
  print("Light turning on")
  GPIO.output(FLOOR_LIGHT_PIN, GPIO.HIGH)
  sleep(1)
  GPIO.output(FLOOR_LIGHT_PIN, GPIO.LOW)
  print("Light turned on")
  floorLightIsOn = True

def turnFloorLightOff():
  print("Light turning off");
  GPIO.output(FLOOR_LIGHT_PIN, GPIO.HIGH);
  sleep(2.5);
  GPIO.output(FLOOR_LIGHT_PIN, GPIO.LOW);
  print("Light turned off");
  floorLightIsOn = False;

def turnSignOn(pin):
  if pin == SIGN_STRAIGHT_PIN: 
    turnFloorLightOn();
  GPIO.output(pin, GPIO.HIGH);
  sign_type = ""
  if pin == SIGN_STRAIGHT_PIN:
    straightLightIsOn = True;
    sign_type="straight"
  elif pin == SIGN_LEFT_PIN:
    sign_type="left"
  elif pin == SIGN_RIGHT_PIN:
    sign_type = "right"
  print(f'Sign {sign_type} turned on')

def turnSignOff(pin):
  if pin == SIGN_STRAIGHT_PIN:
    turnFloorLightOff()
  GPIO.output(pin, GPIO.LOW)
  sign_type = ""
  if pin == SIGN_STRAIGHT_PIN:
    straightLightIsOff = True;
    sign_type="straight"
  elif pin == SIGN_LEFT_PIN:
    sign_type="left"
  elif pin == SIGN_RIGHT_PIN:
    sign_type = "right"
  print(f'Sign {sign_type} turned off')
