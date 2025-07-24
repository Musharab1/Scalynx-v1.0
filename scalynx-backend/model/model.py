import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# Load CSV
df = pd.read_csv("data/synthetic_business_ideas.csv")

# Convert text labels to numbers
df['label'] = df['label'].map({'valid': 1, 'invalid': 0})

# Features and target
X = df[['innovation', 'demand', 'feasibility']]
y = df['label']

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest model
rf_model = RandomForestClassifier(random_state=42)
rf_model.fit(X_train, y_train)

# Save model
os.makedirs("model", exist_ok=True)
joblib.dump(rf_model, "model/model.pkl")

print("✅ Model training complete.")
print("📦 Model saved to: model/model.pkl")
print("📊 Loaded dataset shape:", df.shape)
print("🔍 First few rows:")
print(df.head())
