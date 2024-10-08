import streamlit as st
from openai import OpenAI
import os

# Load the OpenAI API key from Streamlit secrets
api_key = st.secrets["openai_api_key"]
organization = st.secrets.get("openai_organization", None)  # Optional
project = st.secrets.get("openai_project", None)  # Optional

# Initialize the OpenAI client
client = OpenAI(api_key=api_key, organization=organization, project=project)

def create_chat_completion(system_prompt, user_prompt):
    """Creates a chat completion using OpenAI's API."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=4000
        )
        return response
    except Exception as e:
        return f"An error occurred: {e}"

# Streamlit UI
st.title("Weekly Meal Planner and Grocery List Generator")

st.write("Answer the following questions to generate your weekly meal plan and grocery list.")

diet_preference = st.selectbox(
    "What's your dietary preference?",
    ["Vegetarian", "Vegan", "Keto", "Paleo", "Standard"]
)

meals_per_day = st.slider(
    "How many meals do you want per day?",
    1, 5, 3
)

ingredients_to_avoid = st.text_input(
    "Any ingredients you want to avoid?"
)

if st.button("Generate Meal Plan and Grocery List"):
    system_prompt = """
    You are an AI chef assistant. Based on the user's dietary preferences, meals per day, and ingredients they want to avoid, generate a weekly meal plan with recipes and provide a grocery list.
    """

    user_prompt = f"""
    The user prefers a {diet_preference} diet, wants {meals_per_day} meals per day, and wants to avoid the following ingredients: {ingredients_to_avoid}.
    Please generate a meal plan for one week, including recipes for each meal, and a grocery list with quantities.
    """

    response = create_chat_completion(system_prompt, user_prompt)

    if isinstance(response, str):  # If there's an error message
        st.error(response)
    else:
        st.markdown(response.choices[0].message.content)
