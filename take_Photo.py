#Sample code for taking photo with camera

import cv2
import os
from datetime import datetime

def capture_and_save_photo(folder_path, filename=None):
    # Check if the folder exists, if not, create it
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Initialize the webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    # Capture a frame
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        return

    # Release the webcam
    cap.release()
    
    # Generate a filename with a timestamp if none is provided
    if filename is None:
        filename = datetime.now().strftime("taken_photo") + ".jpg"

    # Save the photo
    file_path = os.path.join(folder_path, filename)
    cv2.imwrite(file_path, frame)
    print(f"Photo saved at {file_path}")

# Usage example
folder_path = "photos"
capture_and_save_photo(folder_path)
