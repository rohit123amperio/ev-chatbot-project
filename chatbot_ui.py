import streamlit as st
import requests

# ✅ Set API URL (Replace with your actual Render API URL)
API_URL = "https://ev-chatbot-project-1.onrender.com"  # Replace with your actual Render URL

st.title("🔋 EV Charging Load Prediction Chatbot")

# ✅ Define session state to store user responses
if "location" not in st.session_state:
    st.session_state.location = None
if "station_type" not in st.session_state:
    st.session_state.station_type = None
if "category" not in st.session_state:
    st.session_state.category = None

# ✅ Step 1: Ask for Location
if st.session_state.location is None:
    st.session_state.location = st.selectbox(
        "📍 Select the Location:", ["Berlin", "Munich", "Hamburg", "Cologne", "Frankfurt"]
    )

# ✅ Step 2: Ask for Station Type
if st.session_state.station_type is None:
    st.session_state.station_type = st.selectbox(
        "⚡ Select the Station Type:", ["AC", "DC", "HPC"]
    )

# ✅ Step 3: Ask for Charging Station Category
if st.session_state.category is None:
    st.session_state.category = st.selectbox(
        "🏪 Select the Charging Station Category:", ["Rewe", "Netto", "Penny"]
    )

# ✅ Predict Button
if st.button("🔮 Predict Charging Load"):
    # Create JSON payload
    user_query = {
        "message": f"predict for {st.session_state.location} {st.session_state.station_type} {st.session_state.category}"
    }
    
    # ✅ Send request to chatbot API
    try:
        response = requests.post(API_URL, json=user_query)
        if response.status_code == 200:
            st.success(f"🔋 Prediction: {response.json()['response']}")
        else:
            st.error("⚠️ Error: Could not retrieve prediction. Please check API connection.")
    except Exception as e:
        st.error(f"❌ Failed to connect to API: {e}")

# ✅ Additional Information
st.write("💡 Ask me anything related to EV Charging Load Prediction!")
st.write("🔗 [Visit API](https://ev-chatbot-project-1.onrender.com) for API details.")  # Update with your API URL