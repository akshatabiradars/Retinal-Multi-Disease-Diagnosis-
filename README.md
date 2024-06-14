## Retinal-Multi-Disease-Diagnosis

# Description
Diabetic retinopathy is the leading cause of blindness in the working-age population of the developed world. It is estimated to affect over 93 million people.
World Health Organization estimates that 347 million people have the disease worldwide. Diabetic Retinopathy (DR) is an eye disease associated with long-standing diabetes.
Currently, detecting DR is a time-consuming and manual process that requires a trained clinician to examine and evaluate digital color fundus photographs of the retina. By the time human readers submit their reviews, often a day or two later, the delayed results lead to lost follow up, miscommunication, and delayed treatment.
Clinicians can identify DR by the presence of lesions associated with the vascular abnormalities caused by the disease. While this approach is effective, its resource demands are high. The expertise and equipment required are often lacking in areas where the rate of diabetes in local populations is high and DR detection is most needed. As the number of individuals with diabetes continues to grow, the infrastructure needed to prevent blindness due to DR will become even more insufficient.


# Retinal Multi Disease Diagnosis App 

 # Introduction
 
Welcome to the Retinal Multi Disease Diagnosis App. This web application aims to assist medical professionals and researchers in diagnosing multiple retinal diseases by capturing retinal images, processing them, and providing interactive tools for analysis.

# Key Features
Get Started with Streamlit:
An introduction to Streamlit, an open-source app framework designed for Machine Learning and Data Science projects.
Highlights of what Streamlit offers, such as simple API for building interactive apps, data display, media embedding, and easy deployment.

# Capture Retinal Images:
Use the built-in webcam functionality to capture high-quality images of the right or left eye.
Save the captured images with specific labels, including the name of the person and the date of capture.

# Dynamic Image Cropping:
Select and display any of the captured images.
Use interactive sliders to crop the selected image dynamically.
Save the cropped image for further analysis.

# Organize and Manage Images:
View a list of all captured images, making it easy to manage and organize the data.
Efficiently navigate through images using a simple and intuitive interface.

## Application Workflow

# User Interface:
The application starts with a welcoming title and an introduction to Streamlit and its features.
The sidebar contains options for entering the name of the person and selecting which eye to capture (right or left).
Capturing Images:
The main section has a camera input widget to capture retinal images.
Once an image is captured, it is saved with the name and timestamp in the captured_images directory.
Viewing and Cropping Images:
Users can view the list of captured images in the sidebar.
Selecting an image from the list displays it in the main section.
Four sliders allow users to crop the image dynamically by adjusting the left, upper, right, and lower coordinates.
The cropped image can be saved in the cropped_images directory.
