from picamera2 import Picamera2
import time

camera = Picamera2()

camera.resolution = (640,480)
camera.framerate = 24

camera.start_preview()

from picamera2 import PiCamera
from time import sleep 

camera = PiCamera()
sleep(2)
camera.capture('test_image.jpg')
print("Image captured")