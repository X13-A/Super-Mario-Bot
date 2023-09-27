from ultralytics import YOLO

print("loading model...")
model = YOLO("yolov8n.yaml")
print("training model...")
results = model.train(data="./config.yaml", epochs=1)
print("training finished !")
