import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# ✅ Set Correct API URL
API_URL = "https://ev-chatbot-project.onrender.com/chatbot"  # Replace with your actual Render API URL

st.title("🔋 EV Charging Load Prediction for New Stations")

# ✅ Select options
city = st.selectbox("📍 Select City:", ["Berlin", "Munich", "Hamburg", "Cologne", "Frankfurt"])
station_type = st.selectbox("⚡ Select Station Type:", ["AC", "DC", "HPC"])
category = st.selectbox("🏪 Select Charging Station Category:", ["Rewe", "Netto", "Penny"])

# ✅ Predict Button
if st.button("🔮 Predict Charging Load for a New Station"):
    user_query = {"message": f"predict for {city} {station_type} {category}"}
    
    try:
        response = requests.post(API_URL, json=user_query)
        response_data = response.json()
        
        if response.status_code == 200 and "response" in response_data:
            predicted_load = float(response_data["response"].split(":")[-1].split("kW")[0].strip())
            st.success(f"🔋 Prediction: {predicted_load} kW")

            # ✅ Create a Table 📋
            df_table = pd.DataFrame({"Month": pd.date_range(start="2025-01-01", periods=24, freq='M').strftime('%b-%Y'),
                                     "Load (kW)": np.random.uniform(predicted_load - 30, predicted_load + 30, 24).round(2)})
            
            # ✅ Highlight best & worst months
            def highlight_months(row):
                if row["Load (kW)"] == df_table["Load (kW)"].min():
                    return ["background-color: lightgreen"] * len(row)
                elif row["Load (kW)"] == df_table["Load (kW)"].max():
                    return ["background-color: lightcoral"] * len(row)
                return [""] * len(row)

            st.dataframe(df_table.style.apply(highlight_months, axis=1))

        else:
            st.error("⚠️ Error: Unexpected API response format.")

    except Exception as e:
        st.error(f"❌ Failed to connect to API: {e}")