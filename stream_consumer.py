import json
import joblib
import pandas as pd
import threading
import time
from kafka import KafkaConsumer
import os

# 1. Load the Champion Model Engine
model_path = "models/fraud_model.pkl" if os.path.exists("models") else "model/fraud_model.pkl"
model = joblib.load(model_path)

# 2. Setup Kafka Consumer Connection
consumer = KafkaConsumer(
    'transactions',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    auto_offset_reset='latest'  # Set to 'latest' to catch fresh simulated events
)

# 3. Data Storage for the Dashboard
results_list = []

def export_to_csv():
    """Background task to save the results to a CSV every 5 seconds"""
    while True:
        if results_list:
            # Convert accumulated payloads to a DataFrame and dump to disk
            df = pd.DataFrame(results_list)
            df.to_csv("fraud_data.csv", index=False)
        time.sleep(5)

# Start the background saver thread
threading.Thread(target=export_to_csv, daemon=True).start()

print("🧠 Consumer engine active. Evaluating high-dimensional synthetic transaction streams...")

# 4. Main Processing Loop
for message in consumer:
    tx = message.value  # Contains user_id, Time, Amount, V1-V28
    
    # Wrap the incoming dictionary in a temporary DataFrame row
    tx_df = pd.DataFrame([tx])
    
    # Extract and sort features to match the exact schema the champion model was trained on.
    # This dynamically drops extra metadata like 'user_id', 'prediction', or 'timestamp'.
    tx_features = tx_df[model.feature_names_in_]
    
    # Run the Prediction using the complete 30-feature matrix
    pred = model.predict(tx_features)
    result = "FRAUD" if pred[0] == 1 else "LEGIT"
    
    # Enrich the original payload with operational metadata for the Streamlit UI
    tx['prediction'] = result
    tx['timestamp'] = time.strftime('%H:%M:%S')
    results_list.append(tx)
    
    # Print clean status log to the terminal (Note the capital 'Amount' from the Kaggle schema)
    status_icon = "🚨" if result == "FRAUD" else "✅"
    print(f"{status_icon} Evaluation: User {tx['user_id']} | Amt: ${tx['Amount']:.2f} -> {result}")