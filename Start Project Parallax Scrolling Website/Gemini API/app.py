# Import necessary libraries
from dotenv import load_dotenv
import os
import google.generativeai as genai
from PIL import Image
import streamlit as st

# Load the API key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to interact with Google Gemini Vision Model and get response
def get_response_image(image, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([image[0], prompt])  # Corrected typo: genrate_content -> generate_content
    return response.text, response.image_url

# Function to interact with Google Gemini Pro Model and get response
def get_response(prompt, input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt, input])  # Corrected typo: genrate_content -> generate_content
    return response.text

# Function to prepare image data
def prep_image(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.read()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded!")

# Set Streamlit page configuration
st.set_page_config(
    page_title="Planner: Discover and Plan your Culinary Adventures!",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown(
    """
    <style>
        .main {
            background-color: #f0f8ea; /* Light green background */
            padding: 20px;
            border-radius: 10px;
        }
        .header {
            font-size: 36px;
            color: #4CAF50; /* Green text */
            text-align: center;
            margin-bottom: 20px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Main content
st.markdown('<p class="header">Planner: Discover and Plan your Culinary Adventures!</p>', unsafe_allow_html=True)

# Sidebar options
section_choice = st.radio("Choose Section:", ("Location Finder", "Trip Planner", "Weather Forecasting", "Restaurant & Hotel Planner"))

# Section: Location Finder
if section_choice == "Location Finder":
    upload_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])
    if upload_file is not None:
        image = Image.open(upload_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

    input_prompt_loc = """
    You are an expert Tourist Guide. Your job is to provide a summary about the place and:
    - Location of the place
    - State & Capital
    - Coordinates of the place
    - Some popular places nearby
    
    Return the response using markdown.
    """

    submit = st.button("Get Location!")
    if submit:
        image_data = prep_image(upload_file)
        response = get_response_image(image_data, input_prompt_loc)
        st.subheader("Tour Bot:")
        st.markdown(response[0])
        st.image(response[1], caption="Location Image", use_column_width=True)

# Section: Trip Planner
if section_choice == "Trip Planner":
    input_prompt_planner = """
    You are an expert Tour Planner. Your job is to provide recommendations and a plan for a given location for any number of days.
    Also suggest hidden secrets, hotels, and beautiful places we shouldn't forget to visit.
    Also, tell the best month to visit the given place.
    
    Return the response using markdown.
    """

    input_plan = st.text_area("Provide location and number of days to obtain itinerary plan!")
    submit1 = st.button("Plan my Trip!")
    if submit1:
        response = get_response(input_prompt_planner, input_plan)
        st.subheader("Planner Bot:")
        st.markdown(response)

# Section: Weather Forecasting
if section_choice == "Weather Forecasting":
    input_prompt_weather = """
    You are an expert weather forecaster. Your job is to provide a forecast for a given place for the next 7 days from the current date.
    - Provide Precipitation
    - Provide Humidity
    - Provide Wind
    - Provide Air Quality
    - Provide Cloud Cover
    
    Return the response using markdown.
    """

    input_weather = st.text_area("Provide location to forecast weather!")
    submit2 = st.button("Forecast Weather!")
    if submit2:
        response = get_response(input_prompt_weather, input_weather)
        st.subheader("Weather Bot:")
        st.markdown(response)

# Section: Restaurant & Hotel Planner
if section_choice == "Restaurant & Hotel Planner":
    input_prompt_accommodation = """
    You are an expert Restaurant & Hotel Planner.
    Your job is to provide Restaurant & Hotel options for a given place that are neither too expensive nor too cheap.
    - Provide rating of the restaurant/hotel
    - Top 5 restaurants with address and average cost per cuisine
    - Top 5 hotels with address and average cost per night
    
    Return the response using markdown.
    """

    input_accommodation = st.text_area("Provide location to find Hotels & Restaurants!")
    submit3 = st.button("Find Restaurant & Hotel!")
    if submit3:
        response = get_response(input_prompt_accommodation, input_accommodation)
        st.subheader("Accommodation Bot:")
        st.markdown(response)
