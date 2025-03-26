import streamlit as st
import openai
import pandas as pd

# OpenAI API Key
openai.api_key = "YOUR_OPENAI_API_KEY"

# Load Nutrition Data (Sample Data - Add more entries for better results)
data = pd.DataFrame({
    "Food": ["Apple", "Banana", "Egg", "Chicken", "Broccoli"],
    "Calories": [52, 89, 155, 239, 55],
    "Protein (g)": [0.3, 1.1, 13, 27, 3.7],
    "Fat (g)": [0.2, 0.3, 11, 14, 0.6],
    "Carbs (g)": [14, 23, 1.1, 0, 11],
    "Benefits": [
        "Rich in fiber, good for digestion.",
        "High in potassium, boosts energy.",
        "Excellent source of protein and nutrients.",
        "High in protein, ideal for muscle growth.",
        "Rich in vitamins, great for immunity."
    ]
})

# Streamlit UI
st.title("AI Nutrition Chatbot")
st.write("Get personalized nutrition advice based on your diet needs.")

# User Input
user_input = st.text_input("Ask me anything about nutrition:")

# AI Response with Nutrition Data Integration
if st.button("Get Advice") and user_input.strip():
    # Try to match food data for better response
    matched_food = data[data['Food'].str.contains(user_input, case=False)]
    
    if not matched_food.empty:
        st.write("Here's some nutrition info for you:")
        st.dataframe(matched_food)
    else:
        # Use AI for detailed nutrition advice
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )
        st.success(response['choices'][0]['message']['content'].strip())
