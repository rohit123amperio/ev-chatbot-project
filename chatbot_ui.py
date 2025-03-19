import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.express as px

# ✅ Set API URL (Replace with your actual API URL)
API_URL = "https://ev-chatbot-project.onrender.com/chatbot"  # Replace with your actual Render API URL

# 🎨 Custom Styling for UI
st.markdown(
    """
    <style>
    .main-title { font-size: 32px; text-align: center; font-weight: bold; color: #ff4b4b; }
    .sub-title { font-size: 24px; text-align: center; color: #4caf50; }
    .highlight { font-size: 20px; text-align: center; font-weight: bold; color: #ff9800; }
    .chat-container { background-color: #f4f4f4; padding: 10px; border-radius: 10px; }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<p class="main-title">💬 EV Charging Load Chatbot 🚗⚡</p>', unsafe_allow_html=True)

# ✅ Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# ✅ Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ✅ User Input
user_input = st.chat_input("Ask me about EV charging load predictions, peak hours, or station performance...")

if user_input:
    # ✅ Display User Message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # ✅ Send Query to API
    user_query = {"message": user_input}

    try:
        response = requests.post(API_URL, json=user_query)
        response_data = response.json()

        if response.status_code == 200 and "response" in response_data:
            chatbot_response = response_data["response"]
        else:
            chatbot_response = "⚠️ Error: Unexpected API response format."

    except Exception as e:
        chatbot_response = f"❌ Failed to connect to API: {e}"

    # ✅ Display Chatbot Response
    st.session_state.messages.append({"role": "assistant", "content": chatbot_response})
    with st.chat_message("assistant"):
        st.markdown(chatbot_response)

    # ✅ Generate Predictions for Graphs & Tables if the query is a station prediction
    if "predict for" in user_input.lower():
        try:
            user_words = user_input.split()
            if len(user_words) >= 3:
                city, station_type, category = user_words[-3:]  # Extracts last 3 words
            else:
                raise ValueError("Not enough input data for prediction.")

            # ✅ Simulate Data for Visualization
            months = pd.date_range(start="2023-01-01", periods=24, freq='M').strftime('%b-%Y')
            historical_load = np.random.uniform(20, 100, len(months))

            future_months = pd.date_range(start="2025-01-01", periods=24, freq='M').strftime('%b-%Y')
            future_load_top = np.random.uniform(40, 130, len(future_months))
            future_load_low = np.random.uniform(20, 90, len(future_months))

            # ✅ Create DataFrame
            df_past = pd.DataFrame({"Month": months, "Load (kW)": historical_load, "Type": "Recorded Load"})
            df_future_top = pd.DataFrame({"Month": future_months, "Load (kW)": future_load_top, "Type": "Predicted Load (Top Condition)"})
            df_future_low = pd.DataFrame({"Month": future_months, "Load (kW)": future_load_low, "Type": "Predicted Load (Low Condition)"})

            # ✅ Combine Data for Visualization
            df_combined = pd.concat([df_past, df_future_top, df_future_low])

            # ✅ Show Interactive Graph 📊
            st.subheader(f"📊 Charging Load for {city} ({station_type})")
            fig = px.bar(df_combined, x="Month", y="Load (kW)", color="Type",
                         color_discrete_map={"Recorded Load": "blue", 
                                             "Predicted Load (Top Condition)": "green", 
                                             "Predicted Load (Low Condition)": "red"},
                         title=f"Charging Load Prediction for a New {station_type} Station in {city}")
            st.plotly_chart(fig)

            # ✅ Create a Table 📋 (Top Performers)
            st.subheader("📅 **Monthly Load Predictions (Top Performer)**")
            df_table_top = df_future_top.copy()
            df_table_top["Load (kW)"] = df_table_top["Load (kW)"].round(2)

            # ✅ Show Load Predictions Table
            st.dataframe(df_table_top)
        
        except ValueError:
            st.error("⚠️ Error: Could not extract city, station type, and category from user input.")

# ✅ Additional Information
st.write("💡 Ask me anything related to EV Charging Load Prediction!")
st.write(f"🔗 [Visit API]({API_URL})")