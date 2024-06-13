import streamlit as st
import cv2
import numpy as np
import requests
from datetime import datetime
from streamlit_webrtc import webrtc_streamer,VideoTransformerBase
from camera_input_live import camera_input_live
import av
import os

class VideoTransformer(VideoTransformerBase):
    def __init__(self):
        self.threshold1 = 100
        self.threshold2 = 200

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        image = cv2.cvtColor(cv2.Canny(img, 100, 200), cv2.COLOR_GRAY2BGR)
        return av.VideoFrame.from_ndarray(image, format="bgr24")
    def toggle_webcam(index):
        global capture
        try:
            if st.session_state.is_webcam_enabled:
                FRAME_WINDOW = st.image([])
                camera_index = 1  # Replace with the index you found
                capture = cv2.VideoCapture(camera_index)
                _, frame = capture.read()
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                FRAME_WINDOW.image(frame)
            else:
                if capture is not None:
                capture.release()
        except Exception as e:
        st.error(f"Error accessing webcam: {e}")
def Web_RTC_Video(frame):
    image = frame.to_ndarray(format="bgr24")
    image = cv2.cvtColor(cv2.Canny(image, 100, 200), cv2.COLOR_GRAY2BGR)
    return av.VideoFrame.from_ndarray(image, format="bgr24")

# Directory to save captured images
CAPTURE_DIR = "captured_images"
if not os.path.exists(CAPTURE_DIR):
    os.makedirs(CAPTURE_DIR)

st.title("Retinal Multi Disease Diagnosis - App")

def get_camera_index():
    for index in range(10):  # Check first 10 camera indices
        cap = cv2.VideoCapture(index)
        if cap.isOpened():
            cap.release()
            return index
    return None

def capture_image(side, name):
    camera_index = get_camera_index()
    if camera_index is None:
        st.error("No camera found")
        return None

    cap = cv2.VideoCapture(camera_index)
    ret, frame = cap.read()
    if ret:
        cap.release()
        filename = f"{CAPTURE_DIR}/{side}_Eye_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{name}.jpg"
        cv2.imwrite(filename, frame)
        return filename
    else:
        cap.release()
        st.error("Failed to capture image from webcam")
        return None

# UI to capture images
st.header("Capture Eye Images")
name = st.text_input("Enter Name")
right_eye_capture = st.button("Capture Right Eye")
left_eye_capture = st.button("Capture Left Eye")

if right_eye_capture:
    filename = capture_image("Right", name)
    if filename:
        st.success(f"Right eye image captured and saved as {filename}")

if left_eye_capture:
    filename = capture_image("Left", name)
    if filename:
        st.success(f"Left eye image captured and saved as {filename}")

# UI to display and crop captured images
st.header("Captured Images")
captured_files = [f for f in os.listdir(CAPTURE_DIR) if os.path.isfile(os.path.join(CAPTURE_DIR, f))]

if captured_files:
    selected_file = st.selectbox("Select a captured file", captured_files)
    if selected_file:
        file_path = os.path.join(CAPTURE_DIR, selected_file)
        image = cv2.imread(file_path)
        st.image(image, caption=selected_file, use_column_width=True)

        # Cropping UI
        st.subheader("Crop Image")
        x = st.slider("x", 0, image.shape[1], 0)
        y = st.slider("y", 0, image.shape[0], 0)
        width = st.slider("Width", 0, image.shape[1] - x, image.shape[1] - x)
        height = st.slider("Height", 0, image.shape[0] - y, image.shape[0] - y)
        
        if st.button("Crop Image"):
            cropped_image = image[y:y+height, x:x+width]
            cropped_filename = f"{CAPTURE_DIR}/cropped_{selected_file}"
            cv2.imwrite(cropped_filename, cropped_image)
            st.success(f"Image cropped and saved as {cropped_filename}")
            st.image(cropped_image, caption=cropped_filename, use_column_width=True)
else:
    st.info("No captured images found")
