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
def capture_image(side):
    stframe = st.empty()
    video_capture = cv2.VideoCapture(0)
    
    stframe.text("Capturing {} Eye. Press 's' to save and 'q' to quit.".format(side))
    
    while True:
        ret, frame = video_capture.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        stframe.image(frame)
        
        if cv2.waitKey(1) & 0xFF == ord('s'):
            img_name = "{}_Eye_{}.jpg".format(side, datetime.now().strftime("%Y%m%d_%H%M%S"))
            img_path = os.path.join('captured_images', img_name)
            cv2.imwrite(img_path, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            stframe.text("Saved {}".format(img_name))
            break
        elif cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
    return img_path

# Function to crop image
def crop_image(image, coords):
    return image.crop(coords)

# Function to load captured images
def load_images(path='captured_images'):
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
            img_path = capture_image(capture_side)
            st.sidebar.success(f"Image saved: {img_path}")

    st.sidebar.subheader("Captured Images")
    captured_files = load_images()
    
    if captured_files:
        selected_file = st.sidebar.selectbox("Select Image", captured_files)
        if selected_file:
            image = Image.open(os.path.join('captured_images', selected_file))
            st.image(image, caption=selected_file)

            crop_coords = st.slider("Select Crop Area", 0, 100, (25, 75), step=5)
            if st.button("Crop and Save"):
                cropped_image = crop_image(image, (crop_coords[0], crop_coords[0], crop_coords[1], crop_coords[1]))
                cropped_path = os.path.join('cropped_images', selected_file.replace('.jpg', '_cropped.jpg'))
                cropped_image.save(cropped_path)
                st.success(f"Cropped image saved: {cropped_path}")

if __name__ == "__main__":
    if not os.path.exists('captured_images'):
        os.makedirs('captured_images')
    if not os.path.exists('cropped_images'):
        os.makedirs('cropped_images')
    main()


