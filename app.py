import streamlit as st
import requests
import os
from dotenv import load_dotenv
from PIL import Image
from transformers import pipeline

# Load environment variables
load_dotenv()

# --- CONFIGURATION (The "Engineering" Part) ---
# You must set these in your .env file or Streamlit Secrets!
NUTRITIONIX_APP_ID = os.getenv("NUTRITIONIX_APP_ID")
NUTRITIONIX_API_KEY = os.getenv("NUTRITIONIX_API_KEY")
EDAMAM_APP_ID = os.getenv("EDAMAM_APP_ID")
EDAMAM_APP_KEY = os.getenv("EDAMAM_APP_KEY")

# --- 1. THE EYES: Computer Vision Model ---
# We use a specific model trained on the "Food-101" dataset.
# This runs LOCALLY (or on the server), not via an API call to Google.
@st.cache_resource
def load_image_model():
    # Downloads a ~300MB model specifically for food recognition
    classifier = pipeline("image-classification", model="nateraw/food")
    return classifier

# --- 2. THE BRAIN: Nutritionix API ---
# We send the detected label (e.g., "hamburger") to get scientific facts.
def get_calories(food_name):
    endpoint = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    headers = {
        "x-app-id": NUTRITIONIX_APP_ID,
        "x-app-key": NUTRITIONIX_API_KEY,
        "Content-Type": "application/json"
    }
    # We default to "1 serving" to get standard data
    query = {"query": f"1 serving of {food_name}"}
    
    try:
        response = requests.post(endpoint, headers=headers, json=query)
        if response.status_code == 200:
            data = response.json()['foods'][0]
            return {
                "calories": data['nf_calories'],
                "protein": data['nf_protein'],
                "carbs": data['nf_total_carbohydrate'],
                "fats": data['nf_total_fat']
            }
        else:
            return None
    except:
        return None

# --- 3. THE CHEF: Edamam Recipe API ---
# We search a recipe database using the detected label.
def get_recipes(food_name):
    url = f"https://api.edamam.com/search?q={food_name}&app_id={EDAMAM_APP_ID}&app_key={EDAMAM_APP_KEY}&to=3"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            recipes = []
            for hit in data['hits']:
                r = hit['recipe']
                recipes.append({
                    "label": r['label'],
                    "url": r['url'],
                    "image": r['image'],
                    "calories": round(r['calories'] / r['yield']) # Per serving
                })
            return recipes
        return []
    except:
        return []

# --- STREAMLIT APP UI ---
st.set_page_config(page_title="Smart Nutrition Analyzer", layout="wide")

st.title("🥗 System-Integrated Nutrition Analyzer")
st.caption("Powered by HuggingFace Vision, Nutritionix API, and Edamam API")

# Sidebar for controls
with st.sidebar:
    st.header("Project Architecture")
    st.markdown("""
    This app demonstrates a **3-stage pipeline**:
    1. **Vision:** `nateraw/food` (ViT) identifies the food.
    2. **Data:** `Nutritionix` fetches nutritional facts.
    3. **Search:** `Edamam` retrieves relevant recipes.
    """)

uploaded_file = st.file_uploader("Upload a food image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 1. Show the image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", width=400)
    
    if st.button("Analyze Image"):
        with st.spinner("Step 1: Running Computer Vision Model..."):
            # Load model and predict
            classifier = load_image_model()
            predictions = classifier(image)
            
            # Get the top prediction
            top_food = predictions[0]['label']
            confidence = predictions[0]['score']
            
            # Fix label format (e.g. "hamburger" instead of "hamburger_steak")
            food_label = top_food.replace("_", " ")
        
        st.success(f"✅ **Identification:** I am {confidence*100:.1f}% sure this is **{food_label.title()}**.")
        
        # Create columns for the next steps
        col1, col2 = st.columns(2)
        
        # Step 2: Get Nutrition
        with col1:
            st.subheader(f"📊 Nutritional Facts ({food_label.title()})")
            with st.spinner("Step 2: Querying Nutritionix Database..."):
                nutrition = get_calories(food_label)
                
                if nutrition:
                    st.metric("Calories", f"{nutrition['calories']} kcal")
                    st.write(f"**Protein:** {nutrition['protein']}g")
                    st.write(f"**Carbs:** {nutrition['carbs']}g")
                    st.write(f"**Fats:** {nutrition['fats']}g")
                else:
                    st.error("Could not fetch data from Nutritionix.")

        # Step 3: Get Recipes
        with col2:
            st.subheader(f"👨‍🍳 Recipes for {food_label.title()}")
            with st.spinner("Step 3: Searching Edamam Recipe Index..."):
                recipes = get_recipes(food_label)
                
                if recipes:
                    for r in recipes:
                        with st.expander(f"{r['label']} ({r['calories']} kcal)"):
                            st.image(r['image'], width=100)
                            st.markdown(f"[View Recipe Instructions]({r['url']})")
                else:
                    st.info("No recipes found for this item.")
