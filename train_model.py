import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
import joblib

# ✅ Load dataset
df = pd.read_csv("Processed_Stations.csv")

# ✅ Feature Engineering: Encode Categorical Variables
df["Station Type"] = df["Station Type"].astype("category").cat.codes
df["Category"] = df["Category"].astype("category").cat.codes
df["City"] = df["Address"].apply(lambda x: x.split(",")[1].strip()).astype("category").cat.codes

# ✅ Simulate Peak Hours (Randomly Assigned for Model)
df["Peak Hours"] = np.random.choice([0, 1], size=len(df))  # 1 = Peak, 0 = Non-Peak

# ✅ Simulate Weather Conditions (Randomly Assigned)
weather_conditions = {"Normal": 0, "Hot": 1, "Cold": 2, "Rainy": 3}
df["Weather"] = np.random.choice(list(weather_conditions.values()), size=len(df))

# ✅ Define Features & Target Variable
X = df[["Station Type", "Category", "City", "Peak Hours", "Weather"]]
y = df["Charging Load (kW)"]

# ✅ Split Data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ✅ Train XGBoost Model
model = xgb.XGBRegressor(n_estimators=200, learning_rate=0.1, max_depth=6, random_state=42)
model.fit(X_train, y_train)

# ✅ Save Model
joblib.dump(model, "charging_load_model.pkl")
print("✅ Model trained & saved successfully!")