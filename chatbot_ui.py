import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# ✅ Set Correct API URL
API_URL = "https://ev-chatbot-project.onrender.com/chatbot"  # Fixed API URL

st.title("🔋 EV Charging Load Prediction for New Stations")

# ✅ Select options
city = st.selectbox("📍 Select City:", ["Berlin", "Munich", "Hamburg", "Cologne", "Frankfurt"])
station_type = st.selectbox("⚡ Select Station Type:", ["AC", "DC", "HPC"])
category = st.selectbox("🏪 Select Charging Station Category:", ["Rewe", "Netto", "Penny"])

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