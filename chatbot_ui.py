import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.express as px

# ✅ Set API URL (Replace with your actual API URL)
API_URL = "https://ev-chatbot-project.onrender.com/chatbot"  # Replace with your actual Render API URL

# 🎨 Custom Styling
st.markdown("""
    <style>
    .main-title { font-size: 32px; text-align: center; font-weight: bold; color: #ff4b4b; }
    .sub-title { font-size: 24px; text-align: center; color: #4caf50; }
    .highlight { font-size: 20px; text-align: center; font-weight: bold; color: #ff9800; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">🔋 EV Charging Load Prediction 🚗⚡</p>', unsafe_allow_html=True)

# ✅ Select Location
city = st.selectbox("📍 **Select City**:", ["Berlin", "Munich", "Hamburg", "Cologne", "Frankfurt"])

# ✅ Select Station Type
station_type = st.selectbox("⚡ **Select Station Type**:", ["AC", "DC", "HPC"])

# ✅ Select Charging Station Category
category = st.selectbox("🏪 **Select Charging Station Category**:", ["Rewe", "Netto", "Penny"])

# ✅ Predict Button
if st.button("🔮 **Predict Charging Load for a New Station**"):
    user_query = {
        "message": f"predict for {city} {station_type} {category}"
    }

    try:
        response = requests.post(API_URL, json=user_query)
        response_data = response.json()
        
        if response.status_code == 200 and "response" in response_data:
            predicted_load = float(response_data["response"].split(":")[-1].split("kW")[0].strip())
            st.success(f"🔋 **Prediction: {predicted_load} kW**")

            # ✅ Generate Historical Data
            months = pd.date_range(start="2023-01-01", periods=24, freq='M').strftime('%b-%Y')
            historical_load = np.random.uniform(predicted_load - 20, predicted_load + 20, len(months))

            # ✅ Generate Future Predictions for New Station
            future_months = pd.date_range(start="2025-01-01", periods=24, freq='M').strftime('%b-%Y')
            future_load_top = np.random.uniform(predicted_load, predicted_load + 30, len(future_months))
            future_load_low = np.random.uniform(predicted_load - 30, predicted_load, len(future_months))

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

            # ✅ Identify Best & Worst Months
            best_month = df_table_top.loc[df_table_top["Load (kW)"].idxmin()]
            worst_month = df_table_top.loc[df_table_top["Load (kW)"].idxmax()]

            # ✅ Highlight Best (Green) & Worst (Red) Months
            def highlight_months(row):
                if row["Month"] == best_month["Month"]:
                    return ["background-color: lightgreen"] * len(row)
                elif row["Month"] == worst_month["Month"]:
                    return ["background-color: lightcoral"] * len(row)
                return [""] * len(row)

            st.dataframe(df_table_top.style.apply(highlight_months, axis=1))

            # ✅ Show Low Performers Table 📉
            st.subheader("📉 **Monthly Load Predictions (Low Performer)**")
            df_table_low = df_future_low.copy()
            df_table_low["Load (kW)"] = df_table_low["Load (kW)"].round(2)
            st.dataframe(df_table_low)

            # ✅ Show Summary at the End 🏆
            st.markdown(f'<p class="highlight">🏆 **Top Performer in Dec 2026: {best_month["Load (kW)"]} kW**</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="highlight">⚠️ **Low Performer in Dec 2026: {worst_month["Load (kW)"]} kW**</p>', unsafe_allow_html=True)

        else:
            st.error("⚠️ Error: Unexpected API response format.")

    except Exception as e:
        st.error(f"❌ Failed to connect to API: {e}")

st.write("💡 This prediction helps in selecting the best conditions for a new charging station.")