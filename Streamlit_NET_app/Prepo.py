# import the needed packages
import cv2
import pandas as pd
import numpy as np
import os
from datetime import datetime
import matplotlib.pyplot as plt
from PIL import Image
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import joblib
from PIL import Image
import io

def process_image(image):
    if image.mode != 'RGB':
        image = image.convert('RGB')
    image_np = np.array(image)
    return image_np


# Function to detect the nuclei
def detect_objects2(image_array, kernelsize, aspect, circ, min_size, max_size):
    if len(image_array.shape) != 2:
        raise ValueError("Expected grayscale image")
    blurred = cv2.GaussianBlur(image_array, (11, 11), 0)
    _, thresh = cv2.threshold(blurred, 50, 255, cv2.THRESH_BINARY)
    kernel = np.ones((kernelsize, kernelsize), np.uint8)
    closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    dilated = cv2.dilate(closing, kernel, iterations=2)
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    color_image = cv2.cvtColor(image_array, cv2.COLOR_GRAY2BGR)
    coordinates = []
    for contour in contours:
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = float(w) / h
            area = cv2.contourArea(contour)
            perimeter = cv2.arcLength(contour, True)
            if perimeter == 0:
                continue
            circularity = 4 * np.pi * (area / (perimeter * perimeter))
            if 1 - aspect <= aspect_ratio <= 1 + aspect and circularity > 1 - circ and min_size <= area <= max_size:
                coordinates.append((cX, cY))
                cv2.circle(color_image, (cX, cY), 5, (255, 0, 0), -1)
    return coordinates, color_image



# now we use these coordinates to do the subimaging on the merge-channel images

# Function to extract sub-images around detected nuclei
def extract_sub_images(image_array, coordinates):
    sub_images = []
    for i, (cX, cY) in enumerate(coordinates):
        startX = max(cX - 30, 0)
        startY = max(cY - 30, 0)
        endX = min(cX + 30, image_array.shape[1])
        endY = min(cY + 30, image_array.shape[0])
        sub_image = image_array[startY:endY, startX:endX]
        
        # Debugging information
        print(f"Sub-image {i} coordinates: startX={startX}, startY={startY}, endX={endX}, endY={endY}")
        print(f"Sub-image {i} shape: {sub_image.shape}")
        
        if sub_image.size == 0:
            continue  # Skip empty sub-images
        
        sub_images.append(sub_image)
        #st.image(sub_image, caption=f'Sub Image {i}', use_column_width=True)
    return sub_images




# Function to display the first three subimages of each image in subimages
def extract_sub_images(image_array, coordinates):
    sub_images = []
    for (cX, cY) in coordinates:
        startX = max(cX - 30, 0)
        startY = max(cY - 30, 0)
        endX = min(cX + 30, image_array.shape[1])
        endY = min(cY + 30, image_array.shape[0])
        sub_image = image_array[startY:endY, startX:endX]
        if sub_image.size == 0:
            continue  # Skip invalid sub-images
        sub_images.append(sub_image)
    return sub_images


