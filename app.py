import streamlit as st
import requests
import os
from dotenv import load_dotenv
from PIL import Image
from transformers import pipeline

# Load environment variables
load_dotenv()

# --- CONFIGURATION ---
# Get your free key from: https://calorieninjas.com/api
CALORIE_NINJAS_API_KEY = os.getenv("CALORIE_NINJAS_API_KEY")

# --- 1. THE EYES: Computer Vision Model ---
# This downloads a ~300MB model specifically for food recognition.
# It runs LOCALLY on the Streamlit server (Free).
@st.cache_resource
def load_image_model():
    classifier = pipeline("image-classification", model="nateraw/food")
    return classifier

# --- 2. THE BRAIN: CalorieNinjas API ---
# No Credit Card required. 10k calls/month free.
def get_calories(food_name):
    api_url = f'https://api.calorieninjas.com/v1/nutrition?query={food_name}'
    headers = {'X-Api-Key': CALORIE_NINJAS_API_KEY}
    
    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if len(data['items']) > 0:
                item = data['items'][0]
                return {
                    "name": item['name'],
                    "calories": item['calories'],
                    "protein": item['protein_g'],
                    "carbs": item['carbohydrates_total_g'],
                    "fats": item['fat_total_g']
                }
        return None
    except Exception as e:
        return None

# --- 3. THE CHEF: TheMealDB API ---
# Public Test Key '1' is free for educational use.
def get_recipes(food_name):
    # Search for meals by name
    url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={food_name}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            meals = data.get('meals')
            if meals:
                # Return the top 3 recipes
                return meals[:3]
        return []
    except:
        return []

# --- STREAMLIT APP UI ---
st.set_page_config(page_title="Smart Nutrition Analyzer", layout="wide")

st.title("🥗 System-Integrated Nutrition Analyzer")
st.caption("Powered by HuggingFace (Vision), CalorieNinjas (Facts), and TheMealDB (Recipes)")

# Sidebar for architecture info
with st.sidebar:
    st.header("System Architecture")
    st.markdown("""
    This app uses a **Modular Pipeline**:
    1. **Vision:** `ViT Model` (Local AI) identifies the food.
    2. **Logic:** `CalorieNinjas API` fetches nutritional data.
    3. **Search:** `TheMealDB API` retrieves recipes.
    """)
    
    # Check if API Key is present
    if not CALORIE_NINJAS_API_KEY:
        st.error("⚠️ Missing API Key!")
        st.info("Get your free key at calorieninjas.com and add it to Secrets as `CALORIE_NINJAS_API_KEY`.")

uploaded_file = st.file_uploader("Upload a food image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 1. Show the image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", width=400)
    
    if st.button("Analyze Image"):
        # STEP 1: VISION
        with st.spinner("Step 1: Running Computer Vision Model..."):
            classifier = load_image_model()
            predictions = classifier(image)
            
            # Get top prediction
            top_food = predictions[0]['label']
            confidence = predictions[0]['score']
            
            # Clean up label (e.g. "hamburger_" -> "hamburger")
            food_label = top_food.replace("_", " ")
        
        st.success(f"✅ **Identification:** I am {confidence*100:.1f}% sure this is **{food_label.title()}**.")
        
        # Create columns for details
        col1, col2 = st.columns(2)
        
        # STEP 2: NUTRITION
        with col1:
            st.subheader(f"📊 Nutritional Facts ({food_label.title()})")
            with st.spinner("Step 2: Querying CalorieNinjas..."):
                nutrition = get_calories(food_label)
                
                if nutrition:
                    st.metric("Calories", f"{nutrition['calories']} kcal")
                    st.write(f"**Protein:** {nutrition['protein']}g")
                    st.write(f"**Carbs:** {nutrition['carbs']}g")
                    st.write(f"**Fats:** {nutrition['fats']}g")
                else:
                    st.warning("No specific nutrition data found for this item.")

        # STEP 3: RECIPES
        with col2:
            st.subheader(f"👨‍🍳 Recipes for {food_label.title()}")
            with st.spinner("Step 3: Searching TheMealDB..."):
                recipes = get_recipes(food_label)
                
                if recipes:
                    for r in recipes:
                        with st.expander(f"{r['strMeal']}"):
                            st.image(r['strMealThumb'], width=150)
                            st.write(f"**Category:** {r['strCategory']}")
                            st.markdown(f"[View Instructions]({r['strSource']})")
                else:
                    st.info("No recipes found for this specific dish.")
