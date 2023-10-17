import cv2
from ultralytics import YOLO
import os
from datetime import datetime

# Define the OBS virtual camera as the video source
virtual_camera_name = 'OBS Virtual Camera'  # Change this to the name of your OBS virtual camera
cap = cv2.VideoCapture(1)

# Check if the capture object is opened successfully
if not cap.isOpened():
    print("Error: Could not open OBS virtual camera.")
    exit()

# Define the output video parameters
video_path_out = "C:/Git Projects/OpenCV/Yolo/Realtime_out.mp4"
fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Create the VideoWriter object to save the processed frames
# out = cv2.VideoWriter(video_path_out, cv2.VideoWriter_fourcc(*'H264'), fps, (width, height))

# Your YOLO model and threshold setup goes here
os.environ['YOLO_CONSOLE_OUTPUT'] = 'false'
model_path = os.path.join('.', 'runs', 'detect', 'train9', 'weights', 'last.pt')
model = YOLO(model_path)
threshold = 0.5

history = []

i = 0
while i < 100:
    ret, frame = cap.read()
    objects = []
    if not ret: break

    # Perform object detection on the frame using your YOLO model
    results = model.track(frame,verbose=False)[0]
    
    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, id, confidence, class_id = None
        if len(result) == 6:
            x1, y1, x2, y2, confidence, class_id = result
        elif len(result) == 7:
            x1, y1, x2, y2, id, confidence, class_id = result

        if confidence > threshold:
            objects.append({
                "x": x1,
                "y": y1,
                "id": id,
                "width": abs(x2 - x1),
                "height": abs(y2 - y1),
                "class": class_id,
            })
            print(objects)

    frame = {
        "data": objects,
        "time": datetime.now()
    }
    history.append(frame)
    i += 1

for frame in history:
    print(frame)
    
cap.release()
cv2.destroyAllWindows()
