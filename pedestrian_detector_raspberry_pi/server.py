import io 
from picamera2 import Picamera2, Preview
picam2 = Picamera2()
picam2.start_preview(Preview.QTGL)
picam2.start()


from flask import Flask, Response 
from time import sleep
from ultralytics import YOLO
model = YOLO("./model.pt")

import cv2



app = Flask(__name__)

def generate_frames(): 
    with Picamera2() as camera: 
        camera.resolution = (640, 480)
        camera.framerate = 24

        stream = io.BytesIO()
        for _ in camera.capture_continuous(stream, format='jpeg', use_video_port=True): 
            stream.seek(0)
            yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + stream.read() + b'\r\n'
            stream.seek(0)
            stream.truncate()

@app.route('/video_feed')
def video_feed(): 
   
    while True:
        frame = picam2.capture_array()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)
        result = model(frame)
        result[0].show()
    # return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)

