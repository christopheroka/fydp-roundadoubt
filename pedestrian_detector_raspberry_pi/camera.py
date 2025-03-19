import io 
from picamera2 import Picamera2, Preview
picam2 = Picamera2()
picam2.start_preview(Preview.QTGL)
picam2.start()

from ultralytics import YOLO
model = YOLO("./model.pt")

import cv2
import RPi.GPIO as GPIO

# Set pins
SIGN_LEFT_PIN = 2
SIGN_STRAIGHT_PIN = 3
SIGN_RIGHT_PIN = 4
FLOOR_LIGHT_PIN = 14

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(FLOOR_LIGHT_PIN, GPIO.OUT)
GPIO.setup(SIGN_STRAIGHT_PIN, GPIO.OUT)
GPIO.setup(SIGN_LEFT_PIN, GPIO.OUT)
GPIO.setup(SIGN_RIGHT_PIN, GPIO.OUT)

SHOW_PREVIEW = False
CAMERA_OUTPUT_DIM = (640,480)

floorLightIsOn = False
straightLightIsOn = False
leftLightIsOn = False
rightLightIsOn = False

PERSISTENCE_FRAMES = 5
leftCounter = 0
straightCounter = 0
rightCounter = 0

def turnFloorLightOn():
  global floorLightIsOn
  print("Floor light turning on")
  GPIO.output(FLOOR_LIGHT_PIN, GPIO.HIGH)
  floorLightIsOn = True

def turnFloorLightOff():
  global floorLightIsOn
  GPIO.output(FLOOR_LIGHT_PIN, GPIO.LOW)
  print("Floor light turned off")
  floorLightIsOn = False

def turnSignOn(pin):
  global straightLightIsOn
  global leftLightIsOn
  global rightLightIsOn
  if pin == SIGN_STRAIGHT_PIN: 
    turnFloorLightOn()
  GPIO.output(pin, GPIO.HIGH)
  sign_type = ""
  if pin == SIGN_STRAIGHT_PIN:
    straightLightIsOn = True
    sign_type="straight"
  elif pin == SIGN_LEFT_PIN:
    leftLightIsOn = True
    sign_type="left"
  elif pin == SIGN_RIGHT_PIN:
    rightLightIsOn = True
    sign_type = "right"
  print(f'Sign {sign_type} turned on')

def turnSignOff(pin):
  global straightLightIsOn
  global leftLightIsOn
  global rightLightIsOn
  if pin == SIGN_STRAIGHT_PIN:
    turnFloorLightOff()
  GPIO.output(pin, GPIO.LOW)
  sign_type = ""
  if pin == SIGN_STRAIGHT_PIN:
    straightLightIsOn = False
    sign_type="straight"
  elif pin == SIGN_LEFT_PIN:
    leftLightIsOn = False
    sign_type="left"
  elif pin == SIGN_RIGHT_PIN:
    rightLightIsOn = False
    sign_type = "right"
  print(f'Sign {sign_type} turned off')

# Blink forever
try:   
  while True:
      frame = picam2.capture_array()
      frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)
      result = model(frame)

      if SHOW_PREVIEW:
          result[0].show()
      if len(result[0].boxes) < 1:
          leftCounter = max(0, leftCounter - 1)
          straightCounter = max(0, straightCounter - 1)
          rightCounter = max(0, rightCounter - 1)
      else:
          for i, box in enumerate(result[0].boxes):
              x1, y1, x2, y2 = map(int, result[0].boxes.xyxy[i])
              confidence = float(box.conf[0])
              # print("confidence", confidence)
              # print(f"({x1}, {y1}), ({x2}, {y2})")

              box_middle = x1 + (x2 - x1) / 2
              print(f"BOX_COORDS: {x1},{x2}, BOX_MIDDLE_COORDS: {box_middle}, CONFIDENCE: {confidence}")

              # Keep the light on if ped. was last seen within a small amount of frames (make it less finicky)
              if box_middle < CAMERA_OUTPUT_DIM[0] / 3:
                  leftCounter = PERSISTENCE_FRAMES
                  if not leftLightIsOn:
                      turnSignOn(SIGN_LEFT_PIN)
              elif box_middle < 2 * CAMERA_OUTPUT_DIM[0] / 3:
                  straightCounter = PERSISTENCE_FRAMES
                  if not straightLightIsOn:
                      turnSignOn(SIGN_STRAIGHT_PIN)
              else:
                  rightCounter = PERSISTENCE_FRAMES
                  if not rightLightIsOn:
                      turnSignOn(SIGN_RIGHT_PIN)

      # Turn off lights only when persistance counters reach zero
      if leftCounter == 0 and leftLightIsOn:
          turnSignOff(SIGN_LEFT_PIN)
      if straightCounter == 0 and straightLightIsOn:
          turnSignOff(SIGN_STRAIGHT_PIN)
      if rightCounter == 0 and rightLightIsOn:
          turnSignOff(SIGN_RIGHT_PIN)

      # Reduce persistance counters each frame if no ped. seen
      leftCounter = max(0, leftCounter - 1)
      straightCounter = max(0, straightCounter - 1)
      rightCounter = max(0, rightCounter - 1)

except KeyboardInterrupt:
    # Clean up when you press ctrl+c
    GPIO.cleanup()

