import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image
from google.generativeai.types import GenerationConfig

# Load environment variables
load_dotenv()

# Configure the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# --- HELPER FUNCTION TO PROCESS IMAGE ---
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

# --- GEMINI API CALL (Generic) ---
def get_gemini_response(input_prompt, image_data, user_prompt):
    # Using the 2.5 Flash model which worked for your key
    model = genai.GenerativeModel('models/gemini-2.5-flash')
    
    # Configuration for consistent results (Temperature = 0 for facts)
    config = GenerationConfig(
        temperature=0.1,        # Low temperature = Less hallucination
        top_p=1,
        top_k=32,
        max_output_tokens=4096,
    )
    
    response = model.generate_content(
        [input_prompt, image_data[0], user_prompt], 
        generation_config=config 
    )
    return response.text

# --- STREAMLIT APP CONFIG ---
st.set_page_config(page_title="AI Nutritionist App")

st.header("AI Nutritionist App 📸")
st.write("Upload a photo of your meal to track calories or get recipe ideas!")

# --- PROMPTS ---

# Prompt 1: Calorie Analysis
nutrition_prompt = """
You are an expert nutritionist. A user will provide you with an image of a meal.
Your task is to analyze the food items in the image and calculate the total calories.

Please identify each food item, estimate its quantity, and list its
estimated calorie count. Finally, provide a total calorie estimate.
"""

# Prompt 2: Recipe Recommendations
recipe_prompt = """
You are a talented chef and nutritionist. 
Look at the ingredients visible in the provided image. 
Suggest 3 HEALTHY and delicious recipes that can be made using these primary ingredients.

For each recipe, provide:
1. Recipe Name
2. List of Ingredients (mark which ones are from the image)
3. Step-by-step Instructions
4. Why it is healthy (1 sentence)

Format the output clearly so it is easy to read.
"""

# --- UI LAYOUT ---
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image_Data = ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Meal.", use_container_width=True)
    
    # Process image once
    image_data = input_image_setup(uploaded_file)

# User input
user_input = st.text_input("Add details (e.g., 'I prefer spicy food'):")

# Create two columns for the buttons
col1, col2 = st.columns(2)

with col1:
    analyze_btn = st.button("🔥 Calculate Calories")

with col2:
    recipe_btn = st.button("👨‍🍳 Get Healthy Recipes")

# --- LOGIC ---

# 1. Calorie Calculation Logic
if analyze_btn:
    if uploaded_file is not None:
        with st.spinner("Analyzing calories..."):
            response = get_gemini_response(nutrition_prompt, image_data, user_input)
            st.subheader("Nutritional Analysis:")
            st.write(response)
    else:
        st.warning("Please upload an image first.")

# 2. Recipe Recommendation Logic
if recipe_btn:
    if uploaded_file is not None:
        with st.spinner("Chef AI is thinking of recipes..."):
            response = get_gemini_response(recipe_prompt, image_data, user_input)
            
            st.subheader("Recommended Healthy Recipes:")
            # We use an expander to show the full details cleanly
            with st.expander("View Recipes", expanded=True):
                st.write(response)
    else:
        st.warning("Please upload an image first.")
