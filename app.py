import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image

# Load environment variables
load_dotenv()

# Configure the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# --- HELPER FUNCTION TO PROCESS IMAGE ---
def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
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

# --- GEMINI API CALL ---
def get_gemini_response(input_prompt, image_data, user_prompt):
    # UPDATED: Using the model from your available list
    model = genai.GenerativeModel('models/gemini-2.5-flash')
    
    # The model expects a list containing the prompt and the image data dictionary
    response = model.generate_content([input_prompt, image_data[0], user_prompt])
    return response.text

# --- STREAMLIT APP CONFIG ---
st.set_page_config(page_title="AI Nutritionist App")

st.header("AI Nutritionist App 📸")
st.write("Upload a photo of your meal for a nutritional analysis!")

# System Prompt
system_prompt = """
You are an expert nutritionist. A user will provide you with an image of a meal and optional text details.
Your task is to analyze the food items in the image, considering the user's text, and calculate the total calories.

Please identify each food item, estimate its quantity (e.g., in grams or cups), and list its
estimated calorie count. After listing all items, provide a final, total calorie estimate for
the entire meal. If the user provides text, use it to make your analysis more accurate.
"""

# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image_Data = ""

if uploaded_file is not None:
    # Display the image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Meal.", use_container_width=True)

# User input for extra details
user_input = st.text_input("Add details (e.g., 'I used olive oil'):")

submit = st.button("Analyze My Meal")

# Logic when button is clicked
if submit:
    if uploaded_file is not None:
        try:
            # 1. Process the image into the format Gemini likes
            image_data = input_image_setup(uploaded_file)
            
            # 2. Call Gemini
            with st.spinner("Analyzing..."):
                response = get_gemini_response(system_prompt, image_data, user_input)
                
                # 3. Show Result
                st.subheader("Nutritional Analysis:")
                st.write(response)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please upload an image first.")
