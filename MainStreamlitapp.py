import streamlit as st
import cv2
import numpy as np
import requests
from datetime import datetime
from streamlit_webrtc import webrtc_streamer,VideoTransformerBase
from camera_input_live import camera_input_live
import av
import os 
from PIL import Image
from io import BytesIO

# Function to capture image from webcam
def capture_image(side, name):
    stframe = st.empty()
    video_capture = cv2.VideoCapture(0)
    
    if not video_capture.isOpened():
        stframe.text("Could not open webcam.")
        return None
    
    stframe.text(f"Capturing {side} Eye. Press 's' to save and 'q' to quit.")
    
    while True:
        ret, frame = video_capture.read()
        if not ret:
            stframe.text("Failed to capture image.")
            break
        
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        stframe.image(frame_rgb)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            img_name = f"{side}_Eye_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{name}.jpg"
            img_path = os.path.join('captured_images', img_name)
            cv2.imwrite(img_path, frame)
            stframe.text(f"Saved {img_name}")
            break
        elif key == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
    return img_path

# Function to crop image
def crop_image(image, coords):
    return image.crop(coords)

# Function to load captured images
def load_images(path='captured_images'):
    if not os.path.exists(path):
        os.makedirs(path)
    files = os.listdir(path)
    return [f for f in files if f.endswith('.jpg')]

# Main function
def main():
    st.title("Retinal Multi Disease Diagnosis Platform")

    st.sidebar.header("Options")
    person_name = st.sidebar.text_input("Enter Name:")
    capture_side = st.sidebar.radio("Capture Side", ('Right Eye', 'Left Eye'))
    
    if st.sidebar.button("Capture Image"):
        if not person_name:
            st.sidebar.warning("Please enter a name before capturing.")
        else:
            img_path = capture_image(capture_side, person_name)
            if img_path:
                st.sidebar.success(f"Image saved: {img_path}")
            else:
                st.sidebar.error("Image capture failed.")

    st.sidebar.subheader("Captured Images")
    captured_files = load_images()
    
    if captured_files:
        selected_file = st.sidebar.selectbox("Select Image", captured_files)
        if selected_file:
            image = Image.open(os.path.join('captured_images', selected_file))
            st.image(image, caption=selected_file)

            crop_coords = st.slider("Select Crop Area (left, upper, right, lower)", 0, min(image.size), (0, 0, image.size[0], image.size[1]), step=1)
            if st.button("Crop and Save"):
                cropped_image = crop_image(image, crop_coords)
                cropped_path = os.path.join('cropped_images', selected_file.replace('.jpg', '_cropped.jpg'))
                cropped_image.save(cropped_path)
                st.success(f"Cropped image saved: {cropped_path}")

if __name__ == "__main__":
    if not os.path.exists('captured_images'):
        os.makedirs('captured_images')
    if not os.path.exists('cropped_images'):
        os.makedirs('cropped_images')
    main()



