import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

def train_model():
    # 1. Generate Fake Data
    np.random.seed(42)
    n = 1000
    amt = np.random.uniform(10, 1000, n)
    is_intl = np.random.randint(0, 2, n)
    # Logic: Amount > 800 + International = Fraud
    fraud = ((amt > 800) & (is_intl == 1)).astype(int)
    
    df = pd.DataFrame({'amount': amt, 'is_international': is_intl, 'fraud': fraud})
    
    # 2. Train
    X = df[['amount', 'is_international']]
    y = df['fraud']
    model = RandomForestClassifier(n_estimators=10)
    model.fit(X, y)
    
    # 3. Save
    os.makedirs("models", exist_ok=True)
    joblib.dump(model, "models/fraud_model.pkl")
    print("✅ Model trained and saved in /models/fraud_model.pkl")

if __name__ == "__main__":
    train_model()