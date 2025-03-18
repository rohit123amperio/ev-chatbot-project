import streamlit as st
import requests

# Set API URL (Replace with your actual Render URL)
API_URL = "https://ev-chatbot-project-1.onrender.com"  # Replace with your actual Render API URL

st.title("🔋 EV Charging Load Prediction Chatbot")

# Define session state to store user responses
if "location" not in st.session_state:
    st.session_state.location = None
if "station_type" not in st.session_state:
    st.session_state.station_type = None
if "category" not in st.session_state:
    st.session_state.category = None

# Step 1: Ask for Location
if st.session_state.location is None:
    st.session_state.location = st.selectbox(
        "Select the location:", ["Berlin", "Munich", "Hamburg", "Cologne", "Frankfurt"]
    )

# Step 2: Ask for Station Type
if st.session_state.station_type is None:
    st.session_state.station_type = st.selectbox(
        "Select the station type:", ["AC", "DC", "HPC"]
    )

# Step 3: Ask for Category
if st.session_state.category is None:
    st.session_state.category = st.selectbox(
        "Select the charging station category:", ["Rewe", "Netto", "Penny"]
    )

# Predict Button
if st.button("Predict Charging Load"):
    # Send request to chatbot API
    user_query = {
        "message": f"predict for {st.session_state.location} {st.session_state.station_type} {st.session_state.category}"
    }
    response = requests.post(API_URL, json=user_query)

    # Display chatbot response
    if response.status_code == 200:
        st.write(f"🔮 Prediction: {response.json()['response']}")
    else:
        st.write("⚠️ Error: Could not retrieve prediction.")

st.write("Ask me anything related to EV Charging Load Prediction!")
