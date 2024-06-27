import streamlit as st
from datetime import datetime
import pandas as pd
from PIL import Image
import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array, load_img
import pickle
import os
import cv2
import matplotlib.pyplot as plt
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import joblib
import io
import plotly.graph_objects as go
import zipfile
import utils.data_processing as prep
import shutil
# Set the page configuration at the beginning
import streamlit as st

# Set the page configuration at the beginning
st.set_page_config(
    page_title="NET quantification App",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Example dropdown for page selection
page = st.sidebar.selectbox("Select a page", ["Home", "NETsubimages", "NET-neg-subimages"])

# Display logo
logo_url = "Logo_V1.png"
logo = Image.open(logo_url)
st.image(logo, width=200)

if page == "Home":

    st.markdown("""
    <style>
        /* Padding for the main content */
        .css-z5fcl4 {
            padding: 2rem 3rem 1rem 3rem;
        }

        /* Hide unnecessary elements */
        .css-otxysd {
            display: none;
        }

        .css-1oe5cao {
            max-height: 100vh;
        }

        .css-74h3l2 {
            display: block;
        }

        /* Set the main background and text colors */
        .stApp {
            background-color: #f0f8ff; /* Light background color */
            color: #00008b; /* Dark blue text color */
        }

        /* General text color */
        .st-emotion-cache-1r4qj8v {
            color: #8b0000; /* Dark red text color */
        }

        /* Header colors */
        h1, h2, h3, a, .st-emotion-cache-nahz7x a {
            color: #8b0000; /* Dark red text color */
        }

        /* Sidebar background and text colors */
        .st-emotion-cache-6qob1r {
            background-color: #f0f8ff; /* Light background color */
            color: #00008b; /* Dark blue text color */
        }

        /* Header background color */
        .stApp > header {
            background-color: #f0f8ff; /* Light background color */
        }

        /* Adjust other elements' background and text colors */
        .st-emotion-cache-1cypcdb {
            background-color: #f0f8ff; /* Light background color */
            color: #00008b; /* Dark blue text color */
        }

        .st-emotion-cache-1r4qj8v {
            background-color: #f0f8ff; /* Light background color */
        }

        /* Button text color */
        .stButton button {
            color: #00008b; /* Dark blue text color */
            background-color: #add8e6; /* Light blue background color */
        }

        .stButton button:hover {
            background-color: #87ceeb; /* Light sky blue background color on hover */
            color: #00008b; /* Dark blue text color */
        }

        /* Specific download button text color */
        .st-emotion-cache-n5w6h8 {
            color: #f0f8ff; /* Light text color */
        }

        /* Image caption text color */
        .st-emotion-cache-ltfnpr {
            color: #00008b; /* Dark blue text color */
        }

        /* File uploader text color */
        .st-emotion-cache-1tpl0xr p {
            color: #00008b; /* Dark blue text color */
        }

        /* File uploader's file name text color */
        .stFileUploaderFileName {
            color: #00008b; /* Dark blue text color */
        }

        /* SVG icon color */
        .st-emotion-cache-1pbsqtx {
            fill: #8b0000; /* Dark red fill color */
        }

        /* Text for "No sub-images available for prediction." */
        p {
            color: #8b0000; /* Dark red text color */
        }
    </style>
    """, unsafe_allow_html=True)

    st.header("Automated Net Quantification Inference")
    st.markdown(""" This app allows you to upload NETs images and
                performs recognition of NETs and non-NETs nuclei. 
                It also quantifies the NETs and non-NETs nuclei in the image.
                Furthermore, you can download the resulting quantification as a CSV file and
                the sub-images produced during the preprocessing stage.
            """)

    st.subheader('Load and Preprocess your image')
    
    # Initialize variables
    img_file_buffer = None
    image_pil = None
    image_array = None
    coordinates = None
    color_image = None

    # Layout
    col1, col2, col3 = st.columns(3)
    desired_width = 1024
    desired_height = 1024

   
    with col1:
        img_file_buffer = st.file_uploader('Upload a PNG or JPEG image', type=["jpg", "jpeg", "png", "tif"])
        if img_file_buffer is not None:
            img_bytes = img_file_buffer.read()
            image_pil = Image.open(io.BytesIO(img_bytes))
            resized_image = image_pil.resize((desired_width, desired_height))
            st.image(resized_image, caption='Uploaded Image', use_column_width=True)

    with col2:
        if st.button("About the feature tuning"):
            st.markdown("""***Header of the feature tuning***:For proper quantification of NETs it is important to detect all nuclei without picking up unwanted structures.
                    For this we use an object detection software.
                    Please tweak the features below to achieve the most optimal nucleus detection.""")
                    
            st.markdown("""***Kernel size***: The larger the kernel size the less objects will be separated. 
                    If you have segmented nuclei that are detected as different cells, 
                    increase the kernel size. 
                    If you have separate nuclei that are detected as one, decrease the kernel size.""")
                    
            st.markdown("""***Aspect Ratio***: The aspect ratio is the ratio of width and height of an imaginary
                    box that you can draw around the object.
                    The closer it is to 1 the less elongated the object is allowed to be to be detected as nucleus.""")
                    
            st.markdown("""***Circularity***: The closer the circularity is to 1 the more the object needs 
                    to be a perfect circle to be detected as nucleus.""")
                    
            st.markdown("""***Min/ Max Size***: Give the area thresholds of the detected objects. 
                    If you don’t want small objects to be detected as nucleus increase the min size. 
                    If you don’t want larger objects to be detected as nucleus decrease the max size.""")
            st.button("close")
        st.write("Adjust to optimize nucleus center detection")
        kernelsize = st.slider("kernel size", 1, 31, 5, step=2)
        aspects = st.slider("Aspect Ratio", 0.0, 1.0, 0.7)
        aspect = 1 - aspects
        circs = st.slider("Circularity", 0.0, 1.0, 0.4)
        circ = 1 - circs
        min_size = st.slider("Min Size", 1, 1000, 100)
        max_size = st.slider("Max Size", 1, 10000, 10000)

    if img_file_buffer is not None:
        with col3:
            image_array = np.array(image_pil)
            if len(image_array.shape) == 3:
                image_array = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
            
            coordinates, color_image = prep.detect_objects2(image_array, kernelsize, aspect, circ, min_size, max_size)
            st.image(color_image, caption='Detected Centers', use_column_width=True)
            sub_images = prep.extract_sub_images(image_array, coordinates)
            st.session_state.sub_images = sub_images
            if st.button("display some subimages"):
                if sub_images:
                    for i, sub_image in enumerate(sub_images[:3]):
                        st.image(sub_image, caption=f'Sub Image {i+1}', use_column_width=True)
                else:
                    st.write("No valid sub-images found.")
                st.button("close") 

            button_pressed = st.button("Download All Subimages")
            
            if button_pressed:
                if sub_images:
                    with zipfile.ZipFile(os.path.expanduser('~/Downloads/sub_images.zip'), 'w') as zipf:  # Create a zip file
                        for i, sub_image in enumerate(sub_images):
                            sub_image_pil = Image.fromarray(sub_image)
                            sub_image_pil.save(f'sub_image_{i+1}.png', 'PNG')  # Save image locally
                            zipf.write(f'sub_image_{i+1}.png', f'sub_image_{i+1}.png')  # Add image to zip file
                            os.remove(f'sub_image_{i+1}.png')  # Remove saved image file after adding to zip

                    st.write("All sub-images downloaded successfully.")
                
                else:
                    st.warning("No valid sub-images found.")
    else:
        st.write("Upload an image to get started.")

#########################################################################################################

# Prediction Phase
    st.subheader('Predict Number of Nets and non-Nets')

    # Load the trained logistic regression model, StandardScaler, and PCA
    MODEL_SAVE_PATH_pma_ctr = 'models/CTR_and_PMA_model/logistic_regression_model_v2.pkl'
    SCALER_SAVE_PATH_pma_ctr = 'models/CTR_and_PMA_model/scaler_v2.pkl'
    PCA_SAVE_PATH_pma_ctr = 'models/CTR_and_PMA_model/pca_v2.pkl'

    MODEL_SAVE_PATH_ctr = 'models/CTR_model/logistic_regression_model_DOP_v2.pkl'
    SCALER_SAVE_PATH_ctr = 'models/CTR_model/scaler_v2.pkl'
    PCA_SAVE_PATH_ctr = 'models/CTR_model/pca_v2.pkl'

    MODEL_SAVE_PATH_pma = 'models/PMA_model/logistic_regression_model_PMA.pkl'
    SCALER_SAVE_PATH_pma = 'models/PMA_model/scaler_PMA.pkl'
    PCA_SAVE_PATH_pma = 'models/PMA_model/pca_PMA.pkl'

    model_choices = ["CTR and PMA trained model", "PMA trained model", "CTR trained model"]
    selected_model = st.selectbox('Select a model:', model_choices)
    if selected_model == "CTR and PMA trained model":
        MODEL_SAVE_PATH = MODEL_SAVE_PATH_pma_ctr
        SCALER_SAVE_PATH = SCALER_SAVE_PATH_pma_ctr
        PCA_SAVE_PATH = PCA_SAVE_PATH_pma_ctr
    elif selected_model == "PMA trained model":
        MODEL_SAVE_PATH = MODEL_SAVE_PATH_pma
        SCALER_SAVE_PATH = SCALER_SAVE_PATH_pma
        PCA_SAVE_PATH = PCA_SAVE_PATH_pma
    else:
        MODEL_SAVE_PATH = MODEL_SAVE_PATH_ctr
        SCALER_SAVE_PATH = SCALER_SAVE_PATH_ctr
        PCA_SAVE_PATH = PCA_SAVE_PATH_ctr

    model = joblib.load(MODEL_SAVE_PATH)
    scaler = joblib.load(SCALER_SAVE_PATH)
    pca = joblib.load(PCA_SAVE_PATH)

    IMG_SIZE = (224, 224)
    BATCH_SIZE = 32

    # Define your prediction function
    def predict_image(image, model, scaler, pca, img_size=(224, 224)):
        img = Image.fromarray(image)
        img = img.resize(img_size)
        img_array = img_to_array(img)
        img_array = img_array.reshape((1, -1))  # Flatten the image
        img_array = img_array / 255.0  # Rescale the image

        # Apply StandardScaler and PCA
        img_array_scaled = scaler.transform(img_array)
        img_array_pca = pca.transform(img_array_scaled)

        # Make a prediction
        prediction_prob = model.predict_proba(img_array_pca)
        predicted_class = np.argmax(prediction_prob, axis=1)[0]

        return predicted_class, prediction_prob

    # Function to save image with prediction number or probability in the filename
    def save_image_with_prediction_info(image_array, subimage_number, predicted_class, prediction_prob, output_dir):
        image = Image.fromarray(np.uint8(image_array))  # Convert the NumPy array to a PIL Image
        image = image.convert("RGB")  # Ensure the image is in RGB color
        image = image.resize((250, 250))  # Resize the image to 250x250

        # Create a new folder for each class
        class_folder = os.path.join(output_dir, f"class_{predicted_class}")
        if not os.path.exists(class_folder):
            os.makedirs(class_folder)
        # Create a new filename with subimage number, prediction class and probability
        image_name = f"subimage_{subimage_number}_prob_{np.max(prediction_prob):.2f}.png"
        image_path = os.path.join(class_folder, image_name)
        image.save(image_path)
        return image_path

    # Streamlit layout
    predcol1, predcol2, predcol3 = st.columns(3)
    
    with predcol1:
        if 'sub_images' in st.session_state: 
            # Predict on sub-images
            results = []
            saved_images = {0: [], 1: []}  # Assuming you have two classes: 0 and 1
            for i, sub_image in enumerate(st.session_state['sub_images']):
                predicted_class, prediction_prob = predict_image(sub_image, model, scaler, pca)
                results.append({
                    'Subimage Number': i,
                    'Predicted Category': predicted_class,
                    'Probabilities': prediction_prob.tolist()  # Convert array to list for display
                })
                # Save image with prediction info in filename
                image_path = save_image_with_prediction_info(sub_image.copy(), i, predicted_class, prediction_prob, 'predicted_images')
                saved_images[predicted_class].append(image_path)

            results_df = pd.DataFrame(results)
            st.session_state.results_df = results_df
            st.session_state.saved_images = saved_images  # Store saved_images in session_state
            st.write("Prediction completed")

            if st.button("View detailed table"):
                st.dataframe(results_df)

            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
            output_csv_path = f'results/{timestamp}_predictions_subimages.csv'
            if not os.path.exists('results'):
                os.makedirs('results')
            results_df.to_csv(output_csv_path, index=False)

            st.download_button(
                label="Download Results as CSV",
                data=results_df.to_csv(index=False),
                file_name=f'{timestamp}_predictions_subimages.csv',
                mime='text/csv'
            )
    with predcol2:
        if st.button("View summary"):
            if 'results_df' in st.session_state: 
                image_summary = results_df[['Predicted Category', 'Subimage Number']].groupby(['Predicted Category']).count().reset_index()
                image_summary.rename(columns={'Subimage Number': 'Cell Count'}, inplace=True)
                image_summary['Predicted Category'] = image_summary['Predicted Category'].replace({0: 'NET negative', 1: 'NET positive'})
                st.session_state.image_summary = image_summary
                st.dataframe(image_summary)

    with predcol3:
        # Create a Plotly bar plot
            if 'image_summary' in st.session_state:
                    image_summary = st.session_state.image_summary  # Retrieve from session state
                    # Create a Plotly bar plot
                    fig = go.Figure(data=[go.Bar(x=image_summary['Predicted Category'], y=image_summary['Cell Count'])])
                    fig.update_layout(
                    title='Summary Plot',
                    xaxis_title='Predicted Category',
                    yaxis_title='Cell Count'
                    )
                
                    st.plotly_chart(fig)
 
elif page == "NETsubimages":
    st.title("NETsubimages")
    if 'saved_images' in st.session_state and len(st.session_state.saved_images[1]) > 0:
        images = st.session_state.saved_images[1]
        num_images = len(images)
        cols_per_row = 6

        for i in range(0, num_images, cols_per_row):
            cols = st.columns(cols_per_row)
            for j, image_path in enumerate(images[i:i + cols_per_row]):
                with cols[j]:
                    st.image(image_path)
    else:
        st.write("No NET-neg-subimages available for display.")

elif page == "NET-neg-subimages":
    st.title("NET-neg-subimages")
    if 'saved_images' in st.session_state and len(st.session_state.saved_images[0]) > 0:
        images = st.session_state.saved_images[0]
        num_images = len(images)
        cols_per_row = 6

        for i in range(0, num_images, cols_per_row):
            cols = st.columns(cols_per_row)
            for j, image_path in enumerate(images[i:i + cols_per_row]):
                with cols[j]:
                    st.image(image_path)
    else:
        st.write("No NET-neg-subimages available for display.")

            

     