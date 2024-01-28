# Remove the dotenv import and the load_dotenv() line as you're not using an .env file
# from dotenv import load_dotenv
# load_dotenv()  # take environment variables from .env.

import streamlit as st
from PIL import Image
import google.generativeai as genai

# Define the Authorization header using the API key from Streamlit secrets
headers = {
    "Authorization": st.secrets["api_key"]
}

# Configure the Google API key directly from Streamlit secrets
genai.configure(api_key=st.secrets["google_api_key"])

# Function to load OpenAI model and get responses
def get_gemini_response(input, image, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, image[0], prompt])
    return response.text

# Function to set up image for processing
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Initialize the Streamlit app
st.set_page_config(page_title="Gemini Image Demo")

# UI elements
st.header("Multi Language Invoice Extractor")
input_text = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = ""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit_button = st.button("Tell me about the image")

input_prompt = """
               You are an expert in understanding invoices.
               You will receive input images as invoices &
               you will have to answer questions based on the input image
               """

# Handle button click
if submit_button:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input_text)
    st.subheader("The Response is")
    st.write(response)
