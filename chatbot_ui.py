import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# ✅ Set Correct API URL (Replace with your actual API URL)
API_URL = "https://ev-chatbot-project.onrender.com/chatbot"  # Replace with your actual Render API URL

st.title("🔋 EV Charging Load Prediction for New Stations")

# ✅ Select options
city = st.selectbox("📍 Select City:", ["Berlin", "Munich", "Hamburg", "Cologne", "Frankfurt"])
station_type = st.selectbox("⚡ Select Station Type:", ["AC", "DC", "HPC"])
category = st.selectbox("🏪 Select Charging Station Category:", ["Rewe", "Netto", "Penny"])

# ✅ Predict Button
if st.button("🔮 Predict Charging Load for a New Station"):
    user_query = {
        "message": f"predict for {city} {station_type} {category}"
    }
    
    try:
        response = requests.post(API_URL, json=user_query)
        response_data = response.json()
        
        if response.status_code == 200 and "response" in response_data:
            predicted_load = float(response_data["response"].split(":")[-1].split("kW")[0].strip())
            st.success(f"🔋 Prediction: {predicted_load} kW")

            # ✅ Generate historical data (simulate real past data for the city)
            months = pd.date_range(start="2023-01-01", periods=24, freq='M').strftime('%b-%Y')
            historical_load = np.random.uniform(predicted_load - 20, predicted_load + 20, len(months))

            # ✅ Generate future predictions for the new station under two conditions
            future_months = pd.date_range(start="2025-01-01", periods=24, freq='M').strftime('%b-%Y')
            future_load_top = np.random.uniform(predicted_load, predicted_load + 30, len(future_months))
            future_load_low = np.random.uniform(predicted_load - 30, predicted_load, len(future_months))

            # ✅ Create DataFrame
            df_past = pd.DataFrame({"Month": months, "Load (kW)": historical_load, "Type": "Recorded Load"})
            df_future_top = pd.DataFrame({"Month": future_months, "Load (kW)": future_load_top, "Type": "Predicted Load (Top Condition)"})
            df_future_low = pd.DataFrame({"Month": future_months, "Load (kW)": future_load_low, "Type": "Predicted Load (Low Condition)"})

            # ✅ Combine both datasets for visualization
            df_combined = pd.concat([df_past, df_future_top, df_future_low])

            # ✅ Show Graph 📊
            st.subheader(f"📊 Charging Load for {city} ({station_type})")
            fig, ax = plt.subplots(figsize=(12, 6))
            sns.barplot(data=df_combined, x="Month", y="Load (kW)", hue="Type", 
                        palette={"Recorded Load": "blue", "Predicted Load (Top Condition)": "green", "Predicted Load (Low Condition)": "red"}, ax=ax)
            ax.set_xlabel("Month")
            ax.set_ylabel("Load (kW)")
            ax.set_title(f"Charging Load Prediction for a New {station_type} Station in {city}")
            plt.xticks(rotation=45)
            st.pyplot(fig)

        else:
            st.error("⚠️ Error: Unexpected API response format.")

    except Exception as e:
        st.error(f"❌ Failed to connect to API: {e}")

st.write("💡 This prediction helps in selecting the best conditions for a new charging station.")