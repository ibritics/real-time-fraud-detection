import json
import time
import random
import os
from kafka import KafkaProducer

# 1. Wait/Load the structural boundaries exported by train.py
bounds_path = "models/feature_bounds.json"
if not os.path.exists(bounds_path):
    print(f"❌ Error: Cannot find {bounds_path}. Run train.py first to extract boundaries!")
    exit(1)

with open(bounds_path, "r") as f:
    feature_bounds = json.load(f)

# 2. Setup Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

print("🚀 Producer started. Simulating streaming features based on real dataset Min/Max ranges...")

while True:
    data = {}
    
    # Generate a random uniform number between the true min and max for all 30 features
    for feature, limits in feature_bounds.items():
        data[feature] = round(random.uniform(limits["min"], limits["max"]), 4)
    
    # 3. Add a synthetic tracking ID for your Streamlit UI display
    data["user_id"] = random.randint(1000, 9999)
    
    # Send payload to Kafka
    producer.send('transactions', value=data)
    print(f"📤 Sent -> User: {data['user_id']} | Amt: ${data['Amount']:.2f}")
    
    time.sleep(1)