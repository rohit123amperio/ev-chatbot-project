import pandas as pd

# Load dataset
df = pd.read_excel("EV_Charging_Stations.xlsx")

# Display dataset info
print("Dataset Overview:\n", df.head())

# Convert categorical data to numerical format
df["Station Type"] = df["Station Type"].astype("category").cat.codes
df["Category"] = df["Category"].astype("category").cat.codes

# Save the processed dataset
df.to_csv("Processed_Stations.csv", index=False)
print("✅ Dataset processed and saved as 'Processed_Stations.csv'")