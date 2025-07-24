AI Nutritionist App 📸  
A web application that uses Google's Gemini AI to analyze images of meals and provide an estimated nutritional breakdown, including total calories.
Live Application:https://nutritionist-ai.streamlit.app/
Project Demonstration:Watch a live demonstration of the app on YouTube-https://www.youtube.com/watch?v=qVZLBTaRxrU

📜 Project Overview  
The AI Nutritionist App is a smart tool designed to help users quickly understand the nutritional content of their meals. By uploading a photo and providing optional details, users can get an AI-powered analysis that identifies food items, estimates quantities, and calculates the total calorie count. This project leverages a multimodal large language model to process both image and text inputs.


✨ Key Features  
Image-Based Analysis: Upload a JPG, JPEG, or PNG image of a meal for analysis.
Text Input for Detail: Add specific details about the meal (e.g., cooking methods, hidden ingredients) to refine the AI's analysis.
AI-Powered Nutrition Estimation: Utilizes the Google Gemini model to identify food items and estimate calories.
Interactive Web Interface: Built with Streamlit for a simple and responsive user experience.
Cloud-Deployed: Hosted on Streamlit Community Cloud for easy public access.
 

🛠️ Technology Stack  
Language: Python 3
Web Framework: Streamlit
AI Model: Google Gemini 1.5 Flash (google-generativeai)
Image Processing: Pillow
Environment Management:python-dotenv
Version Control: Git & GitHub
Deployment: Streamlit Community Cloud
 
⚙️ How It Works  
The user opens the Streamlit web application.
They upload an image of their meal and can optionally type extra details into a text box.
Upon clicking "Analyze My Meal," the image and text are sent to a backend function.
The function calls the Google Gemini API, passing the system prompt, the user's image, and the user's text.
The Gemini model analyzes the inputs and generates a nutritional breakdown.
The response is sent back to the Streamlit frontend and displayed to the user.
 
🚀 Running the Project Locally  
To set up and run this project on your local machine, follow these steps:
Prerequisites:
Git installed
Python 3.8 or higher installed
Clone the Repository:
Open your terminal and clone the GitHub repository.
Bash
git clone https://github.com/your-username/your-repository-name.git
cd your-repository-name
Create the Environment File:
Create a file named .env in the root of the project folder. This file will hold your secret API key. This file should never be committed to Git.
GOOGLE_API_KEY="YOUR_API_KEY_HERE"
Install Dependencies:
Install all the required Python libraries from the requirements.txt file.
Bash
pip install -r requirements.txt
Run the Application:
Launch the Streamlit app from your terminal.
Bash
python -m streamlit run app.py
The application will open in a new tab in your web browser.