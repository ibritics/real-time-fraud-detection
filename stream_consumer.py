import json
import joblib
import pandas as pd
import threading
import time
from kafka import KafkaConsumer
import os

# 1. Load the Model (The Brain)
# Check if your folder is called 'model' or 'models' based on your train.py
model_path = "models/fraud_model.pkl" if os.path.exists("models") else "model/fraud_model.pkl"
model = joblib.load(model_path)

# 2. Setup Kafka Consumer
consumer = KafkaConsumer(
    'transactions',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    auto_offset_reset='earliest'
)

# 3. Data Storage for the Dashboard
results_list = []

def export_to_csv():
    """Background task to save the results to a CSV every 5 seconds"""
    while True:
        if results_list:
            # We use CSV because Streamlit can read it while we write to it
            df = pd.DataFrame(results_list)
            df.to_csv("fraud_data.csv", index=False)
        time.sleep(5)

# Start the background saver
threading.Thread(target=export_to_csv, daemon=True).start()

print("🧠 Consumer connected. Monitoring live stream and updating fraud_data.csv...")

# 4. Main Processing Loop
for message in consumer:
    tx = message.value
    
    # Run the Prediction
    pred = model.predict([[tx['amount'], tx['is_international']]])
    result = "FRAUD" if pred[0] == 1 else "LEGIT"
    
    # Enrich the data for the UI
    tx['prediction'] = result
    tx['timestamp'] = time.strftime('%H:%M:%S')
    results_list.append(tx)
    
    # Print to console so we know it's working
    status_icon = "🚨" if result == "FRAUD" else "✅"
    print(f"{status_icon} Processed: User {tx['user_id']} | Amt: ${tx['amount']}")