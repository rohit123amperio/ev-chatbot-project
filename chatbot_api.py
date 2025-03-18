import joblib
import pandas as pd
from flask import Flask, request, jsonify

# ✅ Load trained model
model = joblib.load("charging_load_model.pkl")

# ✅ Load dataset for filtering
df = pd.read_csv("Processed_Stations.csv")

# ✅ Flask App
app = Flask(__name__)

@app.route("/chatbot", methods=["POST"])
def chatbot():
    try:
        user_input = request.json.get("message", "").lower()
        print(f"🔹 Received input: {user_input}")

        # ✅ Extract user selection
        words = user_input.split()
        if len(words) < 4:
            return jsonify({"error": "Invalid input format. Expected 'predict for City StationType Category'."})

        city = words[2]  # Extract city
        station_type = words[3]  # Extract station type
        category = words[4]  # Extract category

        # ✅ Convert Inputs to Encoded Values
        station_type_code = {"AC": 0, "DC": 1, "HPC": 2}.get(station_type, -1)
        category_code = {"Rewe": 0, "Netto": 1, "Penny": 2}.get(category, -1)

        city_data = df[df["Address"].str.contains(city)]
        if city_data.empty:
            return jsonify({"error": f"No data found for city: {city}"})

        city_code = city_data.iloc[0]["City"]

        if station_type_code == -1 or category_code == -1:
            return jsonify({"error": "Invalid station type or category."})

        # ✅ Simulate Random Peak Hours & Weather
        peak_hours = 1  # Assume Peak Hours
        weather = 1  # Assume Normal Weather

        # ✅ Make Prediction
        sample_input = [[station_type_code, category_code, city_code, peak_hours, weather]]
        prediction = model.predict(sample_input)[0]

        response_msg = {"response": f"The predicted charging load for {city} ({station_type}, {category}) is {prediction:.2f} kW."}
        print(f"✅ API Response: {response_msg}")

        return jsonify(response_msg)

    except Exception as e:
        print(f"❌ Error in API: {e}")
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)