# from roboflow import Roboflow

# rf = Roboflow(api_key="pnouPmmUju2DOnKsxQjs")

# project = rf.workspace("roundadoubt").project("yolov9human-2u7yv")

# model = project.version(1, local="http://localhost:9001/").model

# prediction = model.predict("/home/roundadoubt/Downloads/test-image.jpg")

# print(prediction.json())

# prediction.save("output.png")

from ultralytics import YOLO

model = YOLO("./model.pt")
results = model("/home/roundadoubt/Downloads/test-image.jpg")
print(results)
results[0].show()
results[0].save()