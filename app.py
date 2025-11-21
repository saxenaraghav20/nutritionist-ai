import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image

# Load environment variables from .env file
load_dotenv()

# Configure the Google API key
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# --- MODEL AND PROMPT CONFIGURATION ---

# The model now takes the system prompt, user text, and the image
def get_gemini_response(system_prompt, user_prompt, image):
    # Use the Gemini 1.5 Flash model
    model = genai.GenerativeModel('gemini-1.5-pro')
    # The model now receives the system instructions, the image, AND the user's text
    response = model.generate_content([system_prompt, image, user_prompt])
    return response.text

# --- STREAMLIT APP INTERFACE ---

# Set the new page title
st.set_page_config(page_title="AI Nutritionist App") # <-- CHANGE

# Set the new header
st.header("AI Nutritionist App 📸") # <-- CHANGE
st.write("Upload a photo of your meal and provide any extra details for a nutritional analysis!")

# This is the prompt that defines the AI's main role
system_prompt = """
You are an expert nutritionist. A user will provide you with an image of a meal and optional text details.
Your task is to analyze the food items in the image, considering the user's text, and calculate the total calories.

Please identify each food item, estimate its quantity (e.g., in grams or cups), and list its
estimated calorie count. After listing all items, provide a final, total calorie estimate for
the entire meal. If the user provides text, use it to make your analysis more accurate.
"""

# File uploader for the image
uploaded_file = st.file_uploader("Choose an image of your meal...", type=["jpg", "jpeg", "png"])

image_input = ""
if uploaded_file is not None:
    image_input = Image.open(uploaded_file)
    st.image(image_input, caption="Uploaded Meal.", use_container_width=True)

# Add the text input bar for user details
user_prompt = st.text_input("Add details about your meal (e.g., 'the salad has caesar dressing'):") # <-- NEW

# Submit button
submit = st.button("Analyze My Meal")

# When the submit button is clicked
if submit:
    if image_input:
        with st.spinner("Analyzing..."):
            # The user's text is now passed to the model
            response = get_gemini_response(system_prompt, user_prompt, image_input)
            st.subheader("Nutritional Analysis:")
            st.markdown(response)
    else:
        st.warning("Please upload an image first.")
