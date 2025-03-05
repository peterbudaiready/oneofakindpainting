import streamlit as st
import json
import requests

# Set page configuration with title and favicon (optional)
st.set_page_config(
    page_title="My Website",
    page_icon="logo.png",  # Ensure the path is correct
    initial_sidebar_state="collapsed"
)

# Display logo at the top
logo_path = "logo.png"  # Update this path if needed

if logo_path:  # Check if the path is not empty
    st.image(logo_path, width=300)  # Adjust width as needed
else:
    st.warning("⚠️ Logo not found. Make sure 'assets/logo.png' exists.")

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 1
    st.session_state.answers = {}

# Function to send data to webhook
def send_to_webhook(data):
    webhook_url = "https://hook.eu2.make.com/rv5a1aj2gggq9o4pkgsfuiwcbxnxyyxg"  # Replace with your webhook URL
    try:
        response = requests.post(webhook_url, json=data)
        if response.status_code == 200:
            st.success("Form submission was successful!")
        else:
            st.error(f"Failed to send data. Status code: {response.status_code}")
    except Exception as e:
        st.error(f"Error sending data: {e}")

# Define form structure
st.markdown("## Simple Painting Industry Form")

name = st.text_input("What is your name?")
years_in_industry = st.slider("How many years are you in the painting industry?", 1, 50, 1)
team_size = st.slider("How many people do you have in your team?", 1, 50, 1)
speaks_english = st.radio("Does at least one of your team members speak English?", ["Yes", "No"])
work_vehicle = st.radio("Do you have a work vehicle?", ["Yes", "No"])
phone_number = st.text_input("Your phone number")
email = st.text_input("Your email")

# Collect responses and submit
data = {
    "Name": name,
    "Years in Industry": years_in_industry,
    "Team Size": team_size,
    "Speaks English": speaks_english,
    "Work Vehicle": work_vehicle,
    "Phone Number": phone_number,
    "Email": email
}

if st.button("Submit"):
    send_to_webhook(data)
