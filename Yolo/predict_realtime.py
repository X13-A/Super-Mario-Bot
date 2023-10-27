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
video_path_out = "C:/Git Projects/Machine-Learning-E4/Yolo/Realtime_out.avi"
fps = 30
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


# Create the VideoWriter object to save the processed frames
out = cv2.VideoWriter(video_path_out, cv2.VideoWriter_fourcc(*'MJPG'), fps, (width, height))

# Your YOLO model and threshold setup goes here
os.environ['YOLO_CONSOLE_OUTPUT'] = 'false'
model_path = os.path.join('.', 'runs', 'detect', 'train10', 'weights', 'last.pt')
model = YOLO(model_path)
threshold = 0.1

history = []

try:
    i = 0
    while i < 400:
        
        ret, frame = cap.read()
        cv2.imshow('Frame', frame)
        cv2.waitKey(1)
        objects = []
        if not ret: break

        # Perform object detection on the frame using your YOLO model
        results = model.track(frame,verbose=False)[0]
        print(i)
        for result in results.boxes.data.tolist():
            x1, y1, x2, y2, id, confidence, class_id = None, None, None, None, None, None, None
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
                # print(objects)

                # Draw the rectangle around the detected object
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                
                # Draw the label (using class_id here, modify as needed)
                label = str(class_id)
                cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Write the processed frame to the output video
        out.write(frame)

        frame_data  = {
            "data": objects,
            "time": datetime.now()
        }
        history.append(frame_data)
        i += 1

    # for frame_data in history:
    #     print(frame_data)
        
    cap.release()
    out.release()
    cv2.destroyAllWindows()
except Exception as e:
    print(f"Exception occurred: {e}")
