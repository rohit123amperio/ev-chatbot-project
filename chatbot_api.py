import joblib
import pandas as pd
from flask import Flask, request, jsonify

# Load trained model
model = joblib.load("charging_load_model.pkl")

# Load dataset for filtering
df = pd.read_csv("Processed_Stations.csv")

# Initialize Flask app
app = Flask(__name__)

@app.route("/chatbot", methods=["POST"])
def chatbot():
    user_input = request.json.get("message", "").lower()

    if "location" in user_input:
        locations = df["Address"].unique()
        return jsonify({"response": f"Available locations: {', '.join(map(str, locations))}"})

    if "station type" in user_input:
        station_types = ["AC", "DC", "HPC"]
        return jsonify({"response": f"Available station types: {', '.join(station_types)}"})

    if "predict" in user_input:
        sample_input = [[1, 1]]
        prediction = model.predict(sample_input)[0]
        return jsonify({"response": f"Predicted Charging Load: {prediction:.2f} kW"})

    return jsonify({"response": "Ask me about locations, station types, or request a prediction!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)