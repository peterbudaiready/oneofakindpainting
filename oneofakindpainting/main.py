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
logo_path = "oneofakindpainting/logo.png"  # Update this path if needed

if logo_path:  # Check if the path is not empty
    st.image(logo_path, width=300)  # Adjust width as needed
else:
    st.warning("⚠️ Logo not found. Make sure 'logo.png' exists.")

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 1
    st.session_state.answers = {}

# Function to navigate
def next_step():
    st.session_state.step += 1

    # Trigger webhook when reaching step 6
    if st.session_state.step == 7:
        formatted_data = format_answers()
        send_to_webhook(formatted_data)

def prev_step():
    if st.session_state.step > 1:
        st.session_state.step -= 1

# Function to send data to webhook
def send_to_webhook(data):
    webhook_url = "https://hook.eu2.make.com/mztwgjgpnu3aspgpslwabe3wr47c3lqq"  # Replace with your webhook URL
    try:
        response = requests.post(webhook_url, json=data)
        if response.status_code == 200:
            st.success("Price estimate submition was sucessful!")
        else:
            st.error(f"Failed to send data. Status code: {response.status_code}")
    except Exception as e:
        st.error(f"Error sending data: {e}")

# Function to format answers nicely
def format_answers():
    formatted_data = {
        "Painting Type": st.session_state.answers.get(1, "Not answered"),
        "Details": {}
    }
    for step, question in form_steps.items():
        if step != 1:  # Skip the painting type (already included)
            formatted_data["Details"][question["question"]] = st.session_state.answers.get(step, "Not answered")

    return formatted_data

# Define form flow
form_steps = {
    1: {"question": "What kind of painting/staining do you need?", "options": ["Interior", "Exterior", "Speciality finishes"], "type": "radio"},
}

# Check if answer to step 1 exists and update dynamically
def update_form_steps():
    painting_type = st.session_state.answers.get(1)
    steps = {}
    if painting_type == "Interior":
        steps = {
            2: {"question": "What needs to be painted?", "options": ["Ceiling", "Wall", "Trim", "Not sure/Other"], "type": "checkbox"},
            3: {"question": "How many rooms do you want to paint?", "options": ["1 - 2 Rooms", "3 - 4 Rooms", "5+ Rooms"], "type": "radio"},
            4: {"question": "When would you like this request to be completed?", "options": ["Urgent (1-2 days)", "Within 2 weeks", "More than 2 weeks", "Not sure"], "type": "radio"},
            5: {"question": "What is the approximate living square footage of your home?", "min": 1000, "max": 40000, "step": 100, "type": "slider"},
            6: {"question": "Please tell us a little about your project:", "type": "text"}
        }
    elif painting_type == "Exterior":
        steps = {
            2: {"question": "What do you want to paint?", "options": ["More than half of the home exterior (3-4 sides)", "Less than half of the home exterior (1-2 sides)", "Exterior trim", "A deck or porch", "A fence", "Shutters and/or a front door", "Garage exterior", "Other"], "type": "checkbox"},
            3: {"question": "What is the approximate living square footage of your home?", "min": 1000, "max": 40000, "step": 100, "type": "slider"},
            4: {"question": "How many stories is your home?", "options": ["Two stories or more", "One story"], "type": "radio"},
            5: {"question": "What is the primary exterior surface material of your home?", "options": ["Wood", "Metal", "Brick", "Stone", "Stucco", "Other/ I don't know"], "type": "radio"},
            6: {"question": "Please tell us a little about your project:", "type": "text"}
        }
    elif painting_type == "Speciality finishes":
        steps = {
            2: {"question": "What type of speciality finishes are you looking for?", "options": ["Textures", "Faux finish", "Mural or trompe l’oeil", "Metal roof", "Small features/items in a room"], "type": "radio"},
            3: {"question": "What kind of texturing do you need?", "options": ["Apply texture to unfinished drywall", "Match new drywall to existing walls/ceiling", "Repair/patch drywall", "Prepare for wallpapers/Special finish", "Other"], "type": "checkbox"},
            4: {"question": "What kind of location is this?", "options": ["Home", "Business"], "type": "radio"},
            5: {"question": "When would you like this request to be completed?", "options": ["Urgent (1-2 days)", "Within 2 weeks", "More than 2 weeks", "Not sure"], "type": "radio"},
            6: {"question": "Please tell us a little about your project:", "type": "text"}
        }
    return steps

workflow_steps = update_form_steps()
form_steps.update(workflow_steps)

# Display current question
current_step = st.session_state.step
if current_step in form_steps:
    step_data = form_steps[current_step]
    st.markdown(f"## {step_data['question']}")
    
    if step_data['type'] == "radio":
        st.session_state.answers[current_step] = st.radio("", step_data['options'], key=current_step)
    elif step_data['type'] == "checkbox":
        st.session_state.answers[current_step] = st.multiselect("", step_data['options'], key=current_step)
    elif step_data['type'] == "slider":
        st.session_state.answers[current_step] = st.slider("", step_data['min'], step_data['max'], step_data['min'], step_data['step'], key=current_step)
    elif step_data['type'] == "text":
        st.session_state.answers[current_step] = st.text_area("", key=current_step)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.button("Previous", on_click=prev_step, disabled=current_step == 1)
    with col2:
        st.button("Next", on_click=next_step)

# Display final price estimate
if current_step > max(form_steps.keys()):
    sqft = st.session_state.answers.get(5, 1000)

    # Ensure sqft is a valid integer
    if isinstance(sqft, list) and sqft:  # If it's a list, get the first value
        sqft = int(sqft[0])  
    elif isinstance(sqft, str):  # Convert string inputs to integer
        sqft = int(sqft) if sqft.isdigit() else 1000
    else:
        sqft = int(sqft)  # Ensure it's an integer

    low_price = sqft * 1.25 if st.session_state.answers.get(1) != "Speciality finishes" else 382
    high_price = sqft * 1.58 if st.session_state.answers.get(1) != "Speciality finishes" else 2350

    st.markdown("""
    <style>
    .big-font {
    font-size:300px !important;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown("## Thank you!")
    st.markdown(f"Your approximate estimate for your work is between :red[**${low_price:.2f}] to :red[${high_price:.2f}**.]")

    if st.button("Get a special price!"):
        st.markdown("[Click here to call](tel:+17202554154)")

    st.markdown("### [www.1ofakindpainting.com](https://www.1ofakindpainting.com)")
