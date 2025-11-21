import streamlit as st
import google.generativeai as genai
import os

# Load the key from secrets
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

st.title("🔑 API Permission Test")

try:
    st.write("Attempting to connect to Google...")
    
    # This function asks Google for the list of available models
    models = genai.list_models()
    
    found_any = False
    st.write("### Available Models for your Key:")
    
    for m in models:
        if 'generateContent' in m.supported_generation_methods:
            found_any = True
            # We print the EXACT system name you need to use
            st.code(f"model = genai.GenerativeModel('{m.name}')")
            
    if not found_any:
        st.error("❌ Connection successful, but NO models are enabled. Go to Google Cloud Console and enable 'Generative Language API'.")
    else:
        st.success("✅ Success! Copy one of the model names above into your main app.")

except Exception as e:
    st.error(f"❌ Connection Failed: {e}")
