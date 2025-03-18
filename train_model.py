import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib

# Load processed dataset
df = pd.read_csv("Processed_Stations.csv")

# Define input features (Station Type & Category) and target (Charging Load)
X = df[["Station Type", "Category"]]
y = df["Charging Load (kW)"]

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save trained model
joblib.dump(model, "charging_load_model.pkl")
print("✅ Model trained and saved successfully!")