import cv2
import numpy as np
import pyvirtualcam

# Load the template (sprite)
template = cv2.imread('template.png', cv2.IMREAD_COLOR)
# Create a virtual camera
with pyvirtualcam.Camera(width=1280, height=720, fps=30) as cam:
    for _ in cam.frames():
        # Capture a frame from the virtual camera (OBS vcam output)
        frame = np.array(cam.frame, dtype=np.uint8)  # Convert the frame to numpy array
        

        # Perform template matching
        result = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)

        # Define a threshold to determine if a match is found
        threshold = 0.8

        # Find the locations where the template matches
        locations = np.where(result >= threshold)

        # Draw rectangles around detected sprite
        for pt in zip(*locations[::-1]):
            pt1 = (pt[0], pt[1])
            pt2 = (pt[0] + template.shape[1], pt[1] + template.shape[0])
            cv2.rectangle(frame, pt1, pt2, (0, 255, 0), 2)

        # Send the modified frame back to the virtual camera
        cam.send(frame)

        # Exit the loop if needed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
