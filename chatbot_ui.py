import streamlit as st
import requests

# ✅ Set Correct API URL
API_URL = "https://ev-chatbot-project.onrender.com/chatbot"  # Fixed API URL

st.title("🔋 EV Charging Load Prediction Chatbot")

# ✅ Initialize session state correctly
if "location" not in st.session_state:
    st.session_state.location = "Berlin"
if "station_type" not in st.session_state:
    st.session_state.station_type = "AC"
if "category" not in st.session_state:
    st.session_state.category = "Rewe"

# ✅ Select options
st.session_state.location = st.selectbox("📍 Select Location:", ["Berlin", "Munich", "Hamburg", "Cologne", "Frankfurt"])
st.session_state.station_type = st.selectbox("⚡ Select Station Type:", ["AC", "DC", "HPC"])
st.session_state.category = st.selectbox("🏪 Select Charging Station Category:", ["Rewe", "Netto", "Penny"])

# ✅ Predict Button
if st.button("🔮 Predict Charging Load"):
    user_query = {
        "message": f"predict for {st.session_state.location} {st.session_state.station_type} {st.session_state.category}"
    }
    
    try:
        response = requests.post(API_URL, json=user_query)
        response_data = response.json()
        
        if response.status_code == 200 and "response" in response_data:
            st.success(f"🔋 Prediction: {response_data['response']}")
        else:
            st.error("⚠️ Error: Unexpected API response format.")

    except Exception as e:
        st.error(f"❌ Failed to connect to API: {e}")

# ✅ Additional Information
st.write("💡 Ask me anything related to EV Charging Load Prediction!")
st.write(f"🔗 [Visit API]({API_URL})")  # Corrected API link